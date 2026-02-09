"""Fixtures for steel strength check tests."""

import pytest

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.steel.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


@pytest.fixture(scope="session")
def heb_steel_cross_section() -> SteelCrossSection:
    """Create a SteelCrossSection fixture with HEB300 profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = HEB.HEB300
    profile.section_properties()
    profile.unit_stress
    return SteelCrossSection(profile=profile, material=steel_material)


@pytest.fixture(scope="session")
def heb_welded_steel_cross_section() -> SteelCrossSection:
    """Create a SteelCrossSection fixture with welded HEB300 profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = HEB.HEB300
    profile.section_properties()
    profile.unit_stress
    return SteelCrossSection(profile=profile, material=steel_material, fabrication_method="welded")


@pytest.fixture(scope="session")
def chs_steel_cross_section() -> SteelCrossSection:
    """Create a SteelCrossSection fixture with CHS profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = CHS.CHS1016x12_5
    profile.section_properties()
    profile.unit_stress
    return SteelCrossSection(profile=profile, material=steel_material)
