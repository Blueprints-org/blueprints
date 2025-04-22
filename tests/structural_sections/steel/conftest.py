"""Fixtures for steel elements."""

from unittest.mock import Mock

import pytest
from shapely.geometry import Point

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._cross_section import CrossSection
from blueprints.structural_sections.steel.steel_element import SteelElement


@pytest.fixture
def mocker() -> Mock:
    """Provide a mocker instance for mocking objects."""
    return Mock()


@pytest.fixture
def mock_cross_section(mocker: Mock) -> CrossSection:
    """Mock a CrossSection object."""
    cross_section: Mock = mocker.Mock(spec=CrossSection)
    cross_section.name = "MockSection"
    cross_section.area = 683  # mm²
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
    return cross_section


@pytest.fixture
def mock_material(mocker: Mock) -> SteelMaterial:
    """Mock a SteelMaterial object."""
    material: Mock = mocker.Mock(spec=SteelMaterial)
    material.density = 7850  # kg/m³
    material.yield_strength.return_value = 250  # MPa
    material.ultimate_strength.return_value = 400  # MPa
    return material


@pytest.fixture
def steel_element(mock_cross_section: Mock, mock_material: Mock) -> SteelElement:
    """Create a SteelElement instance using mocked cross-section and material."""
    return SteelElement(cross_section=mock_cross_section, material=mock_material, nominal_thickness=10)
