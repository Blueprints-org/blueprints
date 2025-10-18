"""Test suite for the LNPProfile class."""

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.structural_sections.steel.steel_cross_sections.lnp_profile import LNPProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.lnp import LNP
from blueprints.validations import NegativeValueError


class TestLNPProfile:
    """Test suite for LNPProfile."""

    def test_name(self, lnp_profile: LNPProfile) -> None:
        """Test the name of the LNP profile."""
        expected_name: str = "LNP 100x50x6"
        assert lnp_profile.name == expected_name

    def test_steel_volume_per_meter(self, lnp_profile: LNPProfile) -> None:
        """Test the steel volume per meter."""
        # Expected volume per meter calculated analytically for LNP 100x50x6: (area 871 mm² = 0.000871 m²) × 1 m = 0.000871 m³/m
        expected_volume: float = 0.000871  # m³/m
        assert pytest.approx(lnp_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_area(self, lnp_profile: LNPProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area: float = 871  # mm²
        assert pytest.approx(lnp_profile.area, rel=1e-2) == expected_area

    @pytest.mark.slow
    def test_plot(self, lnp_profile: LNPProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig: Figure = lnp_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, lnp_profile: LNPProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the LNP profile shapes with mocked section properties."""
        fig: Figure = lnp_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, lnp_profile: LNPProfile) -> None:
        """Test the geometry of the LNP profile."""
        expected_geometry = lnp_profile._geometry  # noqa: SLF001
        assert expected_geometry is not None

    def test_get_profile_with_corrosion(self) -> None:
        """Test the LNP profile with corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match="The profile has fully corroded."):
            LNPProfile.from_standard_profile(
                profile=LNP.LNP_100x50x6,
                corrosion=3,  # mm, fully corroded
            )

    def test_corrosion_in_name(self) -> None:
        """Test that the name includes corrosion information."""
        lnp_profile_with_corrosion = LNPProfile.from_standard_profile(
            profile=LNP.LNP_100x50x6,
            corrosion=2,  # mm
        )
        expected_name_with_corrosion = "LNP 100x50x6 (corrosion: 2 mm)"
        assert lnp_profile_with_corrosion.name == expected_name_with_corrosion

    def test_custom_profile(self) -> None:
        """Test creating an LNPProfile with custom dimensions."""
        profile = LNPProfile(
            total_width=120,
            total_height=60,
            web_thickness=8,
            base_thickness=10,
            root_radius=5,
            back_radius=0,
            web_toe_radius=4,
            base_toe_radius=5,
            name="Custom LNP",
        )
        # Check that default radii are set correctly
        assert profile.area > 0

    def test_invalid_dimensions(self) -> None:
        """Test that invalid dimensions raise errors."""
        # Case with negative web toe straight part
        with pytest.raises(NegativeValueError, match=r"(?i) 'web_toe_straight_part' cannot be negative"):
            LNPProfile(
                total_width=100,
                total_height=50,
                web_thickness=6,
                base_thickness=6,
                root_radius=3,
                back_radius=6,
                web_toe_radius=7,
                base_toe_radius=0,
            )
        # Case with negative base toe straight part
        with pytest.raises(NegativeValueError, match=r"(?i) 'base_toe_straight_part' cannot be negative"):
            LNPProfile(
                total_width=100,
                total_height=0,
                web_thickness=6,
                base_thickness=6,
                root_radius=3,
                back_radius=3,
                web_toe_radius=0,
                base_toe_radius=7,
            )
        # Case with negative base inner width
        with pytest.raises(NegativeValueError, match=r"(?i) 'base_inner_width' cannot be negative"):
            LNPProfile(
                total_width=20,
                total_height=100,
                web_thickness=10,
                base_thickness=8,
                root_radius=6,
                back_radius=3,
                web_toe_radius=0,
                base_toe_radius=6,
            )
        # Case with negative web inner height
        with pytest.raises(NegativeValueError, match=r"(?i) 'web_inner_height' cannot be negative"):
            LNPProfile(
                total_width=100,
                total_height=30,
                web_thickness=12,
                base_thickness=15,
                root_radius=10,
                back_radius=0,
                web_toe_radius=10,
                base_toe_radius=6,
            )
