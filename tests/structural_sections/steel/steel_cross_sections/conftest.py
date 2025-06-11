"""Fixtures for testing steel cross sections."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import StripSteelProfile


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
def i_profile() -> ISteelProfile:
    """Fixture to set up an I-profile for testing."""
    profile = HEB.HEB360
    steel_class = SteelStrengthClass.S355
    return ISteelProfile.from_standard_profile(profile=profile, steel_material=SteelMaterial(steel_class))


@pytest.fixture
def empty_combined_steel_cross_section() -> CombinedSteelCrossSection:
    """Fixture to set up a combined steel cross-section for testing."""
    return CombinedSteelCrossSection(
        name="Empty Combined Steel Cross Section",
    )
