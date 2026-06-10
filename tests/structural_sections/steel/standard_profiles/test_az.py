"""Test for the AZ standard profiles."""

from typing import ClassVar

import pytest

from blueprints.structural_sections.steel.profile_definitions.az_profile import AZProfile
from blueprints.structural_sections.steel.standard_profiles.az import AZ, AZ_PROFILES_DATABASE
from blueprints.structural_sections.steel.standard_profiles.az import __AZProfileParameters as AZProfileParameters


class TestAZ:
    """Tests for the AZ class."""

    expected_area: ClassVar[dict[str, int]] = {
        "AZ12_700": 8620,
        "AZ12_770": 9250,
        "AZ13_700": 9430,
        "AZ13_700_10_10": 9830,
        "AZ13_770": 9690,
        "AZ14_700": 10230,
        "AZ14_770": 10130,
        "AZ14_770_10_10": 10560,
        "AZ17_700": 9310,
        "AZ18": 9480,
        "AZ18_10_10": 9910,
        "AZ18_700": 9750,
        "AZ18_800": 10290,
        "AZ19_700": 10190,
        "AZ20_700": 10640,
        "AZ22_800": 12280,
        "AZ24_700": 12190,
        "AZ25_800": 13060,
        "AZ26": 12460,
        "AZ26_700": 13100,
        "AZ27_800": 14080,
        "AZ28_700": 14020,
        "AZ28_750": 12840,
        "AZ30_750": 13850,
        "AZ32_750": 14870,
        "AZ36_700N": 15110,
        "AZ38_700N": 16100,
        "AZ40_700N": 17090,
        "AZ42_700N": 18110,
        "AZ44_700N": 19100,
        "AZ46_700N": 20090,
        "AZ48_700": 20190,
        "AZ50_700": 21180,
        "AZ52_700": 22170,
    }

    @pytest.mark.parametrize(("profile_name", "expected_data"), AZ_PROFILES_DATABASE.items())
    def test_as_az_profile(self, profile_name: str, expected_data: AZProfileParameters) -> None:
        """Test that the AZ instance is converted to an AZProfile correctly."""
        profile = getattr(AZ, profile_name)
        expected_profile_data = expected_data

        assert isinstance(profile, AZProfile)
        assert profile.name == expected_profile_data.name
        assert profile.web_thickness == expected_profile_data.web_thickness
        assert profile.flange_thickness == expected_profile_data.flange_thickness
        assert profile.interlocking_ctc == expected_profile_data.interlocking_ctc
        assert profile.coordinates == expected_profile_data.coordinates
        assert profile.area == pytest.approx(self.expected_area[profile_name], rel=0.01)

    @pytest.mark.parametrize("profile_name", AZ_PROFILES_DATABASE.keys())
    def test_validity(self, profile_name: str) -> None:
        """Test that the created profile instance is valid."""
        profile = getattr(AZ, profile_name)

        assert profile.polygon.is_valid, f"Profile {profile.name} is invalid."
        assert profile.area > 0, f"Profile {profile.name} has non-positive area."

    def test_equality_and_identity(self) -> None:
        """Test the equality and identity of AZ profiles."""
        profile1 = AZ.AZ12_700
        profile2 = AZ.AZ12_700

        # Check that two profiles with the same name are equal but not the same object
        assert profile1 == profile2
        assert profile1 is not profile2

        profile3 = AZ.AZ18_700
        assert profile1 != profile3

    @pytest.mark.parametrize("profile_name", AZ_PROFILES_DATABASE.keys())
    def test_multiple_sheets(self, profile_name: str) -> None:
        """Test that multiple sheets can be created for all profiles."""
        profile = getattr(AZ, profile_name)

        # Create profile with multiple sheets
        profile_multiple = profile.multiple_sheets(3)

        assert profile_multiple.number_of_sheets == 3
        assert profile_multiple.polygon.is_valid
        assert profile_multiple.area == pytest.approx(profile.area * 3, rel=0.01)

    def test_with_corrosion(self) -> None:
        """Test that corrosion can be applied to all profiles."""
        profile = AZ.AZ36_700N

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
        profile = AZ.AZ36_700N

        expected_max = max(profile.web_thickness, profile.flange_thickness)
        assert profile.max_thickness == expected_max

    def test_zero_sheets(self) -> None:
        """Test that creating a profile with zero sheets raises an error."""
        profile = AZ.AZ12_700
        with pytest.raises(ValueError, match="Number of sheets must be at least 1"):
            profile.multiple_sheets(0)

    def test_negative_corrosion(self) -> None:
        """Test that applying negative corrosion raises an error."""
        profile = AZ.AZ12_700
        with pytest.raises(ValueError, match="Corrosion value must be non-negative"):
            profile.with_corrosion(-1)

    def test_excessive_corrosion(self) -> None:
        """Test that applying excessive corrosion raises an error."""
        profile = AZ.AZ12_700
        with pytest.raises(ValueError, match="Corrosion amount is too large, resulting in an empty profile"):
            profile.with_corrosion(100)
