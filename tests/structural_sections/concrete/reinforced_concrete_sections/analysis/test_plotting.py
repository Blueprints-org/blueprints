"""Tests for the strain/stress-over-height plotting, using the real backend where a result is needed.

Figures are hard to assert on pixel-by-pixel, so these check the structure (a three-panel figure) and
the projection/law helpers that decide what is drawn. The matplotlib Agg backend keeps it headless.
"""

from collections.abc import Callable

import matplotlib as mpl
import numpy as np
import pytest
from shapely import Polygon

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.plotting import (
    _concrete_stress,
    _draw_neutral_axis,
    _draw_stress,
    _projection_axes,
    _shade_compression_zone,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import StrainPlane, StressStrainResult
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces


def _analysis() -> CrossSectionAnalysis:
    """Reference 300 x 600 C30/37 section with tension and compression reinforcement."""
    cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, material=ReinforcementSteelMaterial(), edge="lower", cover=50)
    cs.add_longitudinal_reinforcement_by_quantity(n=3, diameter=16, material=ReinforcementSteelMaterial(), edge="upper", cover=70)
    return CrossSectionAnalysis(cs)


class TestPlotStructure:
    """The public plot() produces a three-panel figure for every supported regime."""

    @pytest.mark.parametrize(
        "result_factory",
        [
            pytest.param(lambda a: a.cracked_stress(SectionForces(m_y=200)), id="cracked_uniaxial"),
            pytest.param(lambda a: a.uncracked_stress(SectionForces(m_y=-100)), id="uncracked_hogging"),
            pytest.param(lambda a: a.uncracked_stress(SectionForces(m_y=60, m_z=40)), id="uncracked_biaxial"),
            pytest.param(lambda a: a.uncracked_stress(SectionForces(n=-1500)), id="pure_axial"),
        ],
    )
    def test_plot_returns_three_panel_figure(self, result_factory: Callable[[CrossSectionAnalysis], StressStrainResult]) -> None:
        """plot() returns a matplotlib Figure with the section, strain and stress panels."""
        result = result_factory(_analysis())
        figure = result.plot()
        try:
            assert isinstance(figure, Figure)
            titled = [ax.get_title() for ax in figure.axes if ax.get_title()]  # skip the steel twin axis (no title)
            assert titled == ["section", f"{chr(0x03B5)} [{chr(0x2030)}]", f"{chr(0x03C3)} [MPa]"]
        finally:
            plt.close(figure)

    def test_pure_axial_has_no_neutral_axis_line(self) -> None:
        """A pure-axial result has a uniform strain sign, so no neutral-axis line is drawn."""
        figure = _analysis().uncracked_stress(SectionForces(n=-1500)).plot()
        try:
            green_lines = [line for ax in figure.axes for line in ax.get_lines() if line.get_color() == "green"]
            assert green_lines == []
        finally:
            plt.close(figure)

    def test_bending_draws_a_neutral_axis_line_on_every_panel(self) -> None:
        """A bending result crosses zero strain, so a neutral-axis line appears on all three panels."""
        figure = _analysis().cracked_stress(SectionForces(m_y=200)).plot()
        try:
            green_lines = [line for ax in figure.axes for line in ax.get_lines() if line.get_color() == "green"]
            assert len(green_lines) == 3
        finally:
            plt.close(figure)

    def test_stress_panel_has_a_separate_steel_axis(self) -> None:
        """Reinforcement stresses get their own twin x-axis so the concrete block stays legible."""
        figure = _analysis().cracked_stress(SectionForces(m_y=200)).plot()
        try:
            assert len(figure.axes) == 4  # section, strain, concrete stress, steel twin
            assert "rebar stress [MPa]" in [ax.get_xlabel() for ax in figure.axes]
        finally:
            plt.close(figure)

    def test_plot_without_elastic_modulus_raises(self) -> None:
        """A result carrying a strain plane and geometry but no elastic modulus cannot be plotted."""
        result = StressStrainResult(
            forces=SectionForces(m_y=100),
            is_cracked=False,
            concrete_stress_min=-1.0,
            concrete_stress_max=1.0,
            rebar_results=[],
            raw=None,
            strain_plane=StrainPlane(eps_0=0.0, kappa_y=-1e-6, kappa_z=0.0, neutral_axis_depth=100.0, neutral_axis_angle=0.0),
            elastic_modulus=0.0,
            geometry=Polygon([(-150, -300), (150, -300), (150, 300), (-150, 300)]),
        )
        with pytest.raises(ValueError, match="elastic modulus"):
            result.plot()


class TestStressPanel:
    """The stress panel draws the concrete block and only adds a steel axis when there are bars."""

    def _plain_result(self) -> StressStrainResult:
        """A result without any reinforcement bars (an unreinforced concrete section)."""
        return StressStrainResult(
            forces=SectionForces(m_y=100),
            is_cracked=False,
            concrete_stress_min=-1.0,
            concrete_stress_max=1.0,
            rebar_results=[],
            raw=None,
        )

    def test_no_rebars_leaves_a_single_axis(self) -> None:
        """With no reinforcement the stress panel keeps a single concrete axis (no steel twin)."""
        _, ax = plt.subplots()
        try:
            _draw_stress(ax, np.array([-1.0, 1.0]), np.array([-300.0, 300.0]), self._plain_result(), np.array([0.0, 1.0]))
            assert ax.figure.axes == [ax]  # no twin axis was added
        finally:
            plt.close("all")


