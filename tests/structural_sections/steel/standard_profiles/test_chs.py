"""Tests for the CHS class."""

import pytest

from blueprints.structural_sections.steel.profile_definitions.chs_profile import CHSProfile
from blueprints.structural_sections.steel.standard_profiles.chs import CHS, CHS_PROFILES


class TestCHS:
    """Tests for the CHS class."""

    @pytest.mark.parametrize(("profile_name", "expected_data"), CHS_PROFILES.items())
    def test_as_chs_profile(self, profile_name: str, expected_data: tuple) -> None:
        """Test that the CHS instance is converted to a CHSProfile correctly."""
        profile = getattr(CHS, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, CHSProfile)
        assert profile.name == expected_profile_data[0]
        assert profile.outer_diameter == expected_profile_data[1]
        assert profile.wall_thickness == expected_profile_data[2]

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of CHS profiles."""
        profile1 = CHS.CHS21_3x2_3
        profile2 = CHS.CHS21_3x2_3

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = CHS.CHS1016x20
        assert profile1 != profile3
