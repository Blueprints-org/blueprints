"""Tests for the uniaxial N-M interaction diagram (behaviour, plot and error paths).

Numerical anchor points (squash load, tension endpoint, pure-bending consistency) live in
``test_benchmarks.py``; these tests pin the API behaviour with a coarse diagram for speed.
"""

import matplotlib as mpl
import pytest

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

pytest.importorskip("concreteproperties")

from concreteproperties.utils import AnalysisError

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, MomentInteractionResult
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import AnalysisLevel
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection


def _analysis() -> CrossSectionAnalysis:
    cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=20, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


class TestInteractionDiagram:
    """Structure of the uniaxial interaction diagram."""

    def test_returns_points_spanning_compression_to_tension(self) -> None:
        """The diagram spans from a compressive to a tensile axial force."""
        result = _analysis().interaction(n_points=6)
        assert isinstance(result, MomentInteractionResult)
        assert result.theta == 0.0
        forces = [point.n for point in result.points]
        assert min(forces) < 0  # squash (compression) side
        assert max(forces) > 0  # tension side

    def test_moments_are_uniaxial_about_y(self) -> None:
        """For theta=0 every point bends about the y-axis only."""
        result = _analysis().interaction(n_points=6)
        peak = max(point.m for point in result.points)
        for point in result.points:
            assert point.m_z == pytest.approx(0.0, abs=1e-4 * peak)
            assert point.m == pytest.approx(abs(point.m_y))

    def test_control_points_include_requested_count(self) -> None:
        """The diagram carries at least the requested number of points (plus control points)."""
        result = _analysis().interaction(n_points=6)
        assert len(result.points) >= 6

    def test_plot_returns_figure(self) -> None:
        """plot() returns a matplotlib figure with the N-M axes."""
        figure = _analysis().interaction(n_points=6).plot()
        try:
            assert isinstance(figure, Figure)
            (ax,) = figure.axes
            assert "M" in ax.get_xlabel()
            assert "N" in ax.get_ylabel()
        finally:
            plt.close(figure)


class TestErrorPaths:
    """Clear errors for unsupported inputs and solver failures."""

    def test_without_rebars_raises(self) -> None:
        """An interaction analysis without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="Interaction analysis requires at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).interaction()

    def test_non_convergence_is_wrapped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend AnalysisError is re-raised as a clear ValueError with context."""
        analysis = _analysis()
        section = analysis._backend_section(AnalysisLevel.ULS)  # noqa: SLF001 — exercising the cached backend section

        def failing_diagram(*_args: object, **_kwargs: object) -> object:
            raise AnalysisError("equilibrium not found")

        monkeypatch.setattr(section, "moment_interaction_diagram", failing_diagram)
        with pytest.raises(ValueError, match="did not converge"):
            analysis.interaction()
