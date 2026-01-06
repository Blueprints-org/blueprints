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
