"""Test for the SHS standard profiles."""

import pytest

from blueprints.structural_sections.steel.profile_definitions.rhs_profile import RHSProfile
from blueprints.structural_sections.steel.standard_profiles.shs import SHS, SHS_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.shs import __SHSProfileParameters as SHSProfileParameters


class TestSHS:
    """Tests for the SHS class."""

    @pytest.mark.parametrize(("profile_name", "expected_data"), SHS_PROFILES_DATABASE.items())
    def test_as_rhs_profile(self, profile_name: str, expected_data: SHSProfileParameters) -> None:
        """Test that the SHS instance is converted to an RHSProfile correctly."""
        profile = getattr(SHS, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, RHSProfile)
        assert profile.name == expected_profile_data.name
        assert profile.total_height == expected_profile_data.total_height
        assert profile.total_width == expected_profile_data.total_width
        assert profile.left_wall_thickness == expected_profile_data.left_wall_thickness
        assert profile.right_wall_thickness == expected_profile_data.right_wall_thickness
        assert profile.top_wall_thickness == expected_profile_data.top_wall_thickness
        assert profile.bottom_wall_thickness == expected_profile_data.bottom_wall_thickness
        assert profile.top_right_outer_radius == expected_profile_data.top_right_outer_radius
        assert profile.top_left_outer_radius == expected_profile_data.top_left_outer_radius
        assert profile.bottom_right_outer_radius == expected_profile_data.bottom_right_outer_radius
        assert profile.bottom_left_outer_radius == expected_profile_data.bottom_left_outer_radius
        assert profile.top_right_inner_radius == expected_profile_data.top_right_inner_radius
        assert profile.top_left_inner_radius == expected_profile_data.top_left_inner_radius
        assert profile.bottom_right_inner_radius == expected_profile_data.bottom_right_inner_radius
        assert profile.bottom_left_inner_radius == expected_profile_data.bottom_left_inner_radius

    @pytest.mark.parametrize("profile_name", SHS_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(SHS, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of SHS profiles."""
        profile1 = SHS.SHS100x5
        profile2 = SHS.SHS100x5

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = SHS.SHS200x8
        assert profile1 != profile3

    def test_iteration(self) -> None:
        """Test that iterating over the SHS class yields valid profiles."""
        for profile in SHS:
            assert isinstance(profile, RHSProfile)
            assert profile.polygon.is_valid
            assert profile.area > 0
