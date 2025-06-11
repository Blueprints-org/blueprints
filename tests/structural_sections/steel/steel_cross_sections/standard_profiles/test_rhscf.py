"""Test the RHSCF enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhscf import RHSCF


class TestRHSCF:
    """Tests for the RHSCF enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert RHSCF.RHSCF40x20_2.value == ("RHSCF40x20x2", 40, 20, 2, 4, 2)
        assert RHSCF.RHSCF400x300_16.value == ("RHSCF400x300x16", 400, 300, 16, 48, 32)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "RHSCF40x20x2" in [e.value[0] for e in RHSCF]
        assert "RHSCF400x300x16" in [e.value[0] for e in RHSCF]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in RHSCF]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = RHSCF.RHSCF40x20_2
        assert profile.alias == "RHSCF40x20x2"
        assert profile.total_height == 40
        assert profile.total_width == 20
        assert profile.thickness == 2
        assert profile.outer_radius == 4
        assert profile.inner_radius == 2
