"""Test for the UNPStandardProfileClass enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.unp import UNPStandardProfileClass


class TestUNPStandardProfileClass:
    """Tests for the UNPStandardProfileClass enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert UNPStandardProfileClass.UNP_80.value == ("UNP80", 80, 45, 6, 8, 8)
        assert UNPStandardProfileClass.UNP_200.value == ("UNP200", 200, 75, 8.5, 11.5, 11.5)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "UNP80" in [e.value[0] for e in UNPStandardProfileClass]
        assert "UNP200" in [e.value[0] for e in UNPStandardProfileClass]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in UNPStandardProfileClass]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = UNPStandardProfileClass.UNP_80
        assert profile.code == "UNP80"
        assert profile.h == 80
        assert profile.b == 45
        assert profile.t_w == 6
        assert profile.t_f == 8
        assert profile.radius == 8
