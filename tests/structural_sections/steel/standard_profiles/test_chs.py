"""Tests for the CHS enum."""

from dataclasses import asdict

from blueprints.structural_sections.steel.profile_definitions.chs_profile import CHSProfile
from blueprints.structural_sections.steel.standard_profiles.chs import CHS


class TestCHS:
    """Tests for the CHS enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert CHS.CHS21_3x2_3.value == CHSProfile(profile_name="CHS 21.3x2.3", outer_diameter=21.3, wall_thickness=2.3)
        assert asdict(CHS.CHS21_3x2_3) == asdict(CHSProfile(profile_name="CHS 21.3x2.3", outer_diameter=21.3, wall_thickness=2.3))
        assert CHS.CHS2220x40.value == CHSProfile(profile_name="CHS 2220x40", outer_diameter=2220, wall_thickness=40)
        assert asdict(CHS.CHS2220x40) == asdict(CHSProfile(profile_name="CHS 2220x40", outer_diameter=2220, wall_thickness=40))

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "CHS 21.3x2.3" in [profile.profile_name for profile in CHS]
        assert "CHS 2220x40" in [profile.profile_name for profile in CHS]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        assert len(CHS) == len(set(CHS))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = CHS.CHS21_3x2_3
        assert profile.profile_name == "CHS 21.3x2.3"
        assert profile.outer_diameter == 21.3
        assert profile.wall_thickness == 2.3

    def test_as_profile(self) -> None:
        """Test that the CHS enum instance behaves as a CHSProfile instance."""
        profile = CHS.CHS21_3x2_3

        assert isinstance(profile, CHSProfile)
        assert profile.outer_diameter == 21.3
        assert profile.wall_thickness == 2.3

    def test_as_profile_with_corrosion(self) -> None:
        """Test that the CHS enum instance can create a corroded profile."""
        profile = CHS.CHS21_3x2_3
        corrosion_outside = 0.5
        corrosion_inside = 0.3
        corroded_profile = profile.with_corrosion(
            corrosion_outside=corrosion_outside,
            corrosion_inside=corrosion_inside,
        )

        assert isinstance(corroded_profile, CHSProfile)
        assert corroded_profile.outer_diameter == profile.outer_diameter - 2 * corrosion_outside
        assert corroded_profile.wall_thickness == profile.wall_thickness - corrosion_outside - corrosion_inside
        assert corroded_profile.profile_name == f"CHS 21.3x2.3 (corrosion inside: {corrosion_inside} mm, corrosion outside: {corrosion_outside} mm)"
