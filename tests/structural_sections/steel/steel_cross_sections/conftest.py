"""Fixtures for testing steel cross sections."""

from collections.abc import Generator
from unittest.mock import MagicMock, Mock, patch

import pytest
from sectionproperties.post.post import SectionProperties
from shapely.geometry import Point

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections._cross_section import CrossSection
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSProfile
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import IProfile
from blueprints.structural_sections.steel.steel_cross_sections.lnp_profile import LNPProfile
from blueprints.structural_sections.steel.steel_cross_sections.rhs_profile import RHSProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.lnp import LNP
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_cross_sections.steel_cross_section import SteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import StripProfile


@pytest.fixture
def mock_section_properties() -> Generator[MagicMock, None, None]:
    """Fixture to mock section properties with default values."""
    with patch("blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter.CrossSection.section_properties") as mock:
        mock.return_value = SectionProperties(ixx_c=1.0e6, iyy_c=1.0e6)
        yield mock


@pytest.fixture
def strip_profile() -> StripProfile:
    """Fixture to set up a Strip profile for testing."""
    profile = Strip.STRIP160x5
    return StripProfile.from_standard_profile(profile=profile)


@pytest.fixture
def chs_profile() -> CHSProfile:
    """Fixture to set up a CHS profile for testing."""
    profile: CHS = CHS.CHS508x16
    return CHSProfile.from_standard_profile(profile=profile)


@pytest.fixture
def ipe_profile() -> IProfile:
    """Fixture to set up an I-shaped profile for testing."""
    profile = IPE.IPE100
    return IProfile.from_standard_profile(profile=profile)


@pytest.fixture
def h_profile() -> IProfile:
    """Fixture to set up an H-shaped profile for testing."""
    profile = HEB.HEB360
    return IProfile.from_standard_profile(profile=profile)


@pytest.fixture
def rhs_profile() -> RHSProfile:
    """Fixture to set up an RHS profile for testing."""
    profile = RHS.RHS400x200_16
    return RHSProfile.from_standard_profile(profile=profile)


@pytest.fixture
def lnp_profile() -> LNPProfile:
    """Fixture to set up an LNP profile for testing."""
    profile = LNP.LNP_100x50x6
    return LNPProfile.from_standard_profile(
        profile=profile,
        corrosion=0,
    )


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
def steel_cross_section(mock_cross_section: Mock, mock_material: Mock) -> SteelCrossSection:
    """Create a CrossSection instance using mocked cross-section and material."""
    return SteelCrossSection(cross_section=mock_cross_section, material=mock_material)
