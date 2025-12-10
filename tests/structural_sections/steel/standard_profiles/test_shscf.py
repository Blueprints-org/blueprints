"""Test the SHSCF enum."""

from blueprints.structural_sections.steel.profile_definitions.rhs_profile import RHSProfile
from blueprints.structural_sections.steel.standard_profiles.shscf import SHSCF


class TestSHSCF:
    """Tests for the SHSCF enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert SHSCF.SHSCF_20_2.value == ("SHSCF20x2", 20, 2, 4, 2)
        assert SHSCF.SHSCF_600_20.value == ("SHSCF600x20", 600, 20, 60, 40)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "SHSCF20x2" in [e.value[0] for e in SHSCF]
        assert "SHSCF600x20" in [e.value[0] for e in SHSCF]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in SHSCF]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = SHSCF.SHSCF_20_2
        assert profile.alias == "SHSCF20x2"
        assert profile.total_width == 20
        assert profile.total_height == 20
        assert profile.thickness == 2
        assert profile.outer_radius == 4
        assert profile.inner_radius == 2

    def test_as_cross_section(self) -> None:
        """Test that the as_cross_section method returns an RHSProfile instance."""
        profile = SHSCF.SHSCF_20_2
        cross_section = profile.as_cross_section()

        assert isinstance(cross_section, RHSProfile)
        assert cross_section.total_width == profile.total_width
        assert cross_section.total_height == profile.total_height
        assert cross_section.left_wall_thickness == profile.thickness
        assert cross_section.top_left_outer_radius == profile.outer_radius
        assert cross_section.top_left_inner_radius == profile.inner_radius

    def test_as_cross_section_with_corrosion(self) -> None:
        """Test that the as_cross_section method accounts for corrosion."""
        profile = SHSCF.SHSCF_20_2
        corrosion_outside = 0.2
        corrosion_inside = 0.1
        cross_section = profile.as_cross_section(corrosion_outside=corrosion_outside, corrosion_inside=corrosion_inside)

        expected_thickness = profile.thickness - corrosion_outside - corrosion_inside

        assert isinstance(cross_section, RHSProfile)
        assert cross_section.total_width == profile.total_width - 2 * corrosion_outside
        assert cross_section.total_height == profile.total_height - 2 * corrosion_outside
        assert cross_section.left_wall_thickness == expected_thickness
        assert cross_section.top_left_outer_radius == max(profile.outer_radius - corrosion_outside, 0)
        assert cross_section.top_left_inner_radius == profile.inner_radius + corrosion_inside
