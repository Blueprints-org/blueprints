"""Test the SteelCrossSection class."""

from unittest.mock import Mock

from blueprints.structural_sections.steel.steel_cross_sections.steel_cross_section import SteelCrossSection


def test_name(steel_cross_section: SteelCrossSection, mock_cross_section: Mock) -> None:
    """Test that the SteelCrossSection name matches the mock cross-section name."""
    assert steel_cross_section.cross_section.name == mock_cross_section.name


def test_area(steel_cross_section: SteelCrossSection, mock_cross_section: Mock) -> None:
    """Test that the SteelCrossSection area matches the mock cross-section area."""
    assert steel_cross_section.cross_section.area == mock_cross_section.area


def test_perimeter(steel_cross_section: SteelCrossSection, mock_cross_section: Mock) -> None:
    """Test that the SteelCrossSection perimeter matches the mock cross-section perimeter."""
    assert steel_cross_section.cross_section.perimeter == mock_cross_section.perimeter


def test_centroid(steel_cross_section: SteelCrossSection, mock_cross_section: Mock) -> None:
    """Test that the SteelCrossSection centroid matches the mock cross-section centroid."""
    assert steel_cross_section.cross_section.centroid == mock_cross_section.centroid


def test_weight_per_meter(steel_cross_section: SteelCrossSection, mock_cross_section: Mock, mock_material: Mock) -> None:
    """Test that the SteelCrossSection weight per meter is calculated correctly."""
    expected_weight: float = mock_material.density * (mock_cross_section.area * 1e-6)
    assert steel_cross_section.weight_per_meter == expected_weight
