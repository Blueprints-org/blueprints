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

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of Strip profiles."""
        profile1 = Strip.STRIP200x10
        profile2 = Strip.STRIP200x10

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = Strip.STRIP180x5
        assert profile1 != profile3
