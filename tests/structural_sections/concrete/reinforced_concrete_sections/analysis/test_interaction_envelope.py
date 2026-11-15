"""Tests for the closed uniaxial N-M interaction envelope (behaviour, stitching, plot and error paths).

The envelope stitches the two branches of :meth:`CrossSectionAnalysis.interaction`, so these tests use a
coarse diagram for speed; the numerical anchors of the underlying branches live in ``test_benchmarks.py``.
"""

import matplotlib as mpl
import pytest

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, MomentInteractionEnvelope
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection


def _analysis() -> CrossSectionAnalysis:
    """Reference 300 x 600 C30/37 section with only bottom reinforcement (asymmetric capacities)."""
    cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


class TestInteractionEnvelope:
    """Structure of the closed interaction envelope."""

    def test_returns_closed_envelope_about_y(self) -> None:
        """The y-axis envelope is a closed loop spanning compression to tension."""
        result = _analysis().interaction_envelope(n_points=6)
        assert isinstance(result, MomentInteractionEnvelope)
        assert result.axis == "y"
        assert result.points[0] == result.points[-1]  # closed loop
        forces = [point.n for point in result.points]
        assert min(forces) < 0  # squash (compression) side
        assert max(forces) > 0  # tension side

    def test_loop_carries_both_moment_signs(self) -> None:
        """The stitched loop spans a positive (sagging) and a negative (hogging) moment side."""
        result = _analysis().interaction_envelope(n_points=6)
        moments = [point.m_y for point in result.points]
        assert max(moments) > 0  # sagging branch
        assert min(moments) < 0  # hogging branch

    def test_asymmetric_section_has_larger_sagging_than_hogging(self) -> None:
        """With only bottom steel the positive moment capacity exceeds the negative one in magnitude."""
        result = _analysis().interaction_envelope(n_points=6)
        moments = [point.m_y for point in result.points]
        assert max(moments) > abs(min(moments))

    def test_envelope_about_z_spans_both_signs_of_m_z(self) -> None:
        """The z-axis envelope spreads along m_z, closing on both the positive and negative side."""
        result = _analysis().interaction_envelope(axis="z", n_points=6)
        assert result.axis == "z"
        moments = [point.m_z for point in result.points]
        assert max(moments) > 0
        assert min(moments) < 0

    def test_plot_returns_figure_with_signed_axis_label(self) -> None:
        """plot() returns a figure whose x-axis names the signed moment component of the envelope axis."""
        figure = _analysis().interaction_envelope(n_points=6).plot()
        try:
            assert isinstance(figure, Figure)
            (ax,) = figure.axes
            assert "M_{y,Rd}" in ax.get_xlabel()
            assert "N" in ax.get_ylabel()
            assert ax.get_ylim()[0] > ax.get_ylim()[1]  # compression (negative) drawn on top
        finally:
            plt.close(figure)

    def test_plot_about_z_labels_the_z_component(self) -> None:
        """The z-axis envelope plot labels its x-axis with the m_z component."""
        figure = _analysis().interaction_envelope(axis="z", n_points=6).plot()
        try:
            (ax,) = figure.axes
            assert "M_{z,Rd}" in ax.get_xlabel()
        finally:
            plt.close(figure)


class TestErrorPaths:
    """Clear errors for an unsupported axis and a missing reinforcement layout."""

    def test_invalid_axis_raises(self) -> None:
        """An axis other than 'y' or 'z' raises a clear error before any analysis runs."""
        with pytest.raises(ValueError, match="axis must be 'y' or 'z'"):
            _analysis().interaction_envelope(axis="x")  # type: ignore[arg-type]

    def test_without_rebars_raises(self) -> None:
        """An envelope without longitudinal reinforcement raises the interaction error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="Interaction analysis requires at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).interaction_envelope()