class TestProjectionAxes:
    """The height axis follows the strain gradient and stays oriented upward."""

    def test_uniaxial_gradient_gives_vertical_height_axis(self) -> None:
        """A vertical strain gradient yields a vertical height axis (0, 1)."""
        plane = StrainPlane(eps_0=0.0, kappa_y=-4e-6, kappa_z=0.0, neutral_axis_depth=100.0, neutral_axis_angle=0.0)
        height_axis, across_axis = _projection_axes(plane)
        assert height_axis == pytest.approx([0.0, 1.0])
        assert across_axis == pytest.approx([-1.0, 0.0])

    def test_pure_axial_falls_back_to_vertical(self) -> None:
        """A flat strain plane (no curvature) falls back to the geometric vertical."""
        plane = StrainPlane(eps_0=-0.3, kappa_y=0.0, kappa_z=0.0, neutral_axis_depth=None, neutral_axis_angle=0.0)
        height_axis, _ = _projection_axes(plane)
        assert height_axis == pytest.approx([0.0, 1.0])

    def test_horizontal_gradient_orients_towards_positive_x(self) -> None:
        """A purely horizontal gradient orients the height axis toward +x when its y-component is zero."""
        plane = StrainPlane(eps_0=0.0, kappa_y=0.0, kappa_z=-5e-6, neutral_axis_depth=100.0, neutral_axis_angle=90.0)
        height_axis, _ = _projection_axes(plane)
        assert height_axis == pytest.approx([1.0, 0.0])


class TestConcreteStressLaw:
    """The concrete stress law: linear in service, no tension when cracked."""

    def test_uncracked_keeps_tension(self) -> None:
        """An uncracked section keeps the linear tension branch."""
        stress = _concrete_stress(np.array([-1.0, 1.0]), elastic_modulus=33000, is_cracked=False)
        assert stress == pytest.approx([33000 * -1e-3, 33000 * 1e-3])

    def test_cracked_drops_tension(self) -> None:
        """A cracked section zeros the concrete tension stress but keeps compression."""
        stress = _concrete_stress(np.array([-1.0, 1.0]), elastic_modulus=33000, is_cracked=True)
        assert stress == pytest.approx([33000 * -1e-3, 0.0])


class TestCompressionZone:
    """The section panel hatches the concrete that is in compression (strain < 0)."""

    _across = np.array([-150.0, 150.0, 150.0, -150.0])
    _heights = np.array([-300.0, -300.0, 300.0, 300.0])

    def test_full_tension_draws_no_hatch(self) -> None:
        """A section entirely in tension gets no compression hatch."""
        _, ax = plt.subplots()
        try:
            _shade_compression_zone(ax, self._across, self._heights, strain=np.array([1.0, 2.0]), hs=np.array([-300.0, 300.0]))
            assert len(ax.patches) == 0
        finally:
            plt.close("all")

    def test_full_compression_hatches_whole_section_without_clip(self) -> None:
        """A section entirely in compression is hatched whole, with no clip rectangle."""
        _, ax = plt.subplots()
        try:
            _shade_compression_zone(ax, self._across, self._heights, strain=np.array([-2.0, -1.0]), hs=np.array([-300.0, 300.0]))
            assert len(ax.patches) == 1
        finally:
            plt.close("all")

    def test_partial_compression_hatches_a_single_band(self) -> None:
        """A section with a neutral axis adds one hatched patch, clipped to the compressed band."""
        _, ax = plt.subplots()
        try:
            _shade_compression_zone(ax, self._across, self._heights, strain=np.array([1.0, -1.0]), hs=np.array([-300.0, 300.0]))
            assert len(ax.patches) == 1  # the clip to the compressed band is verified visually
        finally:
            plt.close("all")

    def test_zero_end_fibre_leaves_full_hatch(self) -> None:
        """A zero-strain end fibre leaves the full hatch (no interpolated neutral axis)."""
        _, ax = plt.subplots()
        try:
            _shade_compression_zone(ax, self._across, self._heights, strain=np.array([-1.0, 0.0]), hs=np.array([-300.0, 300.0]))
            assert len(ax.patches) == 1
        finally:
            plt.close("all")


class TestNeutralAxisLine:
    """The neutral-axis helper interpolates the zero-strain height for either gradient orientation."""

    def test_no_crossing_draws_nothing(self) -> None:
        """A strain profile that does not change sign draws no neutral-axis line."""
        _, ax = plt.subplots()
        try:
            _draw_neutral_axis([ax], strain=np.array([-2.0, -1.0]), hs=np.array([0.0, 100.0]))
            assert [line for line in ax.get_lines() if line.get_color() == "green"] == []
        finally:
            plt.close("all")

    @pytest.mark.parametrize(
        ("strain", "expected"),
        [
            (np.array([-1.0, 1.0]), 50.0),  # increasing with height
            (np.array([1.0, -1.0]), 50.0),  # decreasing with height
        ],
    )
    def test_crossing_draws_line_at_zero_strain_height(self, strain: np.ndarray, expected: float) -> None:
        """The neutral-axis line sits at the interpolated zero-strain height, regardless of orientation."""
        _, ax = plt.subplots()
        try:
            _draw_neutral_axis([ax], strain=strain, hs=np.array([0.0, 100.0]))
            green = [line for line in ax.get_lines() if line.get_color() == "green"]
            assert len(green) == 1
            assert green[0].get_ydata()[0] == pytest.approx(expected)
        finally:
            plt.close("all")
