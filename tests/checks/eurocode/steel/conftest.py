"""Fixtures for steel strength check tests."""

import pytest
from sectionproperties.post.post import SectionProperties

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.steel.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.unp import UNP
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


@pytest.fixture(scope="class")
def heb_steel_cross_section() -> tuple[SteelCrossSection, SectionProperties]:
    """Create a SteelCrossSection fixture with HEB300 profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = HEB.HEB300
    return SteelCrossSection(profile=profile, material=steel_material), profile.section_properties()


@pytest.fixture(scope="class")
def chs_steel_cross_section() -> tuple[SteelCrossSection, SectionProperties]:
    """Create a SteelCrossSection fixture with CHS profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = CHS.CHS1016x12_5
    return SteelCrossSection(profile=profile, material=steel_material), profile.section_properties()


@pytest.fixture(scope="class")
def unp_steel_cross_section() -> tuple[SteelCrossSection, SectionProperties]:
    """Create a SteelCrossSection fixture with UNP80 profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = UNP.UNP80
    return SteelCrossSection(profile=profile, material=steel_material), profile.section_properties()
