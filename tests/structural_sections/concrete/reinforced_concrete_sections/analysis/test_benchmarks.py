"""Numerical benchmarks against closed-form hand calculations (marked slow).

Reference section: 300 x 500 mm, C30/37, 4 D20 B500B on the lower edge — the classic cracked-section
neutral-axis and steel-stress formulas.
"""

import math

import pytest

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial, ReinforcementSteelQuality
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
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
        properties = analysis.cracked_properties(SectionForces(m_y=150))
        assert properties.neutral_axis_depth == pytest.approx(expected_x, rel=0.02)

    def test_rebar_stress_matches_lever_arm_formula(self) -> None:
        """The cracked steel stress matches sigma_s = M / (A_s * z) with z = d - x/3."""
        analysis, b, d, a_s, n_e = _reference()
        moment = 150.0  # kNm
        x = _cracked_neutral_axis(b, d, a_s, n_e)
        lever_arm = d - x / 3
        expected_stress = moment * 1e6 / (a_s * lever_arm)  # MPa, tension positive
        result = analysis.cracked_stress(SectionForces(m_y=moment))
        assert result.rebar_results[0].stress == pytest.approx(expected_stress, rel=0.02)


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
        return CrossSectionAnalysis(cs).calculate_stress(SectionForces(m_y=200))

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
