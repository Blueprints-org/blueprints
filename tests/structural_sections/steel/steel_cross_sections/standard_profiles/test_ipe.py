"""Test the IPE enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.ipe import IPE


class TestIPE:
    """Tests for the IPE enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert IPE.IPE80.value == ("IPE80", 80, 46, 3.8, 5.2, 5)
        assert IPE.IPE600.value == ("IPE600", 600, 220, 12.0, 19.0, 24)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "IPE80" in [e.value[0] for e in IPE]
        assert "IPE600" in [e.value[0] for e in IPE]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in IPE]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = IPE.IPE80
        assert profile.alias == "IPE80"
        assert profile.total_height == 80
        assert profile.top_flange_width == 46
        assert profile.top_flange_thickness == 5.2
        assert profile.bottom_flange_width == 46
        assert profile.bottom_flange_thickness == 5.2
        assert profile.web_thickness == 3.8
        assert profile.top_radius == 5
        assert profile.bottom_radius == 5
