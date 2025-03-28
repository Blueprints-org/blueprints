"""Test for the HEAProfile enum."""

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.hea import HEAProfile


class TestHEAProfile:
    """Tests for the HEAProfile enum."""

    def test_enum_values(self) -> None:
        """Test that enum values are correctly defined."""
        assert HEAProfile.HEA_100.value == ("HEA100", 96, 100, 5, 8, 12)
        assert HEAProfile.HEA_200.value == ("HEA200", 190, 200, 6.5, 10, 18)

    def test_enum_membership(self) -> None:
        """Test that specific values are members of the enum."""
        assert "HEA100" in [e.value[0] for e in HEAProfile]
        assert "HEA200" in [e.value[0] for e in HEAProfile]

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique."""
        values = [e.value for e in HEAProfile]
        assert len(values) == len(set(values))

    def test_enum_attributes(self) -> None:
        """Test that enum attributes are correctly assigned."""
        profile = HEAProfile.HEA_100
        assert profile.code == "HEA100"
        assert profile.h == 96
        assert profile.b == 100
        assert profile.t_w == 5
        assert profile.t_f == 8
        assert profile.radius == 12
