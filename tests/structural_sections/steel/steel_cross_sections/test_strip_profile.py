"""Test suite for StripSteelProfile."""

from unittest.mock import MagicMock

import matplotlib.pyplot as plt
import pytest

from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import StripProfile


class TestStripSteelProfile:
    """Test suite for StripSteelProfile."""

    def test_code(self, strip_profile: StripProfile) -> None:
        """Test the code of the Strip profile."""
        expected_alias = "160x5"
        assert strip_profile.name == expected_alias

    def test_steel_volume_per_meter(self, strip_profile: StripProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 0.160 * 0.005  # m³/m
        assert pytest.approx(strip_profile.volume_per_meter, rel=1e-6) == expected_volume

    def test_area(self, strip_profile: StripProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 160 * 5  # mm²
        assert pytest.approx(strip_profile.area, rel=1e-6) == expected_area

    @pytest.mark.slow
    def test_plot(self, strip_profile: StripProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig = strip_profile.plot(show=False, include_moment_of_inertia=True)
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, strip_profile: StripProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the Strip profile shapes with mocked section properties."""
        fig = strip_profile.plot(show=False)
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, strip_profile: StripProfile) -> None:
        """Test the geometry of the Strip profile."""
        expected_geometry = strip_profile._geometry  # noqa: SLF001
        assert expected_geometry is not None

    def test_get_profile_with_corrosion(self) -> None:
        """Test the Strip profile with 2 mm corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match="The profile has fully corroded."):
            StripProfile.from_standard_profile(
                profile=Strip.STRIP160x5,
                corrosion=2.5,
            )

    def test_corrosion_in_name(self, strip_profile: StripProfile) -> None:
        """Test that the corrosion is included in the profile name."""
        profile_with_corrosion = StripProfile.from_standard_profile(
            profile=Strip.STRIP160x5,
            corrosion=1,
        )
        expected_name = f"{strip_profile.name} (corrosion: 1 mm)"
        assert profile_with_corrosion.name == expected_name

    def test_immutability(self, strip_profile: StripProfile) -> None:
        """Test that the StripProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            strip_profile.name = "New Name"  # type: ignore[misc]
