"""Test the SteelCrossSection class."""

import pytest
from shapely.geometry import Point

from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestSteelCrossSection:
    """Test suite for the SteelCrossSection class."""

    def test_name(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection name works correctly."""
        assert steel_cross_section.profile.name == "IPE100"

    def test_area(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection area works correctly."""
        assert steel_cross_section.profile.area == pytest.approx(1032.6, 1e-3)

    def test_perimeter(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection perimeter works correctly."""
        assert steel_cross_section.profile.perimeter == pytest.approx(399.762, 1e-3)

    def test_centroid(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection centroid works correctly."""
        assert steel_cross_section.profile.centroid.equals_exact(Point(0.0, 0.0), 1e-3)

    def test_yield_strength(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection yield strength is calculated correctly."""
        expected_yield_strength: float = 275.0  # MPa for S275 steel
        assert steel_cross_section.yield_strength == pytest.approx(expected_yield_strength, 1e-3)

    def test_ultimate_strength(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection ultimate strength is calculated correctly."""
        expected_ultimate_strength: float = 430.0  # MPa for S275 steel
        assert steel_cross_section.ultimate_strength == pytest.approx(expected_ultimate_strength, 1e-3)

    def test_weight_per_meter(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection weight per meter is calculated correctly."""
        expected_weight: float = steel_cross_section.profile.area * steel_cross_section.material.density * 1e-6
        assert steel_cross_section.weight_per_meter == pytest.approx(expected_weight, 1e-3)
