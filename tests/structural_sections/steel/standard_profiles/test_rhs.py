"""Test the RHS enum."""

from blueprints.structural_sections.steel.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.steel_profile_sections.rhs_profile import RHSProfile


class TestRHS:
    """Tests for the RHS enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert RHS.RHS50x30_2_6.value == ("RHS50x30x2.6", 50, 30, 2.6, 3.9, 2.6)
        assert RHS.RHS500x300_20.value == ("RHS500x300x20", 500, 300, 20, 30, 20)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "RHS50x30x2.6" in [e.value[0] for e in RHS]
        assert "RHS500x300x20" in [e.value[0] for e in RHS]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in RHS]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = RHS.RHS50x30_2_6
        assert profile.alias == "RHS50x30x2.6"
        assert profile.total_height == 50
        assert profile.total_width == 30
        assert profile.thickness == 2.6
        assert profile.outer_radius == 3.9
        assert profile.inner_radius == 2.6

    def test_as_cross_section(self) -> None:
        """Test that the as_cross_section method returns an RHSProfile instance."""
        profile = RHS.RHS50x30_2_6
        cross_section = profile.as_cross_section()

        assert isinstance(cross_section, RHSProfile)
        assert cross_section.total_width == profile.total_width
        assert cross_section.total_height == profile.total_height
        assert cross_section.left_wall_thickness == profile.thickness
        assert cross_section.right_wall_thickness == profile.thickness
        assert cross_section.top_wall_thickness == profile.thickness
        assert cross_section.bottom_wall_thickness == profile.thickness
        assert cross_section.top_left_outer_radius == profile.outer_radius
        assert cross_section.top_left_inner_radius == profile.inner_radius

    def test_as_cross_section_with_corrosion(self) -> None:
        """Test that the as_cross_section method accounts for corrosion."""
        profile = RHS.RHS50x30_2_6
        corrosion_outside = 0.4
        corrosion_inside = 0.2
        cross_section = profile.as_cross_section(corrosion_outside=corrosion_outside, corrosion_inside=corrosion_inside)

        expected_thickness = profile.thickness - corrosion_outside - corrosion_inside

        assert isinstance(cross_section, RHSProfile)
        assert cross_section.total_width == profile.total_width - 2 * corrosion_outside
        assert cross_section.total_height == profile.total_height - 2 * corrosion_outside
        assert cross_section.left_wall_thickness == expected_thickness
        assert cross_section.right_wall_thickness == expected_thickness
        assert cross_section.top_wall_thickness == expected_thickness
        assert cross_section.bottom_wall_thickness == expected_thickness
        assert cross_section.top_left_outer_radius == max(profile.outer_radius - corrosion_outside, 0)
        assert cross_section.top_left_inner_radius == profile.inner_radius + corrosion_inside
