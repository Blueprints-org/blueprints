"""Test the SHSCF enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shscf import SHSCF


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
