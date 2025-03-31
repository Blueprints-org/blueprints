"""Test the SteelElement class."""

from unittest.mock import Mock

import pytest
from shapely.geometry import Point

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.general_cross_section import CrossSection
from blueprints.structural_sections.steel.steel_element import SteelElement


@pytest.fixture
def mock_cross_section(mocker: Mock) -> Mock:
    """Mock a CrossSection object."""
    cross_section: Mock = mocker.Mock(spec=CrossSection)
    cross_section.name = "MockSection"
    cross_section.area = 683  # mm²
    cross_section.plate_thickness = 14  # mm
    cross_section.perimeter = 400  # mm
    cross_section.centroid = Point(50, 50)
    cross_section.moment_of_inertia_about_y = 2000  # mm⁴
    cross_section.moment_of_inertia_about_z = 3000  # mm⁴
    cross_section.elastic_section_modulus_about_y_positive = 100  # mm³
    cross_section.elastic_section_modulus_about_y_negative = 90  # mm³
    cross_section.elastic_section_modulus_about_z_positive = 80  # mm³
    cross_section.elastic_section_modulus_about_z_negative = 70  # mm³
    cross_section.plastic_section_modulus_about_y = 60  # mm³
    cross_section.plastic_section_modulus_about_z = 50  # mm³
    cross_section.geometry = {"type": "rectangle", "width": 100, "height": 50}
    cross_section.vertices = [Point(0, 0), Point(100, 0), Point(100, 50), Point(0, 50)]
    cross_section.dotted_mesh.return_value = [(10, 10), (20, 20)]
    return cross_section


@pytest.fixture
def mock_material(mocker: Mock) -> Mock:
    """Mock a SteelMaterial object."""
    material: Mock = mocker.Mock(spec=SteelMaterial)
    material.density = 7850  # kg/m³
    material.yield_strength.return_value = 250  # MPa
    material.ultimate_strength.return_value = 400  # MPa
    return material


@pytest.fixture
def steel_element(mock_cross_section: Mock, mock_material: Mock) -> SteelElement:
    """Create a SteelElement instance using mocked cross-section and material."""
    return SteelElement(cross_section=mock_cross_section, material=mock_material)


def test_name(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement name matches the mock cross-section name."""
    assert steel_element.name == mock_cross_section.name


def test_area(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement area matches the mock cross-section area."""
    assert steel_element.area == mock_cross_section.area


def test_plate_thickness(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement plate thickness matches the mock cross-section plate thickness."""
    assert steel_element.plate_thickness == mock_cross_section.plate_thickness


def test_perimeter(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement perimeter matches the mock cross-section perimeter."""
    assert steel_element.perimeter == mock_cross_section.perimeter


def test_centroid(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement centroid matches the mock cross-section centroid."""
    assert steel_element.centroid == mock_cross_section.centroid


def test_moment_of_inertia_about_y(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement moment of inertia about Y matches the mock cross-section."""
    assert steel_element.moment_of_inertia_about_y == mock_cross_section.moment_of_inertia_about_y


def test_moment_of_inertia_about_z(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement moment of inertia about Z matches the mock cross-section."""
    assert steel_element.moment_of_inertia_about_z == mock_cross_section.moment_of_inertia_about_z


def test_elastic_section_modulus_about_y_positive(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement elastic section modulus about Y+ matches the mock cross-section."""
    assert steel_element.elastic_section_modulus_about_y_positive == mock_cross_section.elastic_section_modulus_about_y_positive


def test_elastic_section_modulus_about_y_negative(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement elastic section modulus about Y- matches the mock cross-section."""
    assert steel_element.elastic_section_modulus_about_y_negative == mock_cross_section.elastic_section_modulus_about_y_negative


def test_elastic_section_modulus_about_z_positive(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement elastic section modulus about Z+ matches the mock cross-section."""
    assert steel_element.elastic_section_modulus_about_z_positive == mock_cross_section.elastic_section_modulus_about_z_positive


def test_elastic_section_modulus_about_z_negative(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement elastic section modulus about Z- matches the mock cross-section."""
    assert steel_element.elastic_section_modulus_about_z_negative == mock_cross_section.elastic_section_modulus_about_z_negative


def test_plastic_section_modulus_about_y(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement plastic section modulus about Y matches the mock cross-section."""
    assert steel_element.plastic_section_modulus_about_y == mock_cross_section.plastic_section_modulus_about_y


def test_plastic_section_modulus_about_z(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement plastic section modulus about Z matches the mock cross-section."""
    assert steel_element.plastic_section_modulus_about_z == mock_cross_section.plastic_section_modulus_about_z


def test_geometry(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement geometry matches the mock cross-section geometry."""
    assert steel_element.geometry == mock_cross_section.geometry


def test_vertices(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement vertices match the mock cross-section vertices."""
    assert steel_element.vertices == mock_cross_section.vertices


def test_dotted_mesh(steel_element: SteelElement, mock_cross_section: Mock) -> None:
    """Test that the SteelElement dotted mesh matches the mock cross-section dotted mesh."""
    assert steel_element.dotted_mesh == mock_cross_section.dotted_mesh.return_value


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


def test_invalid_material_type(mock_cross_section: Mock) -> None:
    """Test that creating a SteelElement with an invalid material type raises a TypeError."""
    with pytest.raises(TypeError):
        SteelElement(cross_section=mock_cross_section, material=mock_material)
