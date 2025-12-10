"""Unit tests for the HEM enum."""

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.hem import HEM


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

    def test_as_cross_section(self) -> None:
        """Test that the as_cross_section method returns an IProfile instance."""
        profile = HEM.HEM100
        cross_section = profile.as_cross_section()

        assert isinstance(cross_section, IProfile)
        assert cross_section.top_flange_width == profile.top_flange_width
        assert cross_section.bottom_flange_width == profile.bottom_flange_width
        assert cross_section.total_height == profile.total_height
        assert cross_section.web_thickness == profile.web_thickness
        assert cross_section.top_radius == profile.top_radius
        assert cross_section.bottom_radius == profile.bottom_radius

    def test_as_cross_section_with_corrosion(self) -> None:
        """Test that the as_cross_section method accounts for corrosion."""
        profile = HEM.HEM100
        corrosion = 0.9
        cross_section = profile.as_cross_section(corrosion=corrosion)

        assert isinstance(cross_section, IProfile)
        assert cross_section.top_flange_width == profile.top_flange_width - 2 * corrosion
        assert cross_section.bottom_flange_width == profile.bottom_flange_width - 2 * corrosion
        assert cross_section.total_height == profile.total_height - 2 * corrosion
        assert cross_section.web_thickness == profile.web_thickness - 2 * corrosion
        assert cross_section.top_radius == profile.top_radius
        assert cross_section.bottom_radius == profile.bottom_radius
