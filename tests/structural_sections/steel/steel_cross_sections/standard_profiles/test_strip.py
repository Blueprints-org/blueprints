"""Tests for the SteelStripProfileClass enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import SteelStripProfileClass


class TestSteelStripProfileClass:
    """Tests for the SteelStripProfileClass enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert SteelStripProfileClass.STRIP_160x5.value == "160 x 5"
        assert SteelStripProfileClass.STRIP_230x25.value == "230 x 25"

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "160 x 5" in [e.value for e in SteelStripProfileClass]
        assert "230 x 25" in [e.value for e in SteelStripProfileClass]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in SteelStripProfileClass]
        assert len(values) == len(set(values))
