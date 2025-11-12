"""Test the SteelElement class."""

from unittest.mock import Mock

import pytest

from blueprints.structural_sections.steel.steel_element import SteelElement


def test_name(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement name matches the mock cross-section name."""
    assert steel_element.cross_section.name == mock_cross_section.name


def test_area(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement area matches the mock cross-section area."""
    assert steel_element.cross_section.area == mock_cross_section.area


def test_perimeter(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement perimeter matches the mock cross-section perimeter."""
    assert steel_element.cross_section.perimeter == mock_cross_section.perimeter


def test_centroid(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement centroid matches the mock cross-section centroid."""
    assert steel_element.cross_section.centroid == mock_cross_section.centroid


def test_moment_of_inertia_about_y(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement moment of inertia about Y matches the mock cross-section."""
    assert steel_element.cross_section.moment_of_inertia_about_y == mock_cross_section.moment_of_inertia_about_y


def test_moment_of_inertia_about_z(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement moment of inertia about Z matches the mock cross-section."""
    assert steel_element.cross_section.moment_of_inertia_about_z == mock_cross_section.moment_of_inertia_about_z


def test_elastic_section_modulus_about_y_positive(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement elastic section modulus about Y+ matches the mock cross-section."""
    assert steel_element.cross_section.elastic_section_modulus_about_y_positive == mock_cross_section.elastic_section_modulus_about_y_positive


def test_elastic_section_modulus_about_y_negative(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement elastic section modulus about Y- matches the mock cross-section."""
    assert steel_element.cross_section.elastic_section_modulus_about_y_negative == mock_cross_section.elastic_section_modulus_about_y_negative


def test_elastic_section_modulus_about_z_positive(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement elastic section modulus about Z+ matches the mock cross-section."""
    assert steel_element.cross_section.elastic_section_modulus_about_z_positive == mock_cross_section.elastic_section_modulus_about_z_positive


def test_elastic_section_modulus_about_z_negative(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement elastic section modulus about Z- matches the mock cross-section."""
    assert steel_element.cross_section.elastic_section_modulus_about_z_negative == mock_cross_section.elastic_section_modulus_about_z_negative


def test_plastic_section_modulus_about_y(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement plastic section modulus about Y matches the mock cross-section."""
    assert steel_element.cross_section.plastic_section_modulus_about_y == mock_cross_section.plastic_section_modulus_about_y


def test_plastic_section_modulus_about_z(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement plastic section modulus about Z matches the mock cross-section."""
    assert steel_element.cross_section.plastic_section_modulus_about_z == mock_cross_section.plastic_section_modulus_about_z


def test_weight_per_meter(steel_element: SteelElement, mock_cross_section: Mock, mock_material: Mock) -> None:
    """Test that the SteelElement weight per meter is calculated correctly."""
    expected_weight: float = mock_material.density * (mock_cross_section.area * 1e-6)
    assert steel_element.weight_per_meter == expected_weight


def test_yield_strength(steel_element: SteelElement, mock_material: Mock) -> None:
    """Test that the SteelElement yield strength matches the mock material yield strength."""
    assert steel_element.yield_strength == mock_material.yield_strength.return_value


def test_ultimate_strength(steel_element: SteelElement, mock_material: Mock) -> None:
    """Test that the SteelElement ultimate strength matches the mock material ultimate strength."""
    assert steel_element.ultimate_strength == mock_material.ultimate_strength.return_value


def test_invalid_yield_strength(steel_element: SteelElement, mock_material: Mock) -> None:
    """Test that accessing yield strength raises a ValueError if not defined."""
    mock_material.yield_strength.return_value = None
    with pytest.raises(ValueError, match=r"Yield strength is not defined for this material."):
        _ = steel_element.yield_strength


def test_invalid_ultimate_strength(steel_element: SteelElement, mock_material: Mock) -> None:
    """Test that accessing ultimate strength raises a ValueError if not defined."""
    mock_material.ultimate_strength.return_value = None
    with pytest.raises(ValueError, match=r"Ultimate strength is not defined for this material."):
        _ = steel_element.ultimate_strength
