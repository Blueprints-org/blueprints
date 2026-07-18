"""Numerical benchmarks against closed-form hand calculations (marked slow).

Reference section: 300 x 500 mm, C30/37, 4 D20 B500B on the lower edge — the classic cracked-section
neutral-axis and steel-stress formulas.
"""

import math

import numpy as np
import pytest

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import StressStrainResult
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

WIDTH = 300.0
HEIGHT = 500.0


def _reference() -> tuple[CrossSectionAnalysis, float, float, float, float]:
    """Build the reference analysis and return (analysis, b, d, a_s, n_e)."""
    concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
    steel = ReinforcementSteelMaterial()
    cs = RectangularReinforcedCrossSection(width=WIDTH, height=HEIGHT, concrete_material=concrete)
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=steel, edge="lower")
    rebars = cs.longitudinal_rebars
    a_s = sum(rebar.area for rebar in rebars)
    top_fibre = cs.profile.polygon.bounds[3]
    d = top_fibre - rebars[0].y  # effective depth from compression fibre to rebar centroid
    n_e = steel.e_s / concrete.e_cm
    return CrossSectionAnalysis(cs), WIDTH, d, a_s, n_e


def _cracked_neutral_axis(b: float, d: float, a_s: float, n_e: float) -> float:
    """Solve the classic quadratic 0.5*b*x^2 = n_e*a_s*(d - x) for the cracked neutral-axis depth x."""
    return (-n_e * a_s + math.sqrt((n_e * a_s) ** 2 + 2 * b * n_e * a_s * d)) / b


@pytest.mark.slow
class TestCrackedBenchmarks:
    """Cracked-section results against the classic transformed-section formulas."""

    def test_neutral_axis_matches_quadratic(self) -> None:
        """The cracked neutral-axis depth matches the closed-form quadratic solution."""
        analysis, b, d, a_s, n_e = _reference()
        expected_x = _cracked_neutral_axis(b, d, a_s, n_e)
        result = analysis.stress(SectionForces(m_y=150), regime=Regime.SLS_CRACKED)
        assert result.cracked_properties is not None
        assert result.cracked_properties.neutral_axis_depth == pytest.approx(expected_x, rel=0.02)

    def test_rebar_stress_matches_lever_arm_formula(self) -> None:
        """The cracked steel stress matches sigma_s = M / (A_s * z) with z = d - x/3."""
        analysis, b, d, a_s, n_e = _reference()
        moment = 150.0  # kNm
        x = _cracked_neutral_axis(b, d, a_s, n_e)
        lever_arm = d - x / 3
        expected_stress = moment * 1e6 / (a_s * lever_arm)  # MPa, tension positive
        result = analysis.stress(SectionForces(m_y=moment), regime=Regime.SLS_CRACKED)
        assert result.rebar_results[0].stress == pytest.approx(expected_stress, rel=0.02)


@pytest.mark.slow
class TestCreepBenchmarks:
    """Creep (E_c,eff = E_cm / (1 + phi)) against the same closed-form formulas with a doubled modular ratio.

    With phi = 1 the effective modulus halves, so the modular ratio alpha_e = E_s / E_c,eff doubles: the
    cracked neutral axis deepens per the classic quadratic and the steel stress follows the lever-arm
    formula with the new x.
    """

    def test_neutral_axis_matches_quadratic_with_doubled_modular_ratio(self) -> None:
        """With phi = 1 the cracked neutral axis matches the quadratic solved with 2 * alpha_e."""
        analysis, b, d, a_s, n_e = _reference()
        expected_x = _cracked_neutral_axis(b, d, a_s, 2 * n_e)
        result = analysis.stress(SectionForces(m_y=150), regime=Regime.SLS_CRACKED, creep_coefficient=1.0)
        assert result.cracked_properties is not None
        assert result.cracked_properties.neutral_axis_depth == pytest.approx(expected_x, rel=0.02)

    def test_rebar_stress_matches_lever_arm_formula_with_creep(self) -> None:
        """With phi = 1 the steel stress matches sigma_s = M / (A_s * z) with z from the deepened x."""
        analysis, b, d, a_s, n_e = _reference()
        moment = 150.0  # kNm
        x = _cracked_neutral_axis(b, d, a_s, 2 * n_e)
        lever_arm = d - x / 3
        expected_stress = moment * 1e6 / (a_s * lever_arm)  # MPa, tension positive
        result = analysis.stress(SectionForces(m_y=moment), regime=Regime.SLS_CRACKED, creep_coefficient=1.0)
        assert result.rebar_results[0].stress == pytest.approx(expected_stress, rel=0.02)


