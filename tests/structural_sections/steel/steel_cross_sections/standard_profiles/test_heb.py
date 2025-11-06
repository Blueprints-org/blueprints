"""Test the HEB enum."""

from blueprints.structural_sections.steel.steel_cross_sections.i_profile import IProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB


class TestHEB:
    """Tests for the HEB enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert HEB.HEB100.value == ("HEB100", 100, 100, 6, 10, 12)
        assert HEB.HEB1000.value == ("HEB1000", 1000, 300, 19, 36, 30)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "HEB100" in [e.value[0] for e in HEB]
        assert "HEB1000" in [e.value[0] for e in HEB]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in HEB]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = HEB.HEB100
        assert profile.alias == "HEB100"
        assert profile.total_height == 100
        assert profile.top_flange_width == 100
        assert profile.top_flange_thickness == 10
        assert profile.bottom_flange_width == 100
        assert profile.bottom_flange_thickness == 10
        assert profile.web_thickness == 6
        assert profile.top_radius == 12
        assert profile.bottom_radius == 12

    def test_as_cross_section(self) -> None:
        """Test that the as_cross_section method returns an IProfile instance."""
        profile = HEB.HEB100
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
        profile = HEB.HEB100
        corrosion = 1.0
        cross_section = profile.as_cross_section(corrosion=corrosion)

        assert isinstance(cross_section, IProfile)
        assert cross_section.top_flange_width == profile.top_flange_width - 2 * corrosion
        assert cross_section.bottom_flange_width == profile.bottom_flange_width - 2 * corrosion
        assert cross_section.total_height == profile.total_height - 2 * corrosion
        assert cross_section.web_thickness == profile.web_thickness - 2 * corrosion
        assert cross_section.top_radius == profile.top_radius
        assert cross_section.bottom_radius == profile.bottom_radius
