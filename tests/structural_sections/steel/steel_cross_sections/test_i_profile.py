"""Test suite for ISteelProfile."""

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.structural_sections.steel.steel_cross_sections.i_profile import IProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB


class TestISteelProfile:
    """Test suite for ISteelProfile."""

    def test_alias(self, h_profile: IProfile) -> None:
        """Test the alias of the I-profile."""
        expected_alias = "HEB360"
        assert h_profile.name == expected_alias

    def test_steel_volume_per_meter(self, h_profile: IProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 1.806e-2  # m³/m
        assert pytest.approx(h_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_area(self, h_profile: IProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 1.806e4  # mm²
        assert pytest.approx(h_profile.area, rel=1e-2) == expected_area

    @pytest.mark.slow
    def test_plot_ipe_profile(self, ipe_profile: IProfile) -> None:
        """Test the plot method for an IPE profile (ensure it runs without errors)."""
        fig: Figure = ipe_profile.plot()
        assert isinstance(fig, plt.Figure)

    @pytest.mark.slow
    def test_plot_h_profile(self, h_profile: IProfile) -> None:
        """Test the plot method for an H-shaped profile (ensure it runs without errors)."""
        fig: Figure = h_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, h_profile: IProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the I-profile shapes with mocked section properties."""
        fig: Figure = h_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, h_profile: IProfile) -> None:
        """Test the geometry of the I profile."""
        expected_geometry = h_profile.geometry
        assert expected_geometry is not None

    def test_get_profile_with_corrosion(self) -> None:
        """Test the HEB profile with 20 mm corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match="The profile has fully corroded."):
            IProfile.from_standard_profile(
                profile=HEB.HEB360,
                corrosion=20,  # mm
            )

    def test_corrosion_in_name(self) -> None:
        """Test that the name includes corrosion information."""
        i_profile_with_corrosion = IProfile.from_standard_profile(
            profile=HEB.HEB360,
            corrosion=2,  # mm
        )
        expected_name_with_corrosion = "HEB360 (corrosion: 2 mm)"
        assert i_profile_with_corrosion.name == expected_name_with_corrosion
