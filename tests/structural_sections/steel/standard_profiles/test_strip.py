"""Test for the Strip standard profiles."""

import pytest

from blueprints.structural_sections.steel.profile_definitions.strip_profile import StripProfile
from blueprints.structural_sections.steel.standard_profiles.strip import STRIP_PROFILES_DATABASE, Strip
from blueprints.structural_sections.steel.standard_profiles.strip import __StripProfileParameters as StripProfileParameters


class TestStrip:
    """Tests for the Strip class."""

    @pytest.mark.parametrize(("profile_name", "expected_data"), STRIP_PROFILES_DATABASE.items())
    def test_as_strip_profile(self, profile_name: str, expected_data: StripProfileParameters) -> None:
        """Test that the Strip instance is converted to a StripProfile correctly."""
        profile = getattr(Strip, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, StripProfile)
        assert profile.name == expected_profile_data.name
        assert profile.width == expected_profile_data.width
        assert profile.height == expected_profile_data.height

    @pytest.mark.parametrize("profile_name", STRIP_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(Strip, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of Strip profiles."""
        profile1 = Strip.STRIP200x10
        profile2 = Strip.STRIP200x10

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = Strip.STRIP180x5
        assert profile1 != profile3

    def test_iteration(self) -> None:
        """Test that iterating over the Strip class yields valid profiles."""
        for profile in Strip:
            assert isinstance(profile, StripProfile)
            assert profile.polygon.is_valid
            assert profile.area > 0
