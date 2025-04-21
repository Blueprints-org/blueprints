"""Fixtures for testing steel cross sections."""

import pytest

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSSteelProfile, LoadStandardCHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import LoadStandardStrip, StripSteelProfile


@pytest.fixture
def strip_profile() -> StripSteelProfile:
    """Fixture to set up a Strip profile for testing."""
    profile = Strip.STRIP160x5
    steel_class = SteelStrengthClass.S355
    return LoadStandardStrip(profile=profile, steel_class=steel_class).get_profile()


@pytest.fixture
def chs_profile() -> CHSSteelProfile:
    """Fixture to set up a CHS profile for testing."""
    profile: CHS = CHS.CHS508x16
    steel_class: SteelStrengthClass = SteelStrengthClass.S355
    return LoadStandardCHS(profile=profile, steel_class=steel_class).get_profile()
