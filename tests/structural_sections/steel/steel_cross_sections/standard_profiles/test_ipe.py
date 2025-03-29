"""Test the IPEStandardProfileClass enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.ipe import IPEStandardProfileClass


class TestIPEStandardProfileClass:
    """Tests for the IPEStandardProfileClass enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert IPEStandardProfileClass.IPE_80.value == ("IPE80", 80, 46, 3.8, 5.2, 5)
        assert IPEStandardProfileClass.IPE_200.value == ("IPE200", 200, 100, 5.6, 8.5, 12)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "IPE80" in [e.value[0] for e in IPEStandardProfileClass]
        assert "IPE200" in [e.value[0] for e in IPEStandardProfileClass]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in IPEStandardProfileClass]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = IPEStandardProfileClass.IPE_80
        assert profile.code == "IPE80"
        assert profile.total_height == 80
        assert profile.top_flange_width == 46
        assert profile.top_flange_thickness == 5.2
        assert profile.bottom_flange_width == 46
        assert profile.bottom_flange_thickness == 5.2
        assert profile.web_thickness == 3.8
        assert profile.top_radius == 5
        assert profile.bottom_radius == 5
