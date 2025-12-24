"""Tests for the CHS class."""

from blueprints.structural_sections.steel.profile_definitions.chs_profile import CHSProfile
from blueprints.structural_sections.steel.standard_profiles.chs import CHS


class TestCHS:
    """Tests for the CHS class."""

    def test_as_chs_profile(self) -> None:
        """Test that the CHS instance is converted to a CHSProfile correctly."""
        profile = CHS.CHS21_3x2_3

        assert isinstance(profile, CHSProfile)
        assert profile.outer_diameter == profile.outer_diameter
        assert profile.wall_thickness == profile.wall_thickness
