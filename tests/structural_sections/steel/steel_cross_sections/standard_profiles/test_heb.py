"""Test the HEBStandardProfileClass enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEBStandardProfileClass


class TestHEBStandardProfileClass:
    """Tests for the HEBStandardProfileClass enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert HEBStandardProfileClass.HEB_100.value == ("HEB100", 100, 100, 6, 10, 12)
        assert HEBStandardProfileClass.HEB_200.value == ("HEB200", 200, 200, 9, 15, 18)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "HEB100" in [e.value[0] for e in HEBStandardProfileClass]
        assert "HEB200" in [e.value[0] for e in HEBStandardProfileClass]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in HEBStandardProfileClass]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = HEBStandardProfileClass.HEB_100
        assert profile.code == "HEB100"
        assert profile.h == 100
        assert profile.b == 100
        assert profile.t_w == 6
        assert profile.t_f == 10
        assert profile.radius == 12
