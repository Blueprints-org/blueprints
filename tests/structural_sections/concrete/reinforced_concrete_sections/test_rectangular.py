"""Tests for Rectangular Reinforced Concrete Sections."""

import matplotlib as mpl

mpl.use("Agg")

from typing import Literal

import pytest
from matplotlib import pyplot as plt
from shapely import LineString, Polygon

from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.rectangular import RectangularReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import ReinforcementByQuantity
from blueprints.structural_sections.concrete.stirrups import StirrupConfiguration


class TestRectangularReinforcedCrossSection:
    """Tests for the RectangularReinforcedCrossSection class."""

    def test_add_stirrup_along_edges(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the add_stirrup_along_edges method."""
        stirrup = rectangular_reinforced_cross_section.add_stirrup_along_edges(
            diameter=8,
            distance=150,
            material=rectangular_reinforced_cross_section.get_present_steel_materials()[0],
        )
        assert stirrup in rectangular_reinforced_cross_section.stirrups

    def test_add_stirrup_in_center(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the add_stirrup_in_center method."""
        stirrup = rectangular_reinforced_cross_section.add_stirrup_in_center(
            width=200,
            diameter=8,
            distance=150,
            material=rectangular_reinforced_cross_section.get_present_steel_materials()[0],
        )
        assert stirrup in rectangular_reinforced_cross_section.stirrups

    @pytest.mark.parametrize(
        "edge",
        [
            "upper",
            "right",
            "lower",
            "left",
        ],
    )
    def test_add_longitudinal_reinforcement_by_quantity(
        self,
        rectangular_reinforced_cross_section: RectangularReinforcedCrossSection,
        edge: Literal["upper", "right", "lower", "left"],
    ) -> None:
        """Test the add_longitudinal_reinforcement_by_quantity method."""
        rectangular_reinforced_cross_section.add_longitudinal_reinforcement_by_quantity(
            n=5,
            diameter=14,
            material=rectangular_reinforced_cross_section.get_present_steel_materials()[0],
            edge=edge,
            cover=23,
            corner_offset=40,
        )
        assert len(rectangular_reinforced_cross_section.longitudinal_rebars) == 15

    def test_add_longitudinal_reinforcement_by_quantity_wrong_edge(
        self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection
    ) -> None:
        """Test the add_longitudinal_reinforcement_by_quantity method with wrong edge."""
        with pytest.raises(ValueError):
            rectangular_reinforced_cross_section.add_longitudinal_reinforcement_by_quantity(
                n=5,
                diameter=14,
                material=rectangular_reinforced_cross_section.get_present_steel_materials()[0],
                edge="wrong",  # type: ignore[arg-type]
            )

    def test_plot(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the plot method."""
        plot = rectangular_reinforced_cross_section.plot(show=False, center_line_style={"linewidth": 0.85})
        assert isinstance(plot, plt.Figure)

    def test_reinforcement_weight_longitudinal_bars(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the reinforcement_weight_longitudinal_bars method."""
        expected_weight = 46.38828588400884  # kg/m
        assert rectangular_reinforced_cross_section.reinforcement_weight_longitudinal_bars == pytest.approx(expected=expected_weight, rel=1e-2)

    def test_reinforcement_weight_stirrups(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the reinforcement_weight_stirrups method."""
        expected_weight = 18.1087  # kg/m
        assert rectangular_reinforced_cross_section.reinforcement_weight_stirrups == pytest.approx(expected=expected_weight, rel=1e-2)

    def test_reinforcement_weight(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the reinforcement_weight method."""
        expected_weight = 64.4969  # kg/m
        assert rectangular_reinforced_cross_section.reinforcement_weight == pytest.approx(expected=expected_weight, rel=1e-2)

    def test_reinforcement_area_longitudinal_bars(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the reinforcement_area_longitudinal_bars method."""
        expected_area = 5909.3357  # mm²/m
        assert rectangular_reinforced_cross_section.reinforcement_area_longitudinal_bars == pytest.approx(expected=expected_area, rel=1e-2)

    def test_concrete_volume(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the concrete_volume method."""
        expected_volume = 0.8  # m³/m
        assert rectangular_reinforced_cross_section.concrete_volume == pytest.approx(expected=expected_volume, rel=1e-2)

    def test_weight_per_volume(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the weight_per_volume method."""
        expected_weight_per_volume = 80.6211  # kg/m³
        assert rectangular_reinforced_cross_section.weight_per_volume == pytest.approx(expected=expected_weight_per_volume, rel=1e-2)

    def test_add_longitudinal_rebar_wrong_position(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the add_longitudinal_rebar method with wrong position."""
        with pytest.raises(ValueError):
            rectangular_reinforced_cross_section.add_longitudinal_rebar(
                rebar=Rebar(
                    diameter=12,
                    x=2500,
                    y=1000,
                    material=rectangular_reinforced_cross_section.get_present_steel_materials()[0],
                )
            )

    def test_add_stirrup_configuration_wrong_position(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the add_stirrup_configuration method with wrong position."""
        with pytest.raises(ValueError):
            rectangular_reinforced_cross_section.add_stirrup_configuration(
                stirrup=StirrupConfiguration(
                    geometry=Polygon([(0, 0), (0, 100), (5000, 5000), (100, 0)]),
                    diameter=8,
                    distance=150,
                    material=rectangular_reinforced_cross_section.get_present_steel_materials()[0],
                ),
            )

    def test_add_reinforcement_configuration_by_linestring(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the add_reinforcement_configuration method with a linestring."""
        linestring = LineString([(-300, 200), (300, 200)])
        rectangular_reinforced_cross_section.add_reinforcement_configuration(
            line=linestring,
            configuration=ReinforcementByQuantity(
                diameter=12,
                n=3,
                material=rectangular_reinforced_cross_section.get_present_steel_materials()[0],
            ),
        )
        assert len(rectangular_reinforced_cross_section.longitudinal_rebars) == 13

    def test_rebar_not_in_cross_section(self, rectangular_reinforced_cross_section: RectangularReinforcedCrossSection) -> None:
        """Test the add_longitudinal_rebar method with a rebar not in the cross-section."""
        rebar = Rebar(
            diameter=12,
            x=2500,
            y=1000,
            material=rectangular_reinforced_cross_section.get_present_steel_materials()[0],
        )
        rectangular_reinforced_cross_section._single_longitudinal_rebars.append(rebar)  # noqa: SLF001
        with pytest.raises(ValueError):
            _ = rectangular_reinforced_cross_section.longitudinal_rebars

    def test_plot_without_longitudinal_reinforcement(self, rectangular_cross_section_no_reinforcement: RectangularReinforcedCrossSection) -> None:
        """Test the plot method for cross-section without longitudinal reinforcement."""
        plot = rectangular_cross_section_no_reinforcement.plot(show=False, center_line_style={"linewidth": 0.85})
        assert isinstance(plot, plt.Figure)

        # Test that get_present_steel_materials returns empty list
        steel_materials = rectangular_cross_section_no_reinforcement.get_present_steel_materials()
        assert steel_materials == []
