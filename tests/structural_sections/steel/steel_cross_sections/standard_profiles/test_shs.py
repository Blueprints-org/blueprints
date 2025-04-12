"""Test the SHS enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shs import SHS


class TestSHS:
    """Tests for the SHS enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert SHS.SHS_40_2_6.value == ("SHS40x2.6", 40, 2.6, 3.9, 2.6)
        assert SHS.SHS_400_20.value == ("SHS400x20", 400, 20, 30, 20)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "SHS40x2.6" in [e.value[0] for e in SHS]
        assert "SHS400x20" in [e.value[0] for e in SHS]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in SHS]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = SHS.SHS_40_2_6
        assert profile.alias == "SHS40x2.6"
        assert profile.total_width == 40
        assert profile.total_height == 40
        assert profile.thickness == 2.6
        assert profile.outer_radius == 3.9
        assert profile.inner_radius == 2.6
