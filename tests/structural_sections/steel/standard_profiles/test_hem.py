"""Test for the HEM standard profiles."""

import pytest

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.hem import HEM, HEM_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.hem import __HEMProfileParameters as HEMProfileParameters


class TestHEM:
    """Tests for the HEM class."""

    @pytest.mark.parametrize(("profile_name", "expected_data"), HEM_PROFILES_DATABASE.items())
    def test_as_hem_profile(self, profile_name: str, expected_data: HEMProfileParameters) -> None:
        """Test that the HEM instance is converted to an IProfile correctly."""
        profile = getattr(HEM, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, IProfile)
        assert profile.name == expected_profile_data.name
        assert profile.total_height == expected_profile_data.total_height
        assert profile.web_thickness == expected_profile_data.web_thickness
        assert profile.bottom_flange_width == expected_profile_data.bottom_flange_width
        assert profile.bottom_flange_thickness == expected_profile_data.bottom_flange_thickness
        assert profile.top_flange_width == expected_profile_data.top_flange_width
        assert profile.top_flange_thickness == expected_profile_data.top_flange_thickness
        assert profile.top_radius == expected_profile_data.top_radius
        assert profile.bottom_radius == expected_profile_data.bottom_radius

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of HEM profiles."""
        profile1 = HEM.HEM200
        profile2 = HEM.HEM200

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = HEM.HEM300
        assert profile1 != profile3