@pytest.mark.slow
class TestUltimateCapacityBenchmark:
    """M_Rd against the closed-form solution for the bilinear concrete design diagram.

    With the bilinear diagram (eps_c3 = 1.75, eps_cu3 = 3.5 per mille) the compression block over the
    neutral-axis depth x carries F_c = alpha * f_cd * b * x with alpha = 1 - eps_c3 / (2 * eps_cu3) =
    0.75, acting at beta * x = 0.35 / 0.9 * x ~ 0.3889 * x below the compression fibre. For a yielding
    single-layer tension section: x = A_s * f_yd / (alpha * f_cd * b) and M_Rd = A_s * f_yd * (d - beta * x).
    """

    def test_m_rd_matches_bilinear_hand_calculation(self) -> None:
        """Pure-bending M_Rd matches the closed-form bilinear stress-block solution."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial()
        analysis, b, d, a_s, _ = _reference()

        alpha = 1 - concrete.eps_c3 / (2 * concrete.eps_cu3)
        # centroid of the bilinear block from the compression fibre, as a fraction of x
        plateau = 1 - concrete.eps_c3 / concrete.eps_cu3
        beta = (plateau * plateau / 2 + (1 - plateau) / 2 * (plateau + (1 - plateau) / 3)) / alpha
        x = a_s * steel.f_yd / (alpha * concrete.f_cd * b)
        expected_m_rd = a_s * steel.f_yd * (d - beta * x) / 1e6  # kNm

        capacity = analysis.bending_capacity()
        assert capacity.m_rd == pytest.approx(expected_m_rd, rel=0.01)

    def test_neutral_axis_depth_matches_hand_calculation(self) -> None:
        """The ultimate neutral-axis depth matches x = A_s * f_yd / (alpha * f_cd * b)."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial()
        analysis, b, _, a_s, _ = _reference()
        alpha = 1 - concrete.eps_c3 / (2 * concrete.eps_cu3)
        expected_x = a_s * steel.f_yd / (alpha * concrete.f_cd * b)
        assert analysis.bending_capacity().neutral_axis_depth == pytest.approx(expected_x, rel=0.02)


@pytest.mark.slow
class TestInteractionBenchmarks:
    """N-M interaction diagram endpoints against closed-form values.

    The lumped bars perforate the concrete geometry, so the squash load counts the net concrete area:
    N_Rd = f_cd * (A_c - A_s) + f_yd * A_s (compression negative in Blueprints). The tension endpoint is
    the bare steel capacity f_yd * A_s (concrete carries no tension).
    """

    def test_squash_load_matches_hand_calculation(self) -> None:
        """The pure-compression endpoint equals f_cd * (A_c - A_s) + f_yd * A_s."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial()
        analysis, *_ = _reference()
        a_c = WIDTH * HEIGHT
        a_s = 4 * math.pi / 4 * 20**2
        expected_squash = -(concrete.f_cd * (a_c - a_s) + steel.f_yd * a_s) / 1e3  # kN, compression negative
        result = analysis.interaction()
        assert min(point.n for point in result.points) == pytest.approx(expected_squash, rel=0.01)

    def test_tension_endpoint_matches_steel_capacity(self) -> None:
        """The pure-tension endpoint equals f_yd * A_s (steel only)."""
        steel = ReinforcementSteelMaterial()
        analysis, *_ = _reference()
        a_s = 4 * math.pi / 4 * 20**2
        expected_tension = steel.f_yd * a_s / 1e3  # kN, tension positive
        result = analysis.interaction()
        assert max(point.n for point in result.points) == pytest.approx(expected_tension, rel=0.01)

    def test_pure_bending_point_matches_bending_capacity(self) -> None:
        """The diagram's N=0 control point reproduces the direct bending capacity."""
        analysis, *_ = _reference()
        capacity = analysis.bending_capacity()
        result = analysis.interaction()
        pure_bending = min(result.points, key=lambda point: abs(point.n))
        assert pure_bending.n == pytest.approx(0.0, abs=1.0)
        assert pure_bending.m == pytest.approx(capacity.m_rd, rel=1e-3)


