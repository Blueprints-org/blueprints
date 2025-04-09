"""Test the SteelCrossSection class."""

from unittest.mock import Mock

import pytest
from shapely.geometry import Point

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.base import SteelCrossSection
from blueprints.structural_sections.steel.steel_element import SteelElement


@pytest.fixture
def mock_steel_material(mocker: Mock) -> Mock:
    """Mock a SteelMaterial object."""
    material: Mock = mocker.Mock(spec=SteelMaterial)
    material.density = 7850  # kg/m³
    return material


@pytest.fixture
def mock_steel_element(mocker: Mock) -> Mock:
    """Mock a SteelElement object."""
    element: Mock = mocker.Mock(spec=SteelElement)
    element.area = 500  # mm²
    element.centroid = Point(50, 50)
    element.moment_of_inertia_about_y = 2000  # mm⁴
    element.moment_of_inertia_about_z = 3000  # mm⁴
    element.yield_strength = 250  # MPa
    element.cross_section = Mock()
    element.cross_section.geometry.exterior.coords = [Point(0, 0), Point(100, 0), Point(100, 50), Point(0, 50)]
    element.cross_section.area = 500  # mm²
    element.cross_section.centroid = Point(50, 50)
    element.cross_section.moment_of_inertia_about_y = 2000  # mm⁴
    element.cross_section.moment_of_inertia_about_z = 3000  # mm⁴
    element.cross_section.elastic_section_modulus_about_y_positive = 100  # mm³
    element.cross_section.elastic_section_modulus_about_y_negative = 90  # mm³
    element.cross_section.elastic_section_modulus_about_z_positive = 80  # mm³
    element.cross_section.elastic_section_modulus_about_z_negative = 70  # mm³
    element.cross_section.geometry = {"type": "rectangle", "width": 100, "height": 50}
    element.cross_section.name = "MockSection"
    return element


@pytest.fixture
def steel_cross_section(mock_steel_material: Mock, mock_steel_element: Mock) -> SteelCrossSection:
    """Create a SteelCrossSection instance with mocked elements."""
    cross_section = Mock(spec=SteelCrossSection)
    cross_section.steel_material = mock_steel_material
    cross_section.elements = [mock_steel_element, mock_steel_element]
    cross_section.steel_volume_per_meter = 0.001
    cross_section.steel_weight_per_meter = 7.85
    cross_section.steel_area = 1000
    cross_section.centroid = Point(50, 50)
    cross_section.moment_of_inertia_about_y = 4000
    cross_section.moment_of_inertia_about_z = 6000
    cross_section.elastic_section_modulus_about_y_positive = 80
    cross_section.elastic_section_modulus_about_y_negative = 80
    cross_section.elastic_section_modulus_about_z_positive = 120
    cross_section.elastic_section_modulus_about_z_negative = 120
    cross_section.vertices = [[Point(0, 0), Point(100, 0), Point(100, 50), Point(0, 50)], [Point(0, 0), Point(100, 0), Point(100, 50), Point(0, 50)]]
    return cross_section


def test_steel_volume_per_meter(steel_cross_section: SteelCrossSection, mock_steel_element: Mock) -> None:
    """Test the steel volume per meter calculation."""
    expected_volume = 2 * mock_steel_element.area * 1000 * 1e-9  # Convert mm³ to m³
    assert steel_cross_section.steel_volume_per_meter == expected_volume


def test_steel_weight_per_meter(steel_cross_section: SteelCrossSection, mock_steel_material: Mock, mock_steel_element: Mock) -> None:
    """Test the steel weight per meter calculation."""
    expected_weight = mock_steel_material.density * 2 * mock_steel_element.area * 1000 * 1e-9
    assert steel_cross_section.steel_weight_per_meter == pytest.approx(expected_weight)


def test_steel_area(steel_cross_section: SteelCrossSection, mock_steel_element: Mock) -> None:
    """Test the total steel area calculation."""
    expected_area = 2 * mock_steel_element.area
    assert steel_cross_section.steel_area == expected_area


def test_centroid(steel_cross_section: SteelCrossSection) -> None:
    """Test the centroid calculation."""
    expected_centroid = Point(50, 50)
    assert steel_cross_section.centroid == expected_centroid


def test_moment_of_inertia_about_y(steel_cross_section: SteelCrossSection, mock_steel_element: Mock) -> None:
    """Test the moment of inertia about the y-axis calculation."""
    expected_moi_y = 2 * mock_steel_element.moment_of_inertia_about_y
    assert steel_cross_section.moment_of_inertia_about_y == expected_moi_y


def test_moment_of_inertia_about_z(steel_cross_section: SteelCrossSection, mock_steel_element: Mock) -> None:
    """Test the moment of inertia about the z-axis calculation."""
    expected_moi_z = 2 * mock_steel_element.moment_of_inertia_about_z
    assert steel_cross_section.moment_of_inertia_about_z == expected_moi_z


def test_elastic_section_modulus_about_y_positive(steel_cross_section: SteelCrossSection) -> None:
    """Test the elastic section modulus about the y-axis on the positive z side."""
    distance_to_top = 50  # Distance from centroid to top
    expected_modulus = steel_cross_section.moment_of_inertia_about_y / distance_to_top
    assert steel_cross_section.elastic_section_modulus_about_y_positive == expected_modulus


def test_elastic_section_modulus_about_y_negative(steel_cross_section: SteelCrossSection) -> None:
    """Test the elastic section modulus about the y-axis on the negative z side."""
    distance_to_bottom = 50  # Distance from centroid to bottom
    expected_modulus = steel_cross_section.moment_of_inertia_about_y / distance_to_bottom
    assert steel_cross_section.elastic_section_modulus_about_y_negative == expected_modulus


def test_elastic_section_modulus_about_z_positive(steel_cross_section: SteelCrossSection) -> None:
    """Test the elastic section modulus about the z-axis on the positive y side."""
    distance_to_right = 50  # Distance from centroid to right
    expected_modulus = steel_cross_section.moment_of_inertia_about_z / distance_to_right
    assert steel_cross_section.elastic_section_modulus_about_z_positive == expected_modulus


def test_elastic_section_modulus_about_z_negative(steel_cross_section: SteelCrossSection) -> None:
    """Test the elastic section modulus about the z-axis on the negative y side."""
    distance_to_left = 50  # Distance from centroid to left
    expected_modulus = steel_cross_section.moment_of_inertia_about_z / distance_to_left
    assert steel_cross_section.elastic_section_modulus_about_z_negative == expected_modulus
