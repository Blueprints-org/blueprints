"""Fixtures for testing steel cross sections."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.structural_sections.steel.profile_definitions.chs_profile import CHSProfile
from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.profile_definitions.lnp_profile import LNPProfile
from blueprints.structural_sections.steel.profile_definitions.rhs_profile import RHSProfile
from blueprints.structural_sections.steel.profile_definitions.strip_profile import StripProfile
from blueprints.structural_sections.steel.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.standard_profiles.lnp import LNP
from blueprints.structural_sections.steel.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.standard_profiles.strip import Strip


@pytest.fixture
def mock_section_properties() -> Generator[MagicMock, None, None]:
    """Fixture to mock section properties with default values."""
    with patch("blueprints.structural_sections.steel.profile_definitions.plotters.general_steel_plotter.Profile.section_properties") as mock:
        mock.return_value = SectionProperties(ixx_c=1.0e6, iyy_c=1.0e6)
        yield mock


@pytest.fixture
def strip_profile() -> StripProfile:
    """Fixture to set up a Strip profile for testing."""
    return Strip.STRIP160x5


@pytest.fixture
def chs_profile() -> CHSProfile:
    """Fixture to set up a CHS profile for testing."""
    return CHS.CHS508x16


@pytest.fixture
def ipe_profile() -> IProfile:
    """Fixture to set up an I-shaped profile for testing."""
    return IPE.IPE100


@pytest.fixture
def h_profile() -> IProfile:
    """Fixture to set up an H-shaped profile for testing."""
    return HEB.HEB360


@pytest.fixture
def rhs_profile() -> RHSProfile:
    """Fixture to set up an RHS profile for testing."""
    return RHS.RHS400x200x16


@pytest.fixture
def lnp_profile() -> LNPProfile:
    """Fixture to set up an LNP profile for testing."""
    return LNP.LNP100x50x6
