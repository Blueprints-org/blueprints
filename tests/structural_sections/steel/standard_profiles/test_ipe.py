"""Test the IPE enum."""

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.ipe import IPE


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
        assert profile.name == "IPE80"
        assert profile.total_height == 80
        assert profile.top_flange_width == 46
        assert profile.top_flange_thickness == 5.2
        assert profile.bottom_flange_width == 46
        assert profile.bottom_flange_thickness == 5.2
        assert profile.web_thickness == 3.8
        assert profile.top_radius == 5
        assert profile.bottom_radius == 5

    def test_as_cross_section(self) -> None:
        """Test that the as_cross_section method returns an IProfile instance."""
        profile = IPE.IPE80
        cross_section = profile

        assert isinstance(cross_section, IProfile)
        assert cross_section.top_flange_width == profile.top_flange_width
        assert cross_section.bottom_flange_width == profile.bottom_flange_width
        assert cross_section.total_height == profile.total_height
        assert cross_section.web_thickness == profile.web_thickness
        assert cross_section.top_radius == profile.top_radius
        assert cross_section.bottom_radius == profile.bottom_radius
        assert cross_section.area > 0

    def test_as_cross_section_with_corrosion(self) -> None:
        """Test that the as_cross_section method accounts for corrosion."""
        profile = IPE.IPE80
        corrosion = 1.2
        cross_section = profile.as_cross_section(corrosion=corrosion)

        assert isinstance(cross_section, IProfile)
        assert cross_section.top_flange_width == profile.top_flange_width - 2 * corrosion
        assert cross_section.bottom_flange_width == profile.bottom_flange_width - 2 * corrosion
        assert cross_section.total_height == profile.total_height - 2 * corrosion
        assert cross_section.web_thickness == profile.web_thickness - 2 * corrosion
        assert cross_section.top_radius == profile.top_radius
        assert cross_section.bottom_radius == profile.bottom_radius
