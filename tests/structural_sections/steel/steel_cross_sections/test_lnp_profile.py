"""Test suite for the LNPProfile class."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.lnp_profile import LNPProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.lnp import LNP


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

    def test_steel_weight_per_meter(self, lnp_profile: LNPProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight: float = lnp_profile.volume_per_meter * 7850  # kg/m
        assert pytest.approx(lnp_profile.weight_per_meter, rel=1e-2) == expected_weight

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
        expected_geometry = getattr(lnp_profile, "geometry", None)
        assert expected_geometry is not None

    def test_get_profile_with_corrosion(self) -> None:
        """Test the LNP profile with corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            LNPProfile.from_standard_profile(
                profile=LNP.LNP_100x50x6,
                steel_material=SteelMaterial(SteelStrengthClass.S355),
                corrosion=3,  # mm, fully corroded
            )

    def test_corrosion_in_name(self) -> None:
        """Test that the name includes corrosion information."""
        lnp_profile_with_corrosion = LNPProfile.from_standard_profile(
            profile=LNP.LNP_100x50x6,
            steel_material=SteelMaterial(SteelStrengthClass.S355),
            corrosion=2,  # mm
        )
        expected_name_with_corrosion = "LNP 100x50x6 (corrosion: 2 mm)"
        assert lnp_profile_with_corrosion.name == expected_name_with_corrosion

    def test_custom_profile(self) -> None:
        """Test creating an LNPProfile with custom dimensions and default radii."""
        steel_material = SteelMaterial(SteelStrengthClass.S355)
        profile = LNPProfile(
            steel_material=steel_material,
            total_width=120,
            total_height=60,
            web_thickness=8,
            base_thickness=10,
            root_radius=None,
            back_radius=None,
            web_toe_radius=None,
            base_toe_radius=None,
            name="Custom LNP",
        )
        # Check that default radii are set correctly
        assert profile.root_radius == 8
        assert profile.back_radius == 16
        assert profile.web_toe_radius == 0
        assert profile.base_toe_radius == 0
