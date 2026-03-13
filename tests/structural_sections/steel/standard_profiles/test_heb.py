"""Test for the HEB standard profiles."""

import pytest

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.heb import HEB, HEB_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.heb import __HEBProfileParameters as HEBProfileParameters


class TestHEB:
    """Tests for the HEB class."""

    @pytest.mark.parametrize(("profile_name", "expected_data"), HEB_PROFILES_DATABASE.items())
    def test_as_heb_profile(self, profile_name: str, expected_data: HEBProfileParameters) -> None:
        """Test that the HEB instance is converted to an IProfile correctly."""
        profile = getattr(HEB, profile_name)
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

    @pytest.mark.parametrize("profile_name", HEB_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(HEB, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of HEB profiles."""
        profile1 = HEB.HEB200
        profile2 = HEB.HEB200

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = HEB.HEB300
        assert profile1 != profile3

    def test_iteration(self) -> None:
        """Test that iterating over the HEB class yields valid profiles."""
        for profile in HEB:
            assert isinstance(profile, IProfile)
            assert profile.polygon.is_valid
            assert profile.area > 0
