"""Test the SHS enum."""

from blueprints.structural_sections.steel.steel_cross_sections.rhs_profile import RHSProfile
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

    def test_as_cross_section(self) -> None:
        """Test that the as_cross_section method returns an RHSProfile instance."""
        profile = SHS.SHS_40_2_6
        cross_section = profile.as_cross_section()

        assert isinstance(cross_section, RHSProfile)
        assert cross_section.total_width == profile.total_width
        assert cross_section.total_height == profile.total_height
        assert cross_section.left_wall_thickness == profile.thickness
        assert cross_section.top_left_outer_radius == profile.outer_radius
        assert cross_section.top_left_inner_radius == profile.inner_radius

    def test_as_cross_section_with_corrosion(self) -> None:
        """Test that the as_cross_section method accounts for corrosion."""
        profile = SHS.SHS_40_2_6
        corrosion_outside = 0.3
        corrosion_inside = 0.1
        cross_section = profile.as_cross_section(corrosion_outside=corrosion_outside, corrosion_inside=corrosion_inside)

        expected_thickness = profile.thickness - corrosion_outside - corrosion_inside

        assert isinstance(cross_section, RHSProfile)
        assert cross_section.total_width == profile.total_width - 2 * corrosion_outside
        assert cross_section.total_height == profile.total_height - 2 * corrosion_outside
        assert cross_section.left_wall_thickness == expected_thickness
        assert cross_section.top_left_outer_radius == max(profile.outer_radius - corrosion_outside, 0)
        assert cross_section.top_left_inner_radius == profile.inner_radius + corrosion_inside
