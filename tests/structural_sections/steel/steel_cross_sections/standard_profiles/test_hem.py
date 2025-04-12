"""Unit tests for the HEM enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.hem import HEM


class TestHEM:
    """Tests for the HEM enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert HEM.HEM100.value == ("HEM100", 120, 106, 12, 20, 12)
        assert HEM.HEM1000.value == ("HEM1000", 1008, 302, 21, 40, 30)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "HEM100" in [e.value[0] for e in HEM]
        assert "HEM1000" in [e.value[0] for e in HEM]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in HEM]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = HEM.HEM100
        assert profile.alias == "HEM100"
        assert profile.total_height == 120
        assert profile.top_flange_width == 106
        assert profile.top_flange_thickness == 20
        assert profile.bottom_flange_width == 106
        assert profile.bottom_flange_thickness == 20
        assert profile.web_thickness == 12
        assert profile.top_radius == 12
        assert profile.bottom_radius == 12
