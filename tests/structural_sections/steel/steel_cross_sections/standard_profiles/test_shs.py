"""Test the SHSStandardProfileClass enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shs import SHSStandardProfileClass


class TestSHSStandardProfileClass:
    """Tests for the SHSStandardProfileClass enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert SHSStandardProfileClass.SHS_40_2_6.value == ("SHS40/2.6", 40, 2.6, 3.9, 2.6)
        assert SHSStandardProfileClass.SHS_100_10.value == ("SHS100/10", 100, 10, 15, 10)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "SHS40/2.6" in [e.value[0] for e in SHSStandardProfileClass]
        assert "SHS100/10" in [e.value[0] for e in SHSStandardProfileClass]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in SHSStandardProfileClass]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = SHSStandardProfileClass.SHS_40_2_6
        assert profile.code == "SHS40/2.6"
        assert profile.total_width == 40
        assert profile.total_height == 40
        assert profile.thickness == 2.6
        assert profile.outer_radius == 3.9
        assert profile.inner_radius == 2.6
