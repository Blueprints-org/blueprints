"""Test for the GU standard profiles."""

from typing import ClassVar

import pytest

from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.structural_sections.steel.standard_profiles.gu import GU, GU_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.gu import __GUProfileParameters as GUProfileParameters


class TestGU:
    """Tests for the GU class."""

    expected_area: ClassVar[dict[str, int]] = {
        "GU6N": 5340,
        "GU7S": 6020,
        "GU8S": 6470,
        "GU10N": 7110,
        "GU11N": 7670,
        "GU12N": 8230,
        "GU13N": 7630,
        "GU14N": 8190,
        "GU15N": 8750,
        "GU16N": 9250,
        "GU18N": 9800,
        "GU18_400": 8830,
        "GU20N": 10340,
        "GU21N": 10430,
        "GU22N": 10970,
        "GU23N": 11520,
        "GU27N": 12410,
        "GU28N": 12970,
        "GU30N": 13530,
        "GU31N": 14000,
        "GU32N": 14540,
        "GU33N": 15080,
    }

    @pytest.mark.parametrize(("profile_name", "expected_data"), GU_PROFILES_DATABASE.items())
    def test_as_gu_profile(self, profile_name: str, expected_data: GUProfileParameters) -> None:
        """Test that the GU instance is converted to an GUProfile correctly."""
        profile = getattr(GU, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, SheetpileUProfile)
        assert profile.name == expected_profile_data.name
        assert profile.web_thickness == expected_profile_data.web_thickness
        assert profile.flange_thickness == expected_profile_data.flange_thickness
        assert profile.interlocking_ctc == expected_profile_data.interlocking_ctc
        assert profile.coordinates == expected_profile_data.coordinates
        assert profile.area == pytest.approx(self.expected_area[profile_name], rel=0.01)

    @pytest.mark.parametrize("profile_name", GU_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(GU, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0, f"Profile {profile.name} has non-positive area."

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of GU profiles."""
        profile1 = GU.GU6N
        profile2 = GU.GU6N

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = GU.GU18N
        assert profile1 != profile3

    @pytest.mark.parametrize("profile_name", GU_PROFILES_DATABASE.keys())
    def test_multiple_sheets(self, profile_name: str) -> None:
        """Test that multiple sheets can be created for all profiles."""
        profile = getattr(GU, profile_name)

        # Create profile with multiple sheets
        profile_multiple = profile.multiple_sheets(3)

        assert profile_multiple.number_of_sheets == 3
        assert profile_multiple.polygon.is_valid
        assert profile_multiple.area == pytest.approx(profile.area * 3, rel=0.05)

    def test_with_corrosion(self) -> None:
        """Test that corrosion can be applied to all profiles."""
        profile = GU.GU18N

        # Apply corrosion
        corrosion_mm = 1.0
        perimeter_mm = profile.polygon.length
        corroded_area = perimeter_mm * corrosion_mm
        expected_area = max(profile.area - corroded_area, 0)

        corroded_profile = profile.with_corrosion(corrosion=corrosion_mm)

        # Check that corrosion reduces dimensions
        assert corroded_profile.web_thickness == pytest.approx(profile.web_thickness - 2 * corrosion_mm, rel=0.01)
        assert corroded_profile.flange_thickness == pytest.approx(profile.flange_thickness - 2 * corrosion_mm, rel=0.01)
        assert corroded_profile.area == pytest.approx(expected_area, rel=0.01)
        assert corroded_profile.polygon.is_valid

    def test_max_thickness(self) -> None:
        """Test that max_thickness property returns the correct value."""
        profile = GU.GU18N

        expected_max = max(profile.web_thickness, profile.flange_thickness)
        assert profile.max_thickness == expected_max

    def test_zero_sheets(self) -> None:
        """Test that creating a profile with zero sheets raises an error."""
        profile = GU.GU6N
        with pytest.raises(ValueError, match="Number of sheets must be at least 1"):
            profile.multiple_sheets(0)

    def test_negative_corrosion(self) -> None:
        """Test that applying negative corrosion raises an error."""
        profile = GU.GU6N
        with pytest.raises(ValueError, match="Corrosion value must be non-negative"):
            profile.with_corrosion(-1)

    def test_excessive_corrosion(self) -> None:
        """Test that applying excessive corrosion raises an error."""
        profile = GU.GU6N
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            profile.with_corrosion(100)
