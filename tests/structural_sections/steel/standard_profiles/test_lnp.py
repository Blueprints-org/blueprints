"""Test the LNP enum."""

from blueprints.structural_sections.steel.profile_definitions.lnp_profile import LNPProfile
from blueprints.structural_sections.steel.standard_profiles.lnp import LNP


class TestLNP:
    """Tests for the LNP enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert LNP.LNP_40x40x4.value == ("LNP 40x40x4", 40, 40, 4, 6, 3)
        assert LNP.LNP_200x100x16.value == ("LNP 200x100x16", 200, 100, 16, 15, 7.5)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "LNP 40x40x4" in [e.value[0] for e in LNP]
        assert "LNP 200x100x16" in [e.value[0] for e in LNP]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in LNP]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = LNP.LNP_60x40x7
        assert profile.alias == "LNP 60x40x7"
        assert profile.height == 60
        assert profile.width == 40
        assert profile.base_thickness == 7
        assert profile.web_thickness == 7
        assert profile.root_radius == 6
        assert profile.back_radius == 0
        assert profile.toe_radius == 3

    def test_as_cross_section(self) -> None:
        """Test that the as_cross_section method returns an LNPProfile instance."""
        profile = LNP.LNP_60x40x7
        cross_section = profile.as_cross_section()

        assert isinstance(cross_section, LNPProfile)
        assert cross_section.total_width == profile.width
        assert cross_section.total_height == profile.height
        assert cross_section.web_thickness == profile.web_thickness
        assert cross_section.base_thickness == profile.base_thickness
        assert cross_section.root_radius == profile.root_radius
        assert cross_section.back_radius == profile.back_radius
        assert cross_section.web_toe_radius == profile.toe_radius
        assert cross_section.base_toe_radius == profile.toe_radius

    def test_as_cross_section_with_corrosion(self) -> None:
        """Test that the as_cross_section method accounts for corrosion."""
        profile = LNP.LNP_60x40x7
        corrosion = 0.5
        cross_section = profile.as_cross_section(corrosion=corrosion)

        expected_thickness = profile.base_thickness - 2 * corrosion

        assert isinstance(cross_section, LNPProfile)
        assert cross_section.total_width == profile.width - 2 * corrosion
        assert cross_section.total_height == profile.height - 2 * corrosion
        assert cross_section.web_thickness == expected_thickness
        assert cross_section.base_thickness == expected_thickness
        assert cross_section.root_radius == profile.root_radius + corrosion
        assert cross_section.back_radius == profile.back_radius
        assert cross_section.web_toe_radius == max(profile.toe_radius - corrosion, 0)
        assert cross_section.base_toe_radius == max(profile.toe_radius - corrosion, 0)
