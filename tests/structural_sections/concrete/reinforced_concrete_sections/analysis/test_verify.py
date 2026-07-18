"""Tests for the ULS unity check (verify) and the biaxial envelope intersection."""

import math

import pytest

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import (
    BiaxialInteractionResult,
    CrossSectionAnalysis,
    InteractionPoint,
    UtilizationResult,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces


def _beam_analysis() -> CrossSectionAnalysis:
    """300 x 500 C30/37 with 4 D20 B500B on the lower edge."""
    cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


def _beam_steel_area() -> float:
    """Total reinforcement area of the beam section as the analyzer sees it [mm2]."""
    analysis = _beam_analysis()
    return sum(rebar.area for rebar in analysis._cross_section.longitudinal_rebars)  # noqa: SLF001 — mirrors the capacity source


def _column_analysis() -> CrossSectionAnalysis:
    """400 x 400 C30/37 with one D25 in each corner (fully symmetric)."""
    cs = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    for x in (-150, 150):
        for y in (-150, 150):
            cs.add_longitudinal_rebar(Rebar(diameter=25, x=x, y=y, material=ReinforcementSteelMaterial()))
    return CrossSectionAnalysis(cs)


class TestUniaxialVerification:
    """Uniaxial design actions are checked against the bending capacity at the design axial force."""

    def test_half_the_capacity_gives_half_utilization(self) -> None:
        """A design moment at half the sagging capacity verifies at utilization 0.5."""
        analysis = _beam_analysis()
        capacity = analysis.bending_capacity()
        result = analysis.verify(SectionForces(m_y=0.5 * capacity.m_rd))
        assert isinstance(result, UtilizationResult)
        assert result.utilization == pytest.approx(0.5, rel=1e-3)
        assert result.is_ok
        assert result.governing == "uniaxial bending"
        assert result.m_rd == pytest.approx(capacity.m_rd)
        assert result.n_rd is None  # no axial force in the design action

    def test_overloaded_section_fails_the_check(self) -> None:
        """A design moment beyond the capacity verifies at utilization > 1."""
        analysis = _beam_analysis()
        capacity = analysis.bending_capacity()
        result = analysis.verify(SectionForces(m_y=1.2 * capacity.m_rd))
        assert result.utilization == pytest.approx(1.2, rel=1e-3)
        assert not result.is_ok

    def test_hogging_uses_the_hogging_capacity(self) -> None:
        """A negative m_y is checked against the (smaller) hogging capacity."""
        analysis = _beam_analysis()
        hogging = analysis.bending_capacity(theta=180.0)
        result = analysis.verify(SectionForces(m_y=-0.5 * abs(hogging.m_y_rd)))
        assert result.utilization == pytest.approx(0.5, rel=1e-3)
        assert result.m_rd == pytest.approx(hogging.m_rd)

    def test_m_z_only_uses_the_z_axis_capacity(self) -> None:
        """A pure m_z action is checked against the capacity about the z-axis."""
        analysis = _column_analysis()
        about_z = analysis.bending_capacity(theta=90.0)
        result = analysis.verify(SectionForces(m_z=0.5 * abs(about_z.m_z_rd)))
        assert result.utilization == pytest.approx(0.5, rel=1e-3)

    def test_axial_force_shifts_the_capacity(self) -> None:
        """The check uses the bending capacity at the design axial force (N-M interaction)."""
        analysis = _beam_analysis()
        with_compression = analysis.bending_capacity(n=-500.0)
        result = analysis.verify(SectionForces(n=-500.0, m_y=0.5 * with_compression.m_rd))
        assert result.utilization == pytest.approx(0.5, rel=1e-3)
        assert result.n_rd is not None


class TestAxialVerification:
    """Pure axial design actions are checked against the squash or tensile capacity."""

    def test_pure_compression_ratio(self) -> None:
        """A compressive force at half the squash load verifies at utilization 0.5."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial()
        a_s = _beam_steel_area()
        squash = (concrete.f_cd * (300 * 500 - a_s) + steel.f_yd * a_s) / 1e3  # kN magnitude
        result = _beam_analysis().verify(SectionForces(n=-0.5 * squash))
        assert result.governing == "axial"
        assert result.utilization == pytest.approx(0.5, rel=1e-3)
        assert result.m_rd is None

    def test_pure_tension_ratio(self) -> None:
        """A tensile force at half the steel capacity verifies at utilization 0.5."""
        steel = ReinforcementSteelMaterial()
        tension_capacity = steel.f_yd * _beam_steel_area() / 1e3  # kN
        result = _beam_analysis().verify(SectionForces(n=0.5 * tension_capacity))
        assert result.governing == "axial"
        assert result.utilization == pytest.approx(0.5, rel=1e-3)
        assert result.n_rd == pytest.approx(tension_capacity, rel=1e-6)

    def test_axial_overload_governs_without_a_bending_check(self) -> None:
        """An axial force beyond its capacity governs outright; no bending capacity is computed."""
        concrete = ConcreteMaterial(ConcreteStrengthClass.C30_37)
        steel = ReinforcementSteelMaterial()
        a_s = _beam_steel_area()
        squash = (concrete.f_cd * (300 * 500 - a_s) + steel.f_yd * a_s) / 1e3
        result = _beam_analysis().verify(SectionForces(n=-2.0 * squash, m_y=100.0))
        assert result.governing == "axial"
        assert result.utilization == pytest.approx(2.0, rel=1e-3)
        assert not result.is_ok
        assert result.m_rd is None


class TestBiaxialVerification:
    """Biaxial design actions are checked against the biaxial envelope along the load direction."""

    def test_half_the_diagonal_capacity_gives_half_utilization(self) -> None:
        """A diagonal moment pair at half the envelope capacity verifies at utilization ~0.5."""
        analysis = _column_analysis()
        envelope = analysis.biaxial_interaction(n_points=16)
        diagonal_capacity = envelope.capacity_along(1.0, 1.0)
        component = 0.5 * diagonal_capacity / math.sqrt(2.0)
        result = analysis.verify(SectionForces(m_y=component, m_z=component), n_points=16)
        assert result.governing == "biaxial bending"
        assert result.utilization == pytest.approx(0.5, rel=0.02)


class TestCapacityAlong:
    """The envelope-ray intersection helper."""

    def _unit_square_envelope(self) -> BiaxialInteractionResult:
        """A synthetic square envelope through (+-100, -+100)."""
        corners = [(100.0, 100.0), (-100.0, 100.0), (-100.0, -100.0), (100.0, -100.0), (100.0, 100.0)]
        points = tuple(InteractionPoint(n=0.0, m_y=m_y, m_z=m_z, m=math.hypot(m_y, m_z)) for m_y, m_z in corners)
        return BiaxialInteractionResult(n=0.0, points=points, raw=None)

    def test_axis_aligned_direction(self) -> None:
        """Along the m_y axis the square envelope is intersected at its edge."""
        assert self._unit_square_envelope().capacity_along(50.0, 0.0) == pytest.approx(100.0)

    def test_diagonal_direction(self) -> None:
        """Along the diagonal the square envelope is intersected at its corner."""
        assert self._unit_square_envelope().capacity_along(1.0, 1.0) == pytest.approx(math.hypot(100.0, 100.0))

    def test_zero_direction_raises(self) -> None:
        """A zero moment pair has no direction."""
        with pytest.raises(ValueError, match="direction is undefined"):
            self._unit_square_envelope().capacity_along(0.0, 0.0)

    def test_degenerate_envelope_raises(self) -> None:
        """An envelope collapsed to a single point cannot be intersected."""
        point = InteractionPoint(n=0.0, m_y=0.0, m_z=0.0, m=0.0)
        degenerate = BiaxialInteractionResult(n=0.0, points=(point, point), raw=None)
        with pytest.raises(ValueError, match="degenerate"):
            degenerate.capacity_along(1.0, 0.0)


class TestErrorPaths:
    """Clear errors for unsupported inputs."""

    def test_without_rebars_raises(self) -> None:
        """A verification without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="Verification requires at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).verify(SectionForces(m_y=100.0))
