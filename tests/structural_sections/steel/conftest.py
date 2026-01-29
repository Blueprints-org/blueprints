"""Fixtures for testing steel cross sections."""

import pytest

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


@pytest.fixture
def steel_cross_section() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing."""
    return SteelCrossSection(
        profile=IPE.IPE100,
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
    )


@pytest.fixture
def thick_41_mm_flange_i_profile() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing with thick flanges."""
    return SteelCrossSection(
        profile=IProfile(
            top_flange_width=200,  # mm, wide flange
            top_flange_thickness=41,  # mm, thick flange
            bottom_flange_width=200,  # mm, wide flange
            bottom_flange_thickness=41,  # mm, thick flange
            total_height=300,  # mm, example height
            web_thickness=20,  # mm, thick web
            top_radius=18,  # mm, typical radius
            bottom_radius=18,  # mm, typical radius
        ),
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
    )


@pytest.fixture
def thick_40_mm_flange_i_profile() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing with thick flanges."""
    return SteelCrossSection(
        profile=IProfile(
            top_flange_width=200,  # mm, wide flange
            top_flange_thickness=40,  # mm, thick flange
            bottom_flange_width=200,  # mm, wide flange
            bottom_flange_thickness=40,  # mm, thick flange
            total_height=300,  # mm, example height
            web_thickness=20,  # mm, thick web
            top_radius=18,  # mm, typical radius
            bottom_radius=18,  # mm, typical radius
        ),
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
    )