@pytest.mark.slow
class TestMomentCurvatureBenchmarks:
    """Moment-curvature anchors: uncracked stiffness, cracking kink and ultimate moment.

    The uncracked branch must follow E_cm * I of the transformed section (bars perforate the concrete,
    so the transformed inertia adds (n_e - 1) * A_s terms about the shifted centroid). The kink must sit
    at the cracking moment and the peak of the curve must reproduce the ultimate capacity M_Rd.
    """

    @staticmethod
    def _uncracked_stiffness() -> float:
        """E_cm * I of the transformed uncracked section in kNm*mm (M[kNm] / kappa[1/mm])."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        _, b, d, a_s, n_e = _reference()
        y_bar = HEIGHT / 2 - d  # rebar y-coordinate relative to the section centroid (negative, below)
        a_transformed = b * HEIGHT + (n_e - 1) * a_s
        centroid_shift = (n_e - 1) * a_s * y_bar / a_transformed
        inertia = b * HEIGHT**3 / 12 + b * HEIGHT * centroid_shift**2 + (n_e - 1) * a_s * (y_bar - centroid_shift) ** 2
        return concrete.e_cm * inertia * 1e-6

    def test_uncracked_branch_follows_transformed_stiffness(self) -> None:
        """The secant stiffness of the early branch equals E_cm * I of the transformed section."""
        result = _reference()[0].moment_curvature()
        kappa_probe = 2e-7  # well below the cracking curvature
        secant = float(np.interp(kappa_probe, result.kappa, result.m)) / kappa_probe
        assert secant == pytest.approx(self._uncracked_stiffness(), rel=0.03)

    def test_cracking_kink_sits_at_m_cr(self) -> None:
        """Past the cracking curvature (m_cr / EI) the secant stiffness drops off the uncracked branch."""
        analysis = _reference()[0]
        cracked = analysis.stress(SectionForces(m_y=150), regime=Regime.SLS_CRACKED).cracked_properties
        assert cracked is not None
        stiffness = self._uncracked_stiffness()
        kappa_cr = cracked.m_cr / stiffness
        result = analysis.moment_curvature()
        secant_before = float(np.interp(0.5 * kappa_cr, result.kappa, result.m)) / (0.5 * kappa_cr)
        secant_after = float(np.interp(2.5 * kappa_cr, result.kappa, result.m)) / (2.5 * kappa_cr)
        assert secant_before == pytest.approx(stiffness, rel=0.03)
        assert secant_after < 0.8 * stiffness

    def test_ultimate_moment_matches_bending_capacity(self) -> None:
        """The peak of the moment-curvature curve reproduces the ultimate capacity M_Rd."""
        analysis = _reference()[0]
        capacity = analysis.bending_capacity()
        result = analysis.moment_curvature()
        assert result.m_ultimate == pytest.approx(capacity.m_rd, rel=0.03)


@pytest.mark.slow
class TestIdeaStaticaReference:
    """Pin the IDEA StatiCa RCS reference case from the analysis example documentation page.

    Rectangular 300 x 600 mm, C30/37, 4 D25 B500B on the lower edge (50 mm cover), pure M_y = 200 kNm
    (SLS, N = 0). The IDEA StatiCa RCS reference values are hard-coded here so the suite never calls the
    external tool; keeping this test green keeps the documented comparison table honest.
    """

    def _idea_reference_result(self) -> StressStrainResult:
        """Build and analyze the documented IDEA reference section."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial(ReinforcementSteelQuality.B500B)
        cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=concrete)
        cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", material=steel)
        return CrossSectionAnalysis(cs).stress(SectionForces(m_y=200))

    def test_cracks_like_idea(self) -> None:
        """The reference case cracks, matching IDEA StatiCa RCS."""
        assert self._idea_reference_result().is_cracked

    def test_concrete_compression_matches_idea(self) -> None:
        """Max concrete compression matches IDEA StatiCa RCS (-16.23 MPa)."""
        assert self._idea_reference_result().concrete_stress_min == pytest.approx(-16.23, abs=0.1)

    def test_reinforcement_stress_matches_idea(self) -> None:
        """Reinforcement stress matches IDEA StatiCa RCS (211.98 MPa)."""
        assert self._idea_reference_result().rebar_results[0].stress == pytest.approx(211.98, rel=0.01)

    def test_reinforcement_strain_matches_idea(self) -> None:
        """Reinforcement strain matches IDEA StatiCa RCS (1.060 per mille)."""
        assert self._idea_reference_result().rebar_results[0].strain == pytest.approx(1.060, rel=0.01)

    def test_neutral_axis_depth_matches_idea(self) -> None:
        """Neutral-axis depth matches IDEA StatiCa RCS (x = 171 mm)."""
        properties = self._idea_reference_result().cracked_properties
        assert properties is not None
        assert properties.neutral_axis_depth == pytest.approx(171.0, rel=0.02)
