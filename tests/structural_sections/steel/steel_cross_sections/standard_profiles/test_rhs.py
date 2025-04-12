"""Test the RHS enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHS


class TestRHS:
    """Tests for the RHS enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert RHS.RHS50x30_2_6.value == ("RHS50x30x2.6", 50, 30, 2.6, 3.9, 2.6)
        assert RHS.RHS500x300_20.value == ("RHS500x300x20", 500, 300, 20, 30, 20)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "RHS50x30x2.6" in [e.value[0] for e in RHS]
        assert "RHS500x300x20" in [e.value[0] for e in RHS]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in RHS]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = RHS.RHS50x30_2_6
        assert profile.alias == "RHS50x30x2.6"
        assert profile.total_height == 50
        assert profile.total_width == 30
        assert profile.thickness == 2.6
        assert profile.outer_radius == 3.9
        assert profile.inner_radius == 2.6
