"""Test the SHSCFStandardProfileClass enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shscf import SHSCFStandardProfileClass


class TestSHSCFStandardProfileClass:
    """Tests for the SHSCFStandardProfileClass enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert SHSCFStandardProfileClass.SHSCF_40_2.value == ("SHSCF40/2", 40, 2, 4, 2)
        assert SHSCFStandardProfileClass.SHSCF_100_10.value == ("SHSCF100/10", 100, 10, 25, 15)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "SHSCF40/2" in [e.value[0] for e in SHSCFStandardProfileClass]
        assert "SHSCF100/10" in [e.value[0] for e in SHSCFStandardProfileClass]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in SHSCFStandardProfileClass]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = SHSCFStandardProfileClass.SHSCF_40_2
        assert profile.code == "SHSCF40/2"
        assert profile.total_width == 40
        assert profile.total_height == 40
        assert profile.thickness == 2
        assert profile.outer_radius == 4
        assert profile.inner_radius == 2
