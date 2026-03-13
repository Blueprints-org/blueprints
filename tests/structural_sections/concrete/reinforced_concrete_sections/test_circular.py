"""Tests for Circular Reinforced Concrete Sections."""

import matplotlib as mpl

mpl.use("Agg")

import pytest
from matplotlib import pyplot as plt
from shapely import LineString, Polygon

from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.circular import CircularReinforcedCrossSection
from blueprints.structural_sections.concrete.reinforced_concrete_sections.reinforcement_configurations import ReinforcementByQuantity
from blueprints.structural_sections.concrete.stirrups import StirrupConfiguration


class TestCircularReinforcedCrossSection:
    """Tests for the CircularReinforcedCrossSection class."""

    def test_add_stirrup_along_perimeter(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the add_stirrup_along_perimeter method."""
        stirrup = circular_reinforced_cross_section.add_stirrup_along_perimeter(
            diameter=12,
            distance=150,
            material=circular_reinforced_cross_section.get_present_steel_materials()[0],
        )
        assert stirrup in circular_reinforced_cross_section.stirrups

    def test_add_longitudinal_reinforcement_by_quantity(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the add_longitudinal_reinforcement_by_quantity method."""
        assert len(circular_reinforced_cross_section.longitudinal_rebars) == 7

    def test_plot(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the plot method."""
        plot = circular_reinforced_cross_section.plot(show=False, center_line_style={"linewidth": 0.85})
        assert isinstance(plot, plt.Figure)

    def test_reinforcement_weight_longitudinal_bars(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the reinforcement_weight_longitudinal_bars method."""
        expected_weight = 14.98802804  # kg/m
        assert circular_reinforced_cross_section.reinforcement_weight_longitudinal_bars == pytest.approx(expected=expected_weight, rel=1e-2)

    def test_reinforcement_weight_stirrups(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the reinforcement_weight_stirrups method."""
        expected_weight = 22.96448757  # kg/m
        assert circular_reinforced_cross_section.reinforcement_weight_stirrups == pytest.approx(expected=expected_weight, rel=1e-3)

    def test_reinforcement_weight(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the reinforcement_weight method."""
        expected_weight = 37.95251561  # kg/m
        assert circular_reinforced_cross_section.reinforcement_weight == pytest.approx(expected=expected_weight, rel=1e-3)

    def test_reinforcement_area_longitudinal_bars(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the reinforcement_area_longitudinal_bars method."""
        expected_area = 1909.302935  # mm²/m
        assert circular_reinforced_cross_section.reinforcement_area_longitudinal_bars == pytest.approx(expected=expected_area, rel=1e-2)

    def test_concrete_volume(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the concrete_volume method."""
        expected_volume = 0.125663706  # m³/m
        assert circular_reinforced_cross_section.concrete_volume == pytest.approx(expected=expected_volume, rel=1e-2)

    def test_weight_per_volume(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the weight_per_volume method."""
        expected_weight_per_volume = 302.0165231  # kg/m³
        assert circular_reinforced_cross_section.weight_per_volume == pytest.approx(expected=expected_weight_per_volume, rel=1e-2)

    def test_add_longitudinal_rebar_wrong_position(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the add_longitudinal_rebar method with wrong position."""
        with pytest.raises(ValueError):
            circular_reinforced_cross_section.add_longitudinal_rebar(
                rebar=Rebar(
                    diameter=12,
                    x=2500,
                    y=1000,
                    material=circular_reinforced_cross_section.get_present_steel_materials()[0],
                )
            )

    def test_add_stirrup_configuration_wrong_position(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the add_stirrup_configuration method with wrong position."""
        with pytest.raises(ValueError):
            circular_reinforced_cross_section.add_stirrup_configuration(
                stirrup=StirrupConfiguration(
                    geometry=Polygon([(0, 0), (0, 100), (5000, 5000), (100, 0)]),
                    diameter=8,
                    distance=150,
                    material=circular_reinforced_cross_section.get_present_steel_materials()[0],
                ),
            )

    def test_add_reinforcement_configuration_by_linestring(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the add_reinforcement_configuration method with a linestring."""
        linestring = LineString([(-100, 100), (100, 0)])
        circular_reinforced_cross_section.add_reinforcement_configuration(
            line=linestring,
            configuration=ReinforcementByQuantity(
                diameter=12,
                n=7,
                material=circular_reinforced_cross_section.get_present_steel_materials()[0],
            ),
        )
        assert len(circular_reinforced_cross_section.longitudinal_rebars) == 14

    def test_rebar_not_in_cross_section(self, circular_reinforced_cross_section: CircularReinforcedCrossSection) -> None:
        """Test the add_longitudinal_rebar method with a rebar not in the cross-section."""
        rebar = Rebar(
            diameter=12,
            x=2500,
            y=1000,
            material=circular_reinforced_cross_section.get_present_steel_materials()[0],
        )
        circular_reinforced_cross_section._single_longitudinal_rebars.append(rebar)  # noqa: SLF001
        with pytest.raises(ValueError):
            _ = circular_reinforced_cross_section.longitudinal_rebars

    def test_plot_without_longitudinal_reinforcement(self, circular_cross_section_no_reinforcement: CircularReinforcedCrossSection) -> None:
        """Test the plot method for cross-section without longitudinal reinforcement."""
        plot = circular_cross_section_no_reinforcement.plot(show=False, center_line_style={"linewidth": 0.85})
        assert isinstance(plot, plt.Figure)

        # Test that get_present_steel_materials returns empty list
        steel_materials = circular_cross_section_no_reinforcement.get_present_steel_materials()
        assert steel_materials == []
