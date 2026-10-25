"""Tests for the ULS verification diagram: the unity check drawn on the capacity section.

The capacity marker comes from the exact unity check, so these tests pin the numbers against ``verify``
and check the plot structure (markers, utilization in the title) on a coarse surface for speed.
"""

import matplotlib as mpl
import pytest

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

pytest.importorskip("concreteproperties")

from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis import CrossSectionAnalysis, VerificationDiagram
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces


def _analysis() -> CrossSectionAnalysis:
    """Reference 300 x 600 C30/37 section with only bottom reinforcement."""
    cs = RectangularReinforcedCrossSection(width=300, height=600, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
    cs.add_longitudinal_reinforcement_by_quantity(n=4, diameter=25, material=ReinforcementSteelMaterial(), edge="lower")
    return CrossSectionAnalysis(cs)


class TestVerificationDiagram:
    """The verification diagram carries the exact unity check on a resultant capacity section."""

    def test_carries_the_exact_unity_check(self) -> None:
        """The diagram's utilization equals the exact verify() result for the same action."""
        analysis = _analysis()
        forces = SectionForces(n=0.0, m_y=200.0)
        diagram = analysis.verification_diagram(forces, n_theta=12, n_points=8)
        assert isinstance(diagram, VerificationDiagram)
        assert diagram.section.kind == "resultant"
        assert diagram.utilization.utilization == pytest.approx(analysis.verify(forces).utilization)
        assert diagram.utilization.m_ed == pytest.approx(200.0)
        assert diagram.utilization.is_ok

    def test_plot_marks_action_and_capacity_with_the_utilization(self) -> None:
        """plot() marks M_Ed and M_Rd and states the passing unity check in the title."""
        figure = _analysis().verification_diagram(SectionForces(n=0.0, m_y=200.0), n_theta=12, n_points=8).plot()
        try:
            assert isinstance(figure, Figure)
            (ax,) = figure.axes
            labels = [text.get_text() for text in ax.get_legend().get_texts()]
            assert any("M_{Ed}" in label for label in labels)
            assert any("M_{Rd}" in label for label in labels)
            assert "unity check" in ax.get_title()
            assert "OK" in ax.get_title()
            assert ax.get_ylim()[0] > ax.get_ylim()[1]  # compression (negative) drawn on top
        finally:
            plt.close(figure)

    def test_exceeded_action_is_reported_in_the_title(self) -> None:
        """A design moment beyond the capacity gives a utilization above one and an 'exceeded' title."""
        diagram = _analysis().verification_diagram(SectionForces(n=0.0, m_y=1000.0), n_theta=12, n_points=8)
        assert not diagram.utilization.is_ok
        figure = diagram.plot()
        try:
            (ax,) = figure.axes
            assert "exceeded" in ax.get_title()
        finally:
            plt.close(figure)

    def test_pure_axial_action_raises(self) -> None:
        """A pure axial action has no moment section to draw, so the diagram raises."""
        with pytest.raises(ValueError, match="needs a bending design action"):
            _analysis().verification_diagram(SectionForces(n=-500.0))

    def test_without_rebars_raises(self) -> None:
        """A verification diagram without longitudinal reinforcement raises via the unity check."""
        cs = RectangularReinforcedCrossSection(width=300, height=500, concrete_material=ConcreteMaterial(ConcreteStrengthClass.C30_37))
        with pytest.raises(ValueError, match="Verification requires at least one longitudinal rebar"):
            CrossSectionAnalysis(cs).verification_diagram(SectionForces(m_y=100.0))
