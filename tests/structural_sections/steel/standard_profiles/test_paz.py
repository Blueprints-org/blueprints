"""Test for the PAZ standard profiles."""

from typing import ClassVar

import pytest

from blueprints.structural_sections.steel.profile_definitions.sheetpile_z_profile import SheetpileZProfile
from blueprints.structural_sections.steel.standard_profiles.paz import PAZ, PAZ_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.paz import __PAZProfileParameters as PAZProfileParameters


class TestPAZ:
    """Tests for the PAZ class."""

    expected_area: ClassVar[dict[str, int]] = {
        "PAZ4350": 4870,
        "PAZ4360": 5830,
        "PAZ4370": 6790,
        "PAZ4450": 4800,
        "PAZ4460": 5750,
        "PAZ4470": 6680,
        "PAZ4550": 4800,
        "PAZ4560": 5750,
        "PAZ4570": 6680,
        "PAZ4660": 5750,
        "PAZ4670": 6680,
        "PAZ5360": 6920,
        "PAZ5370": 8050,
        "PAZ5380": 9180,
        "PAZ5390": 10310,
        "PAZ54100": 11360,
        "PAZ5460": 6870,
        "PAZ5470": 7980,
        "PAZ5480": 9090,
        "PAZ5490": 10210,
        "PAZ55100": 11360,
        "PAZ5560": 6870,
        "PAZ5570": 7980,
        "PAZ5580": 9100,
        "PAZ5590": 10220,
        "PAZ56100": 11360,
        "PAZ5660": 6870,
        "PAZ5670": 7980,
        "PAZ5680": 9100,
        "PAZ5690": 10210,
    }

    @pytest.mark.parametrize(("profile_name", "expected_data"), PAZ_PROFILES_DATABASE.items())
    def test_as_paz_profile(self, profile_name: str, expected_data: PAZProfileParameters) -> None:
        """Test that the PAZ instance is converted to a PAZProfile correctly."""
        profile = getattr(PAZ, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, SheetpileZProfile)
        assert profile.name == expected_profile_data.name
        assert profile.web_thickness == expected_profile_data.web_thickness
        assert profile.flange_thickness == expected_profile_data.flange_thickness
        assert profile.interlocking_ctc == expected_profile_data.interlocking_ctc
        assert profile.coordinates == expected_profile_data.coordinates
        assert profile.area == pytest.approx(self.expected_area[profile_name], rel=0.02)

    @pytest.mark.parametrize("profile_name", PAZ_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(PAZ, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0, f"Profile {profile.name} has non-positive area."

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of PAZ profiles."""
        profile1 = PAZ.PAZ4350
        profile2 = PAZ.PAZ4350

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = PAZ.PAZ5690
        assert profile1 != profile3

    @pytest.mark.parametrize("profile_name", PAZ_PROFILES_DATABASE.keys())
    def test_multiple_sheets(self, profile_name: str) -> None:
        """Test that multiple sheets can be created for all profiles."""
        profile = getattr(PAZ, profile_name)

        # Create profile with multiple sheets
        profile_multiple = profile.multiple_sheets(3)

        assert profile_multiple.number_of_sheets == 3
        assert profile_multiple.polygon.is_valid
        assert profile_multiple.area == pytest.approx(profile.area * 3, rel=0.01)

    def test_with_corrosion(self) -> None:
        """Test that corrosion can be applied to all profiles."""
        profile = PAZ.PAZ5690

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
        profile = PAZ.PAZ5690

        expected_max = max(profile.web_thickness, profile.flange_thickness)
        assert profile.max_thickness == expected_max

    def test_zero_sheets(self) -> None:
        """Test that creating a profile with zero sheets raises an error."""
        profile = PAZ.PAZ4350
        with pytest.raises(ValueError, match="Number of sheets must be at least 1"):
            profile.multiple_sheets(0)

    def test_negative_corrosion(self) -> None:
        """Test that applying negative corrosion raises an error."""
        profile = PAZ.PAZ4350
        with pytest.raises(ValueError, match="Corrosion value must be non-negative"):
            profile.with_corrosion(-1)

    def test_excessive_corrosion(self) -> None:
        """Test that applying excessive corrosion raises an error."""
        profile = PAZ.PAZ4350
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            profile.with_corrosion(100)
