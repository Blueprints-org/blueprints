"""Test suite for ISteelProfile."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.structural_sections.steel.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.steel_profile_sections.i_profile import IProfile


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
        expected_geometry = h_profile._geometry  # noqa: SLF001
        assert expected_geometry is not None

    def test_get_profile_with_corrosion(self) -> None:
        """Test the HEB profile with 20 mm corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
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

    def test_immutability(self, h_profile: IProfile) -> None:
        """Test that the IProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            h_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, h_profile: IProfile) -> None:
        """Test the transform method of the I profile."""
        transformed_profile = h_profile.transform(horizontal_offset=1000, vertical_offset=500, rotation=90)
        assert transformed_profile is not None
        assert isinstance(transformed_profile, IProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == h_profile.centroid.x + 1000
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == h_profile.centroid.y + 500
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == h_profile.profile_width
