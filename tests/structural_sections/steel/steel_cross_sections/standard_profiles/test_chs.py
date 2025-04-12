"""Tests for the CHS enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS


class TestCHS:
    """Tests for the CHS enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert CHS.CHS21_3x2_3.value == ("CHS 21.3x2.3", 21.3, 2.3)
        assert CHS.CHS2220x40.value == ("CHS 2220x40", 2220, 40)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "CHS 21.3x2.3" in [e.value[0] for e in CHS]
        assert "CHS 2220x40" in [e.value[0] for e in CHS]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in CHS]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = CHS.CHS21_3x2_3
        assert profile.alias == "CHS 21.3x2.3"
        assert profile.diameter == 21.3
        assert profile.thickness == 2.3
