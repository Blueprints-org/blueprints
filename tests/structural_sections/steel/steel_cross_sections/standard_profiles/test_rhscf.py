"""Test the RHSCF enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhscf import RHSCF


class TestRHSCF:
    """Tests for the RHSCF enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert RHSCF.RHSCF50x30_2_5.value == ("RHSCF50x30/2.5", 50, 30, 2.5, 5, 2.5)
        assert RHSCF.RHSCF100x60_6_3.value == ("RHSCF100x60/6.3", 100, 60, 6.3, 15.8, 9.4)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "RHSCF50x30/2.5" in [e.value[0] for e in RHSCF]
        assert "RHSCF100x60/6.3" in [e.value[0] for e in RHSCF]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in RHSCF]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = RHSCF.RHSCF50x30_2_5
        assert profile.code == "RHSCF50x30/2.5"
        assert profile.total_height == 50
        assert profile.total_width == 30
        assert profile.thickness == 2.5
        assert profile.outer_radius == 5
        assert profile.inner_radius == 2.5
