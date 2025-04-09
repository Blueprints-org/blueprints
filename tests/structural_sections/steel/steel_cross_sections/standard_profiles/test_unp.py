"""Test for the UNP enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.unp import UNP


class TestUNP:
    """Tests for the UNP enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert UNP.UNP_80.value == ("UNP80", 80, 45, 6, 8, 8)
        assert UNP.UNP_200.value == ("UNP200", 200, 75, 8.5, 11.5, 11.5)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "UNP80" in [e.value[0] for e in UNP]
        assert "UNP200" in [e.value[0] for e in UNP]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in UNP]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = UNP.UNP_80
        assert profile.top_flange_total_width == 45
        assert profile.top_flange_thickness == 8
        assert profile.bottom_flange_total_width == 45
        assert profile.bottom_flange_thickness == 8
        assert profile.total_height == 80
        assert profile.web_thickness == 6
        assert profile.radius == 8
