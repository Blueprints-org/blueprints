"""Tests for the CHSStandardProfileClass enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHSStandardProfileClass


class TestCHSStandardProfileClass:
    """Tests for the CHSStandardProfileClass enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert CHSStandardProfileClass.CHS_21_3x2_3.value == "CHS 21.3x2.3"
        assert CHSStandardProfileClass.CHS_457x40.value == "CHS 457x40"

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "CHS 21.3x2.3" in [e.value for e in CHSStandardProfileClass]
        assert "CHS 457x40" in [e.value for e in CHSStandardProfileClass]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in CHSStandardProfileClass]
        assert len(values) == len(set(values))
