"""Unit tests for the HEMProfile enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.hem import HEMProfile


class TestHEMProfile:
    """Tests for the HEMProfile enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert HEMProfile.HEM_100.value == ("HEM100", 120, 106, 12, 20, 12)
        assert HEMProfile.HEM_200.value == ("HEM200", 220, 206, 15, 25, 18)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "HEM100" in [e.value[0] for e in HEMProfile]
        assert "HEM200" in [e.value[0] for e in HEMProfile]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in HEMProfile]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = HEMProfile.HEM_100
        assert profile.code == "HEM100"
        assert profile.h == 120
        assert profile.b == 106
        assert profile.t_w == 12
        assert profile.t_f == 20
        assert profile.radius == 12
