"""Fixtures for testing steel cross sections."""

import pytest

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.standard_profiles.rhscf import RHSCF
from blueprints.structural_sections.steel.standard_profiles.shs import SHS
from blueprints.structural_sections.steel.steel_cross_section import FabricationMethod, SteelCrossSection


@pytest.fixture
def steel_cross_section_hot_formed() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing."""
    return SteelCrossSection(
        profile=IPE.IPE100,
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
    )


@pytest.fixture
def steel_cross_section_corroded() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing."""
    return SteelCrossSection(
        profile=IPE.IPE100.with_corrosion(corrosion=1.1),
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
    )


@pytest.fixture
def steel_cross_section_cold_formed() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing."""
    return SteelCrossSection(
        profile=RHSCF.RHSCF100x40x2_5,
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
    )


@pytest.fixture
def steel_cross_section_cold_formed_corroded() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing."""
    return SteelCrossSection(
        profile=RHSCF.RHSCF100x40x2_5.with_corrosion(corrosion_outside=0.5),
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
    )


@pytest.fixture
def steel_cross_section_welded() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing."""
    return SteelCrossSection(
        profile=SHS.SHS100x10,
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
        fabrication_method=FabricationMethod.WELDED,
    )


@pytest.fixture
def steel_cross_section_welded_corroded() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing."""
    return SteelCrossSection(
        profile=SHS.SHS100x10.with_corrosion(corrosion_inside=1.0),
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
        fabrication_method=FabricationMethod.WELDED,
    )


@pytest.fixture
def steel_cross_section_fabrication_not_set() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing."""
    return SteelCrossSection(
        profile=CHS.CHS1016x12_5.with_corrosion(corrosion_inside=1.0, corrosion_outside=1.5),
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
    )


@pytest.fixture
def steel_cross_section_fabrication_different_name() -> SteelCrossSection:
    """Fixture to set up a SteelCrossSection for testing."""
    profile = CHS.CHS1016x12_5.with_corrosion(corrosion_inside=1.0, corrosion_outside=1.5)
    object.__setattr__(profile, "name", "Custom_CHS_Profile")
    return SteelCrossSection(
        profile=profile,
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
