"""Fixtures for steel strength check tests."""

import pytest

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.steel.profile_definitions.rhs_profile import RHSProfile
from blueprints.structural_sections.steel.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.standard_profiles.rhscf import RHSCF
from blueprints.structural_sections.steel.steel_cross_section import FabricationMethod, SteelCrossSection


@pytest.fixture(scope="class")
def rhs_steel_cross_section() -> SteelCrossSection:
    """Create a SteelCrossSection fixture with RHS profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = RHSCF.RHSCF200x100x8
    return SteelCrossSection(profile=profile, material=steel_material)


@pytest.fixture(scope="class")
def rhs_welded_steel_cross_section() -> SteelCrossSection:
    """Create a SteelCrossSection fixture with RHS profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = RHSCF.RHSCF200x100x8
    return SteelCrossSection(profile=profile, material=steel_material, fabrication_method=FabricationMethod.WELDED)


@pytest.fixture(scope="class")
def rhs_custom_steel_cross_section() -> SteelCrossSection:
    """Create a SteelCrossSection fixture with custom RHS profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = RHSProfile(
        total_width=200, total_height=300, left_wall_thickness=10, right_wall_thickness=11, top_wall_thickness=12, bottom_wall_thickness=12
    )
    return SteelCrossSection(profile=profile, material=steel_material, fabrication_method=FabricationMethod.COLD_FORMED)


@pytest.fixture(scope="class")
def heb_steel_cross_section() -> SteelCrossSection:
    """Create a SteelCrossSection fixture with HEB300 profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = HEB.HEB300
    return SteelCrossSection(profile=profile, material=steel_material)


@pytest.fixture(scope="class")
def heb_welded_steel_cross_section() -> SteelCrossSection:
    """Create a SteelCrossSection fixture with welded HEB300 profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = HEB.HEB300
    return SteelCrossSection(profile=profile, material=steel_material, fabrication_method=FabricationMethod.WELDED)


@pytest.fixture(scope="class")
def chs_steel_cross_section() -> SteelCrossSection:
    """Create a SteelCrossSection fixture with CHS profile and S355 steel material."""
    steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
    profile = CHS.CHS1016x12_5
    return SteelCrossSection(profile=profile, material=steel_material)
