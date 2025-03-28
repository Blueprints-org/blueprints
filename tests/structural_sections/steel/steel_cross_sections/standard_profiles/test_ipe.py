"""Test the IPEProfile enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.ipe import IPEProfile


class TestIPEProfile:
    """Tests for the IPEProfile enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert IPEProfile.IPE_80.value == ("IPE80", 80, 46, 3.8, 5.2, 5)
        assert IPEProfile.IPE_200.value == ("IPE200", 200, 100, 5.6, 8.5, 12)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "IPE80" in [e.value[0] for e in IPEProfile]
        assert "IPE200" in [e.value[0] for e in IPEProfile]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in IPEProfile]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = IPEProfile.IPE_80
        assert profile.code == "IPE80"
        assert profile.h == 80
        assert profile.b == 46
        assert profile.t_w == 3.8
        assert profile.t_f == 5.2
        assert profile.radius == 5
