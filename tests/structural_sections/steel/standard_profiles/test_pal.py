"""Test for the PAL standard profiles."""

from typing import ClassVar

import pytest

from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.structural_sections.steel.standard_profiles.pal import PAL, PAL_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.pal import __PALProfileParameters as PALProfileParameters


class TestPAL:
    """Tests for the PAL class."""

    expected_area: ClassVar[dict[str, int]] = {
        "PAL3030": 2470,
        "PAL3040": 3290,
        "PAL3050": 4100,
        "PAL3130": 3000,
        "PAL3140": 3990,
        "PAL3150": 4970,
    }

    @pytest.mark.parametrize(("profile_name", "expected_data"), PAL_PROFILES_DATABASE.items())
    def test_as_pal_profile(self, profile_name: str, expected_data: PALProfileParameters) -> None:
        """Test that the PAL instance is converted to an PALProfile correctly."""
        profile = getattr(PAL, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, SheetpileUProfile)
        assert profile.name == expected_profile_data.name
        assert profile.web_thickness == expected_profile_data.web_thickness
        assert profile.flange_thickness == expected_profile_data.flange_thickness
        assert profile.interlocking_ctc == expected_profile_data.interlocking_ctc
        assert profile.coordinates == expected_profile_data.coordinates
        assert profile.area == pytest.approx(self.expected_area[profile_name], rel=0.01)

    @pytest.mark.parametrize("profile_name", PAL_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(PAL, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0, f"Profile {profile.name} has non-positive area."

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of PAL profiles."""
        profile1 = PAL.PAL3030
        profile2 = PAL.PAL3030

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = PAL.PAL3040
        assert profile1 != profile3

    @pytest.mark.parametrize("profile_name", PAL_PROFILES_DATABASE.keys())
    def test_multiple_sheets(self, profile_name: str) -> None:
        """Test that multiple sheets can be created for all profiles."""
        profile = getattr(PAL, profile_name)

        # Create profile with multiple sheets
        profile_multiple = profile.multiple_sheets(3)

        assert profile_multiple.number_of_sheets == 3
        assert profile_multiple.polygon.is_valid
        assert profile_multiple.area == pytest.approx(profile.area * 3, rel=0.05)

    def test_with_corrosion(self) -> None:
        """Test that corrosion can be applied to all profiles."""
        profile = PAL.PAL3040

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
        profile = PAL.PAL3040

        expected_max = max(profile.web_thickness, profile.flange_thickness)
        assert profile.max_thickness == expected_max

    def test_zero_sheets(self) -> None:
        """Test that creating a profile with zero sheets raises an error."""
        profile = PAL.PAL3030
        with pytest.raises(ValueError, match="Number of sheets must be at least 1"):
            profile.multiple_sheets(0)

    def test_negative_corrosion(self) -> None:
        """Test that applying negative corrosion raises an error."""
        profile = PAL.PAL3030
        with pytest.raises(ValueError, match="Corrosion value must be non-negative"):
            profile.with_corrosion(-1)

    def test_excessive_corrosion(self) -> None:
        """Test that applying excessive corrosion raises an error."""
        profile = PAL.PAL3030
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            profile.with_corrosion(100)
