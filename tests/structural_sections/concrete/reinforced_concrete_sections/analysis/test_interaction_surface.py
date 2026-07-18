"""Tests for the ULS interaction surface, its fixed-N rings and its fixed-direction N-M resultant sections.

The surface build runs one interaction diagram per neutral-axis angle, so a single coarse surface is built
once per module and reused. Its rings are cross-checked against the exact capacity routines, which is the
correctness anchor for the interpolation and slicing.
"""

import matplotlib as mpl
import pytest

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import (
    CrossSectionAnalysis,
    InteractionPoint,
    InteractionSection,
    InteractionSurface,
    MomentInteractionResult,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection


def _analysis() -> CrossSectionAnalysis:
    """Reference 300 x 600 C30/37 section with only bottom reinforcement (asymmetric capacities)."""
    cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


@pytest.fixture(scope="module")
def analysis() -> CrossSectionAnalysis:
    """The reference section analyzer, reused across the module."""
    return _analysis()


@pytest.fixture(scope="module")
def surface(analysis: CrossSectionAnalysis) -> InteractionSurface:
    """A coarse surface with meridians on the principal directions (0, 90, 180, 270 deg)."""
    return analysis.interaction_surface(n_theta=16, n_points=10)


class TestSurfaceBuild:
    """The surface is a set of neutral-axis-angle meridians over a full revolution."""

    def test_has_one_meridian_per_angle(self, surface: InteractionSurface) -> None:
        """The surface carries n_theta meridians at the requested angles."""
        assert isinstance(surface, InteractionSurface)
        assert len(surface.meridians) == 16
        assert surface.thetas[:4] == (0.0, 22.5, 45.0, 67.5)
        assert all(isinstance(meridian, MomentInteractionResult) for meridian in surface.meridians)

    def test_without_rebars_raises(self) -> None:
        """A surface without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="Interaction surface analysis requires at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).interaction_surface()


class TestRing:
    """A fixed-axial-force ring, interpolated from the meridians, matches the exact capacities."""

    def test_ring_is_closed(self, surface: InteractionSurface) -> None:
        """The ring is a closed loop (first vertex repeated at the end)."""
        ring = surface.ring(0.0)
        assert ring.points[0] == ring.points[-1]

    def test_ring_reproduces_exact_bending_capacity(self, surface: InteractionSurface, analysis: CrossSectionAnalysis) -> None:
        """The interpolated ring at N=0 reproduces the exact sagging and hogging capacities."""
        ring = surface.ring(0.0)
        assert ring.capacity_along(1.0, 0.0) == pytest.approx(analysis.bending_capacity(theta=0.0).m_rd, rel=0.02)
        assert ring.capacity_along(-1.0, 0.0) == pytest.approx(analysis.bending_capacity(theta=180.0).m_rd, abs=2.0)

    def test_axial_force_outside_range_raises(self, surface: InteractionSurface) -> None:
        """A ring beyond the surface's axial range (past the squash load) raises a clear error."""
        with pytest.raises(ValueError, match="outside the surface's axial range"):
            surface.ring(-100000.0)


class TestSurface3D:
    """The 3D surface plot renders the (M_y, M_z, N) capacity surface."""

    def test_plot_3d_returns_a_3d_figure(self, surface: InteractionSurface) -> None:
        """plot_3d() returns a figure with a 3D axes labelled M_y, M_z and N."""
        figure = surface.plot_3d(n_levels=8)
        try:
            assert isinstance(figure, Figure)
            (ax,) = figure.axes
            assert ax.name == "3d"
            assert "M_{y,Rd}" in ax.get_xlabel()
            assert "M_{z,Rd}" in ax.get_ylabel()
            assert "N_{Rd}" in ax.get_zlabel()
            assert ax.get_zlim()[0] > ax.get_zlim()[1]  # compression (negative) drawn on top
        finally:
            plt.close(figure)


class TestResultantSection:
    """A fixed-direction N-M resultant section, sliced from the surface."""

    def test_section_about_y_is_closed_and_signed(self, surface: InteractionSurface) -> None:
        """The section along +M_y closes into a loop spanning a sagging and a hogging side."""
        section = surface.section_resultant(m_y=1.0, m_z=0.0)
        assert isinstance(section, InteractionSection)
        assert section.points[0] == section.points[-1]
        signed = section.signed_moments()
        assert max(signed) > 0  # sagging boundary
        assert min(signed) < 0  # hogging boundary

    def test_section_direction_and_projection(self, surface: InteractionSurface) -> None:
        """The section reports its unit direction and projects each point onto it."""
        section = surface.section_resultant(m_y=3.0, m_z=4.0)
        assert section.direction == pytest.approx((0.6, 0.8))
        # each point lies on the cutting plane, so its projection equals its resultant magnitude (up to sign)
        for point, signed in zip(section.points, section.signed_moments(), strict=True):
            assert abs(signed) == pytest.approx(point.m, abs=1e-6)

    def test_section_peak_matches_the_uniaxial_envelope(self, surface: InteractionSurface, analysis: CrossSectionAnalysis) -> None:
        """The +M_y section boundary peaks at the same order as the exact uniaxial interaction envelope."""
        section_peak = max(section for section in surface.section_resultant(m_y=1.0, m_z=0.0).signed_moments())
        envelope_peak = max(point.m_y for point in analysis.interaction_envelope(axis="y", n_points=10).points)
        assert section_peak == pytest.approx(envelope_peak, rel=0.05)

    def test_section_skips_axial_levels_the_direction_cannot_reach(self, surface: InteractionSurface) -> None:
        """Along +M_z the near-pole rings are offset off the M_z axis, so those levels are skipped."""
        full = surface.section_resultant(m_y=1.0, m_z=0.0, n_levels=48)
        skipped = surface.section_resultant(m_y=0.0, m_z=1.0, n_levels=48)
        assert len(skipped.points) < len(full.points)  # some axial levels dropped
        assert skipped.points[0] == skipped.points[-1]  # still a closed loop

    def test_zero_direction_raises(self, surface: InteractionSurface) -> None:
        """A section without a moment direction (both components zero) raises a clear error."""
        with pytest.raises(ValueError, match="moment direction is undefined"):
            surface.section_resultant(m_y=0.0, m_z=0.0)

    def test_direction_that_never_intersects_raises(self) -> None:
        """A direction that misses every ring raises rather than returning an empty section."""
        # a degenerate surface whose rings all sit on the +M_y axis, well away from the M_z axis
        points = (
            InteractionPoint(n=-100.0, m_y=1000.0, m_z=0.0, m=1000.0),
            InteractionPoint(n=100.0, m_y=1000.0, m_z=0.0, m=1000.0),
        )
        meridian = MomentInteractionResult(theta=0.0, points=points, raw=None)
        surface = InteractionSurface(thetas=(0.0, 180.0), meridians=(meridian, meridian), raw=None)
        with pytest.raises(ValueError, match="does not intersect the interaction surface"):
            surface.section_resultant(m_y=0.0, m_z=1.0)

    def test_plot_returns_figure_with_resultant_axes(self, surface: InteractionSurface) -> None:
        """plot() returns a figure with the N-M resultant axes and the direction in the title."""
        figure = surface.section_resultant(m_y=1.0, m_z=0.0).plot()
        try:
            assert isinstance(figure, Figure)
            (ax,) = figure.axes
            assert "M" in ax.get_xlabel()
            assert "N" in ax.get_ylabel()
            assert "resultant section" in ax.get_title()
            assert ax.get_ylim()[0] > ax.get_ylim()[1]  # compression (negative) drawn on top
        finally:
            plt.close(figure)


class TestComponentSections:
    """Fixed-component N-M_y and N-M_z sections, sliced at a constant transverse moment."""

    def test_n_my_is_closed_and_signed(self, surface: InteractionSurface) -> None:
        """The N-M_y section through the symmetry plane closes and spans a sagging and a hogging side."""
        section = surface.section_n_my(m_z=0.0)
        assert section.kind == "n_my"
        assert section.points[0] == section.points[-1]
        signed = section.signed_moments()
        assert signed == [point.m_y for point in section.points]  # the plotted moment is M_y itself
        assert max(signed) > 0
        assert min(signed) < 0

    def test_n_my_narrows_with_transverse_moment(self, surface: InteractionSurface) -> None:
        """A non-zero fixed M_z narrows the N-M_y section (less M_y capacity left)."""
        wide = max(surface.section_n_my(m_z=0.0).signed_moments())
        narrow = max(surface.section_n_my(m_z=40.0).signed_moments())
        assert narrow < wide

    def test_n_mz_is_closed_and_skips_unreached_levels(self, surface: InteractionSurface) -> None:
        """The N-M_z section at a fixed M_y closes and skips axial levels its plane cannot reach."""
        section = surface.section_n_mz(m_y=200.0, n_levels=48)
        assert section.kind == "n_mz"
        assert section.points[0] == section.points[-1]
        signed = section.signed_moments()
        assert signed == [point.m_z for point in section.points]  # the plotted moment is M_z itself
        assert max(signed) > 0
        assert min(signed) < 0
        assert len(section.points) < 2 * 48 + 1  # some levels were dropped (plane beyond the near-pole rings)

    def test_plot_labels_follow_the_cut_kind(self, surface: InteractionSurface) -> None:
        """The N-M_y and N-M_z plots label their moment axis and name the fixed component."""
        my_figure = surface.section_n_my(m_z=0.0).plot()
        mz_figure = surface.section_n_mz(m_y=200.0).plot()
        try:
            (my_ax,) = my_figure.axes
            (mz_ax,) = mz_figure.axes
            assert "M_{y,Rd}" in my_ax.get_xlabel()
            assert "M_z$ = 0" in my_ax.get_title()
            assert "M_{z,Rd}" in mz_ax.get_xlabel()
            assert "M_y$ = 200" in mz_ax.get_title()
        finally:
            plt.close(my_figure)
            plt.close(mz_figure)
