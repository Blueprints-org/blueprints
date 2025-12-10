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
        profile=IProfile.from_standard_profile(IPE.IPE100),
        material=SteelMaterial(steel_class=SteelStrengthClass.S275),
    )
