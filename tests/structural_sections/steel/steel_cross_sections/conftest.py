"""Fixtures for testing steel cross sections."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.lnp_profile import LNPProfile
from blueprints.structural_sections.steel.steel_cross_sections.rhs_profile import RHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.lnp import LNP
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import StripSteelProfile


@pytest.fixture
def mock_section_properties() -> Generator[MagicMock, None, None]:
    """Fixture to mock section properties with default values."""
    with patch(
        "blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter.CombinedSteelCrossSection.section_properties"
    ) as mock:
        mock.return_value = SectionProperties(ixx_c=1.0e6, iyy_c=1.0e6)
        yield mock


@pytest.fixture
def strip_profile() -> StripSteelProfile:
    """Fixture to set up a Strip profile for testing."""
    profile = Strip.STRIP160x5
    steel_class = SteelStrengthClass.S355
    return StripSteelProfile.from_standard_profile(profile=profile, steel_material=SteelMaterial(steel_class))


@pytest.fixture
def chs_profile() -> CHSSteelProfile:
    """Fixture to set up a CHS profile for testing."""
    profile: CHS = CHS.CHS508x16
    steel_class: SteelStrengthClass = SteelStrengthClass.S355
    return CHSSteelProfile.from_standard_profile(profile=profile, steel_material=SteelMaterial(steel_class))


@pytest.fixture
def ipe_profile() -> ISteelProfile:
    """Fixture to set up an I-shaped profile for testing."""
    profile = IPE.IPE100
    steel_class = SteelStrengthClass.S355
    return ISteelProfile.from_standard_profile(profile=profile, steel_material=SteelMaterial(steel_class))


@pytest.fixture
def h_profile() -> ISteelProfile:
    """Fixture to set up an H-shaped profile for testing."""
    profile = HEB.HEB360
    steel_class = SteelStrengthClass.S355
    return ISteelProfile.from_standard_profile(profile=profile, steel_material=SteelMaterial(steel_class))


@pytest.fixture
def empty_combined_steel_cross_section() -> CombinedSteelCrossSection:
    """Fixture to set up a combined steel cross-section for testing."""
    return CombinedSteelCrossSection(
        name="Empty Combined Steel Cross Section",
    )


@pytest.fixture
def rhs_profile() -> RHSSteelProfile:
    """Fixture to set up an RHS profile for testing."""
    profile = RHS.RHS400x200_16
    steel_class = SteelStrengthClass.S355
    return RHSSteelProfile.from_standard_profile(profile=profile, steel_material=SteelMaterial(steel_class))


@pytest.fixture
def lnp_profile() -> LNPProfile:
    """Fixture to set up an LNP profile for testing."""
    profile = LNP.LNP_100x50x6
    steel_class = SteelStrengthClass.S355
    return LNPProfile.from_standard_profile(
        profile=profile,
        steel_material=SteelMaterial(steel_class),
        corrosion=0,
    )
