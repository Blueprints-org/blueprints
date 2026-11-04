"""Tests for the ULS bending capacity (sign/axis round trip, behaviour and error paths).

The sign/axis round trip is the highest correctness risk of the capacity path: Blueprints is
tension-positive on SAF y/z member axes, the backend compression-positive on geometric x/y axes. The
conversion pair is pinned directly and the capacity signs are pinned on asymmetric sections.
"""

import pytest

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import (
    CrossSectionAnalysis,
    SteelBranch,
    UltimateCapacityResult,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import (
    _from_backend_actions,
    _to_backend_actions,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces


def _bottom_reinforced_analysis() -> CrossSectionAnalysis:
    """300 x 500 C30/37 with 4 D20 B500B on the lower edge only (asymmetric about the y-axis)."""
    cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


def _square_symmetric_analysis() -> CrossSectionAnalysis:
    """400 x 400 C30/37 with one D25 in each corner (fully symmetric)."""
    cs = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    for x in (-150, 150):
        for y in (-150, 150):
            cs.add_longitudinal_rebar(Rebar(diameter=25, x=x, y=y, material=ReinforcementSteelMaterial()))
    return CrossSectionAnalysis(cs)


class TestActionRoundTrip:
    """Blueprints -> backend -> Blueprints action conversion is the exact identity."""

    @pytest.mark.parametrize(
        "forces",
        [
            pytest.param(SectionForces(n=-1000), id="pure_compression"),
            pytest.param(SectionForces(n=500), id="pure_tension"),
            pytest.param(SectionForces(m_y=150), id="sagging"),
            pytest.param(SectionForces(m_y=-150), id="hogging"),
            pytest.param(SectionForces(m_z=80), id="m_z_only"),
            pytest.param(SectionForces(m_z=-80), id="m_z_negative"),
            pytest.param(SectionForces(n=-300, m_y=120, m_z=-45), id="biaxial_with_compression"),
        ],
    )
    def test_round_trip_is_identity(self, forces: SectionForces) -> None:
        """_from_backend_actions inverts _to_backend_actions exactly."""
        n, m_y, m_z = _from_backend_actions(*_to_backend_actions(forces))
        assert n == pytest.approx(forces.n)
        assert m_y == pytest.approx(forces.m_y)
        assert m_z == pytest.approx(forces.m_z)


class TestBendingCapacitySigns:
    """Capacity signs pinned on asymmetric sections (the axis/sign mapping proof)."""

    def test_sagging_capacity_is_positive_m_y(self) -> None:
        """theta=0 gives the sagging capacity: positive m_y_rd, no m_z component."""
        capacity = _bottom_reinforced_analysis().bending_capacity()
        assert capacity.m_y_rd > 0
        assert capacity.m_z_rd == pytest.approx(0.0, abs=1e-6 * capacity.m_y_rd)
        assert capacity.m_rd == pytest.approx(capacity.m_y_rd)

    def test_hogging_capacity_is_negative_m_y_and_smaller(self) -> None:
        """theta=180 gives the hogging capacity: negative m_y_rd, smaller than sagging (bottom steel only)."""
        analysis = _bottom_reinforced_analysis()
        sagging = analysis.bending_capacity(theta=0.0)
        hogging = analysis.bending_capacity(theta=180.0)
        assert hogging.m_y_rd < 0
        assert abs(hogging.m_y_rd) < sagging.m_y_rd

    def test_theta_90_bends_about_the_z_axis(self) -> None:
        """theta=90 gives the capacity about the z-axis; symmetry makes it equal to the y-axis capacity."""
        analysis = _square_symmetric_analysis()
        about_y = analysis.bending_capacity(theta=0.0)
        about_z = analysis.bending_capacity(theta=90.0)
        assert about_z.m_y_rd == pytest.approx(0.0, abs=1e-4 * about_y.m_rd)
        assert about_z.m_z_rd > 0  # theta=90 compresses the -x side, so the +x side is in tension
        assert about_z.m_z_rd == pytest.approx(about_y.m_y_rd, rel=1e-2)

    def test_neutral_axis_metadata(self) -> None:
        """The capacity carries the neutral-axis depth, angle and k_u."""
        capacity = _bottom_reinforced_analysis().bending_capacity()
        assert isinstance(capacity, UltimateCapacityResult)
        assert 0 < capacity.neutral_axis_depth < 500
        assert capacity.neutral_axis_angle == pytest.approx(0.0)
        assert 0 < capacity.k_u < 1


class TestAxialForceEffect:
    """The axial force shifts the capacity along the interaction curve."""

    def test_moderate_compression_raises_the_capacity(self) -> None:
        """A moderate compression raises the bending capacity of an under-reinforced section."""
        analysis = _bottom_reinforced_analysis()
        pure_bending = analysis.bending_capacity()
        with_compression = analysis.bending_capacity(n=-500.0)
        assert with_compression.m_rd > pure_bending.m_rd

    def test_echoes_the_axial_force(self) -> None:
        """The result echoes the (converged) axial force in Blueprints sign convention."""
        capacity = _bottom_reinforced_analysis().bending_capacity(n=-500.0)
        assert capacity.n == pytest.approx(-500.0, rel=1e-3)

    def test_axial_force_beyond_capacity_raises_clear_error(self) -> None:
        """A tensile force beyond the section's tensile capacity cannot reach equilibrium."""
        with pytest.raises(ValueError, match="did not converge"):
            _bottom_reinforced_analysis().bending_capacity(n=100_000.0)


class TestSteelBranch:
    """The inclined steel branch adds hardening capacity over the horizontal branch."""

    def test_inclined_branch_gives_higher_capacity(self) -> None:
        """The inclined branch (hardening towards k*f_yd) yields a slightly higher capacity."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
        horizontal = CrossSectionAnalysis(cs).bending_capacity()
        inclined = CrossSectionAnalysis(cs, steel_branch=SteelBranch.INCLINED).bending_capacity()
        assert inclined.m_rd > horizontal.m_rd
        assert inclined.m_rd < 1.1 * horizontal.m_rd  # hardening is bounded by k = 1.08


class TestErrorPaths:
    """Clear errors for unsupported inputs."""

    def test_without_rebars_raises(self) -> None:
        """A capacity analysis without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="Ultimate capacity analysis requires at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).bending_capacity()
