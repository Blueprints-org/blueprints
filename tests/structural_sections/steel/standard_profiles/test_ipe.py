"""Test for the IPE standard profiles."""

import pytest

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE, IPE_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.ipe import __IPEProfileParameters as IPEProfileParameters


class TestIPE:
    """Tests for the IPE class."""

    @pytest.mark.parametrize(("profile_name", "expected_data"), IPE_PROFILES_DATABASE.items())
    def test_as_ipe_profile(self, profile_name: str, expected_data: IPEProfileParameters) -> None:
        """Test that the IPE instance is converted to an IProfile correctly."""
        profile = getattr(IPE, profile_name)
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

    @pytest.mark.parametrize("profile_name", IPE_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(IPE, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of IPE profiles."""
        profile1 = IPE.IPE200
        profile2 = IPE.IPE200

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = IPE.IPE300
        assert profile1 != profile3

    def test_iteration(self) -> None:
        """Test that iterating over the IPE class yields valid profiles."""
        for profile in IPE:
            assert isinstance(profile, IProfile)
            assert profile.polygon.is_valid
            assert profile.area > 0
