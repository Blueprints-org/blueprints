"""Test the RHSStandardProfileClass enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHSStandardProfileClass


class TestRHSStandardProfileClass:
    """Tests for the RHSStandardProfileClass enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert RHSStandardProfileClass.RHS50x30_2_6.value == ("RHS50x30/2.6", 50, 30, 2.6, 3.9, 2.6)
        assert RHSStandardProfileClass.RHS100x60_8.value == ("RHS100x60/8", 100, 60, 8, 12, 8)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "RHS50x30/2.6" in [e.value[0] for e in RHSStandardProfileClass]
        assert "RHS100x60/8" in [e.value[0] for e in RHSStandardProfileClass]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in RHSStandardProfileClass]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = RHSStandardProfileClass.RHS50x30_2_6
        assert profile.code == "RHS50x30/2.6"
        assert profile.total_height == 50
        assert profile.total_width == 30
        assert profile.thickness == 2.6
        assert profile.outer_radius == 3.9
        assert profile.inner_radius == 2.6
