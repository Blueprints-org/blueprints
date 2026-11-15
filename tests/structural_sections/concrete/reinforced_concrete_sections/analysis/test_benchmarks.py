"""Numerical benchmarks against closed-form hand calculations (marked slow).

Reference section: 300 x 500 mm, C30/37, 4 D20 B500B on the lower edge — the classic cracked-section
neutral-axis and steel-stress formulas.
"""

import math

import pytest

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, Regime
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
class TestValidationPageHandCalculations:
    """Pin the hand calculations of the validation documentation page on its reference beam.

    Rectangular 300 x 600 mm, C30/37, 4 D25 B500B on the lower edge (50 mm cover). The closed-form values
    are those worked out step by step on the page; keeping this test green keeps the page honest.
    """

    @staticmethod
    def _analysis() -> CrossSectionAnalysis:
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial(ReinforcementSteelQuality.B500B)
        cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=concrete)
        cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, edge="lower", cover=50, material=steel)
        return CrossSectionAnalysis(cs)

    def test_cracked_pure_bending(self) -> None:
        """M = 200 kNm: x = 171.0 mm, sigma_c = -16.24 MPa, sigma_s = 212.0 MPa."""
        result = self._analysis().stress(SectionForces(m_y=200))
        assert result.is_cracked
        assert result.strain_plane is not None
        assert result.strain_plane.neutral_axis_depth == pytest.approx(171.0, rel=2e-3)
        assert result.concrete_stress_min == pytest.approx(-16.24, rel=2e-3)
        assert max(bar.stress for bar in result.rebar_results) == pytest.approx(212.0, rel=2e-3)

    def test_uncracked_transformed_section(self) -> None:
        """M = 40 kNm: x = 312.5 mm, sigma_c = -2.106 / +1.938 MPa, sigma_s = 9.24 MPa."""
        result = self._analysis().stress(SectionForces(m_y=40))
        assert not result.is_cracked
        assert result.strain_plane is not None
        assert result.strain_plane.neutral_axis_depth == pytest.approx(312.5, rel=2e-3)
        assert result.concrete_stress_min == pytest.approx(-2.106, rel=2e-3)
        assert result.concrete_stress_max == pytest.approx(1.938, rel=2e-3)
        assert max(bar.stress for bar in result.rebar_results) == pytest.approx(9.24, rel=2e-3)
