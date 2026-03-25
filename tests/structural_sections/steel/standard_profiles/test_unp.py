"""Test for the UNP standard profiles."""

import pytest

from blueprints.structural_sections.steel.profile_definitions.unp_profile import UNPProfile
from blueprints.structural_sections.steel.standard_profiles.unp import UNP, UNP_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.unp import __UNPProfileParameters as UNPProfileParameters


class TestUNP:
    """Tests for the UNP class."""

    @pytest.mark.parametrize(("profile_name", "expected_data"), UNP_PROFILES_DATABASE.items())
    def test_as_unp_profile(self, profile_name: str, expected_data: UNPProfileParameters) -> None:
        """Test that the UNP instance is converted to a UNPProfile correctly."""
        profile = getattr(UNP, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, UNPProfile)
        assert profile.name == expected_profile_data.name
        assert profile.top_flange_total_width == expected_profile_data.top_flange_total_width
        assert profile.top_flange_thickness == expected_profile_data.top_flange_thickness
        assert profile.bottom_flange_total_width == expected_profile_data.bottom_flange_total_width
        assert profile.bottom_flange_thickness == expected_profile_data.bottom_flange_thickness
        assert profile.total_height == expected_profile_data.total_height
        assert profile.web_thickness == expected_profile_data.web_thickness
        assert profile.top_root_fillet_radius == expected_profile_data.top_root_fillet_radius
        assert profile.bottom_root_fillet_radius == expected_profile_data.bottom_root_fillet_radius
        assert profile.top_toe_radius == expected_profile_data.top_toe_radius
        assert profile.bottom_toe_radius == expected_profile_data.bottom_toe_radius
        assert profile.top_slope == expected_profile_data.top_slope
        assert profile.bottom_slope == expected_profile_data.bottom_slope

    @pytest.mark.parametrize("profile_name", UNP_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(UNP, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of UNP profiles."""
        profile1 = UNP.UNP200
        profile2 = UNP.UNP200

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = UNP.UNP300
        assert profile1 != profile3

    def test_iteration(self) -> None:
        """Test that iterating over the UNP class yields valid profiles."""
        for profile in UNP:
            assert isinstance(profile, UNPProfile)
            assert profile.polygon.is_valid
            assert profile.area > 0
