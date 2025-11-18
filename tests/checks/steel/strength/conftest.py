"""Tests for SteelIProfileStrengthClass3.NormalForceCheck according to Eurocode 3."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB


@pytest.fixture(scope="class")
def heb_profile_and_properties() -> tuple[ISteelProfile, SectionProperties]:
    """Fixture to create a standard HEB profile and its section properties."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    heb_profile = ISteelProfile.from_standard_profile(
        profile=HEB.HEB300,
        steel_material=steel_material,
        corrosion=0,
    )
    heb_properties = heb_profile.section_properties(geometric=True, plastic=False, warping=False)
    return heb_profile, heb_properties
