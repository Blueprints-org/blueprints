"""Test for the HEA enum."""

from blueprints.structural_sections.steel.standard_profiles.hea import HEA
from blueprints.structural_sections.steel.steel_profile_sections.i_profile import IProfile


class TestHEA:
    """Tests for the HEA enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert HEA.HEA100.value == ("HEA100", 96, 100, 5, 8, 12)
        assert HEA.HEA1000.value == ("HEA1000", 990, 300, 16.5, 31, 30)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "HEA100" in [e.value[0] for e in HEA]
        assert "HEA1000" in [e.value[0] for e in HEA]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in HEA]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = HEA.HEA100
        assert profile.alias == "HEA100"
        assert profile.top_flange_width == 100
        assert profile.top_flange_thickness == 8
        assert profile.bottom_flange_width == 100
        assert profile.bottom_flange_thickness == 8
        assert profile.total_height == 96
        assert profile.web_thickness == 5
        assert profile.top_radius == 12
        assert profile.bottom_radius == 12

    def test_as_cross_section(self) -> None:
        """Test that the as_cross_section method returns an IProfile instance."""
        profile = HEA.HEA100
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
        profile = HEA.HEA100
        corrosion = 0.8
        cross_section = profile.as_cross_section(corrosion=corrosion)

        assert isinstance(cross_section, IProfile)
        assert cross_section.top_flange_width == profile.top_flange_width - 2 * corrosion
        assert cross_section.bottom_flange_width == profile.bottom_flange_width - 2 * corrosion
        assert cross_section.total_height == profile.total_height - 2 * corrosion
        assert cross_section.web_thickness == profile.web_thickness - 2 * corrosion
        assert cross_section.top_radius == profile.top_radius
        assert cross_section.bottom_radius == profile.bottom_radius
