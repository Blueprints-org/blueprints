"""Sign- and unit-convention tests for the analysis adapter, using the real backend.

These pin the single conversion point in ``_adapter.py``: Blueprints is tension-positive / compression-
negative in kN/kNm; the backend is the opposite. An asymmetric section and a pure-axial case are
mandatory (issue #1061). Not marked slow on purpose — this is the coverage that proves the adapter.
"""

import warnings

import pytest

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces


def _bare_section() -> RectangularReinforcedCrossSection:
    return RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))


def _symmetric_analysis() -> CrossSectionAnalysis:
    cs = _bare_section()
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


class TestNormalForceSign:
    """Pin the normal-force sign (Blueprints tension positive, compression negative)."""

    def test_compression_is_negative(self) -> None:
        """A compressive (negative) normal force yields compressive (negative) concrete stresses."""
        result = _symmetric_analysis().uncracked_stress(SectionForces(n=-1000))
        assert result.concrete_stress_min < 0
        assert result.concrete_stress_max < 0

    def test_tension_is_positive(self) -> None:
        """A tensile (positive) normal force yields tensile (positive) concrete stresses."""
        result = _symmetric_analysis().uncracked_stress(SectionForces(n=500))
        assert result.concrete_stress_max > 0

    def test_pure_axial_is_uniform_and_does_not_warn(self) -> None:
        """Pure axial force gives a uniform stress field and the backend divide warning is suppressed."""
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            result = _symmetric_analysis().uncracked_stress(SectionForces(n=-1000))
        assert result.concrete_stress_min == pytest.approx(result.concrete_stress_max, rel=1e-9)


class TestMomentSign:
    """Pin the bending-moment axis mapping and sign on an asymmetric layout."""

    def test_positive_m_y_tensions_the_bottom(self) -> None:
        """Positive m_y (about the y-axis) tensions the bottom fibre and compresses the top."""
        cs = _bare_section()
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=0, y=-100, material=ReinforcementSteelMaterial()))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=0, y=100, material=ReinforcementSteelMaterial()))
        result = CrossSectionAnalysis(cs).uncracked_stress(SectionForces(m_y=100))
        bottom = next(r for r in result.rebar_results if r.y < 0)
        top = next(r for r in result.rebar_results if r.y > 0)
        assert bottom.stress > 0
        assert top.stress < 0

    def test_positive_m_z_tensions_the_positive_y_side(self) -> None:
        """Positive m_z (about the z-axis) tensions the +x side and compresses the -x side."""
        cs = _bare_section()
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=-100, y=0, material=ReinforcementSteelMaterial()))
        cs.add_longitudinal_rebar(Rebar(diameter=20, x=100, y=0, material=ReinforcementSteelMaterial()))
        result = CrossSectionAnalysis(cs).uncracked_stress(SectionForces(m_z=100))
        positive = next(r for r in result.rebar_results if r.x > 0)
        negative = next(r for r in result.rebar_results if r.x < 0)
        assert positive.stress > 0
        assert negative.stress < 0


class TestAxialMagnitude:
    """Pin the unit conversion against a transformed-section hand calculation."""

    def test_uniform_axial_stress_matches_transformed_section(self) -> None:
        """Pure axial stress equals N / A_transformed (compression negative)."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial()
        cs = _bare_section()
        cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=steel, edge="lower")
        bar_area = 3.141592653589793 / 4 * 20**2
        a_transformed = 300 * 500 + (steel.e_s / concrete.e_cm - 1) * 4 * bar_area
        expected = -1000e3 / a_transformed  # N / mm^2, compression negative
        result = CrossSectionAnalysis(cs).uncracked_stress(SectionForces(n=-1000))
        assert result.concrete_stress_min == pytest.approx(expected, rel=1e-2)
