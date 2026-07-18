"""Tests for the biaxial M_y-M_z interaction envelope (behaviour, plot and error paths)."""

import matplotlib as mpl
import pytest

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

pytest.importorskip("concreteproperties")

from concreteproperties.utils import AnalysisError

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import BiaxialInteractionResult, CrossSectionAnalysis
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import AnalysisLevel
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection


def _square_symmetric_analysis() -> CrossSectionAnalysis:
    """400 x 400 C30/37 with one D25 in each corner (fully symmetric)."""
    cs = RectangularReinforcedCrossSection(width=400, height=400, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    for x in (-150, 150):
        for y in (-150, 150):
            cs.add_longitudinal_rebar(Rebar(diameter=25, x=x, y=y, material=ReinforcementSteelMaterial()))
    return CrossSectionAnalysis(cs)


class TestBiaxialEnvelope:
    """Structure and symmetry of the biaxial envelope."""

    def test_envelope_is_closed_and_echoes_n(self) -> None:
        """The envelope is a closed polygon (first point repeated) at the requested axial force."""
        result = _square_symmetric_analysis().biaxial_interaction(n=-500.0, n_points=8)
        assert isinstance(result, BiaxialInteractionResult)
        assert result.n == -500.0
        assert len(result.points) == 9  # 8 angles + closing point
        assert result.points[0].m_y == pytest.approx(result.points[-1].m_y)
        assert result.points[0].m_z == pytest.approx(result.points[-1].m_z)

    def test_symmetric_section_gives_symmetric_envelope(self) -> None:
        """A doubly symmetric section yields an envelope symmetric in m_y and m_z."""
        result = _square_symmetric_analysis().biaxial_interaction(n_points=8)
        max_m_y = max(point.m_y for point in result.points)
        min_m_y = min(point.m_y for point in result.points)
        max_m_z = max(point.m_z for point in result.points)
        assert max_m_y == pytest.approx(-min_m_y, rel=1e-2)
        assert max_m_y == pytest.approx(max_m_z, rel=1e-2)

    def test_envelope_peak_matches_uniaxial_capacity(self) -> None:
        """The envelope contains the uniaxial sagging capacity (the theta=0 sample)."""
        analysis = _square_symmetric_analysis()
        capacity = analysis.bending_capacity()
        result = analysis.biaxial_interaction(n_points=8)
        max_m_y = max(point.m_y for point in result.points)
        assert max_m_y == pytest.approx(capacity.m_y_rd, rel=1e-3)

    def test_plot_returns_figure(self) -> None:
        """plot() returns a matplotlib figure with the M_y-M_z axes."""
        figure = _square_symmetric_analysis().biaxial_interaction(n_points=8).plot()
        try:
            assert isinstance(figure, Figure)
            (ax,) = figure.axes
            assert "M_{y,Rd}" in ax.get_xlabel()
            assert "M_{z,Rd}" in ax.get_ylabel()
        finally:
            plt.close(figure)


class TestErrorPaths:
    """Clear errors for unsupported inputs and solver failures."""

    def test_without_rebars_raises(self) -> None:
        """A biaxial interaction analysis without longitudinal reinforcement raises a clear error."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="Biaxial interaction analysis requires at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).biaxial_interaction()

    def test_non_convergence_is_wrapped(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A backend AnalysisError is re-raised as a clear ValueError with context."""
        analysis = _square_symmetric_analysis()
        section = analysis._backend_section(AnalysisLevel.ULS)  # noqa: SLF001 — exercising the cached backend section

        def failing_diagram(*_args: object, **_kwargs: object) -> object:
            raise AnalysisError("equilibrium not found")

        monkeypatch.setattr(section, "biaxial_bending_diagram", failing_diagram)
        with pytest.raises(ValueError, match="did not converge"):
            analysis.biaxial_interaction()
