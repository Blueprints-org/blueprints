"""Test for the LNP standard profiles."""

import pytest

from blueprints.structural_sections.steel.profile_definitions.lnp_profile import LNPProfile
from blueprints.structural_sections.steel.standard_profiles.lnp import LNP, LNP_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.lnp import __LNPProfileParameters as LNPProfileParameters


class TestLNP:
    """Tests for the LNP class."""

    @pytest.mark.parametrize(("profile_name", "expected_data"), LNP_PROFILES_DATABASE.items())
    def test_as_lnp_profile(self, profile_name: str, expected_data: LNPProfileParameters) -> None:
        """Test that the LNP instance is converted to an LNPProfile correctly."""
        profile = getattr(LNP, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, LNPProfile)
        assert profile.name == expected_profile_data.name
        assert profile.total_width == expected_profile_data.total_width
        assert profile.total_height == expected_profile_data.total_height
        assert profile.web_thickness == expected_profile_data.web_thickness
        assert profile.base_thickness == expected_profile_data.base_thickness
        assert profile.root_radius == expected_profile_data.root_radius
        assert profile.back_radius == expected_profile_data.back_radius
        assert profile.web_toe_radius == expected_profile_data.web_toe_radius
        assert profile.base_toe_radius == expected_profile_data.base_toe_radius

    @pytest.mark.parametrize("profile_name", LNP_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(LNP, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of LNP profiles."""
        profile1 = LNP.LNP40x40x4
        profile2 = LNP.LNP40x40x4

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = LNP.LNP60x40x7
        assert profile1 != profile3

    def test_iteration(self) -> None:
        """Test that iterating over the LNP class yields valid profiles."""
        for profile in LNP:
            assert isinstance(profile, LNPProfile)
            assert profile.polygon.is_valid
            assert profile.area > 0
