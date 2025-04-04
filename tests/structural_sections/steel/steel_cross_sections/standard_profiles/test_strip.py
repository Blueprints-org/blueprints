"""Tests for the StripStandardProfileClassClass enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import StripStandardProfileClass


class TestStripStandardProfileClassClass:
    """Tests for the StripStandardProfileClassClass enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert StripStandardProfileClass.STRIP_160x5.value == ("160x5", 160, 5)
        assert StripStandardProfileClass.STRIP_230x25.value == ("230x25", 230, 25)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "160x5" in [e.value[0] for e in StripStandardProfileClass]
        assert "230x25" in [e.value[0] for e in StripStandardProfileClass]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in StripStandardProfileClass]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = StripStandardProfileClass.STRIP_160x5
        assert profile.code == "160x5"
        assert profile.width == 160
        assert profile.height == 5
