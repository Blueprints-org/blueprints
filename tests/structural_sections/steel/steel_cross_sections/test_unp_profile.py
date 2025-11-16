"""Test suite for UNPSteelProfile."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.unp import UNP
from blueprints.structural_sections.steel.steel_cross_sections.unp_profile import UNPSteelProfile


class TestUNPSteelProfile:
    """Test suite for UNPSteelProfile."""

    def test_alias(self, unp_profile: UNPSteelProfile) -> None:
        """Test the alias of the UNP-profile."""
        expected_alias = "UNP300"
        assert unp_profile.name == expected_alias

    def test_steel_volume_per_meter(self, unp_profile: UNPSteelProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 5.880e-3  # m³/m
        assert pytest.approx(unp_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_weight_per_meter(self, unp_profile: UNPSteelProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight = 5.880e-3 * 7850  # kg/m
        assert pytest.approx(unp_profile.weight_per_meter, rel=1e-2) == expected_weight

    def test_steel_area(self, unp_profile: UNPSteelProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 5.880e3  # mm²
        assert pytest.approx(unp_profile.area, rel=1e-2) == expected_area

    @pytest.mark.slow
    def test_plot_unp_profile(self, unp_profile: UNPSteelProfile) -> None:
        """Test the plot method for a UNP profile (ensure it runs without errors)."""
        fig: Figure = unp_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, unp_profile: UNPSteelProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the UNP-profile shapes with mocked section properties."""
        fig: Figure = unp_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, unp_profile: UNPSteelProfile) -> None:
        """Test the geometry of the UNP profile."""
        expected_geometry = unp_profile.geometry
        assert expected_geometry is not None

    def test_get_profile_with_corrosion(self) -> None:
        """Test the UNP profile with 20 mm corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            UNPSteelProfile.from_standard_profile(
                profile=UNP.UNP300,
                steel_material=SteelMaterial(SteelStrengthClass.S355),
                corrosion=20,  # mm
            )

    def test_corrosion_in_name(self) -> None:
        """Test that the name includes corrosion information."""
        unp_profile_with_corrosion = UNPSteelProfile.from_standard_profile(
            profile=UNP.UNP300,
            steel_material=SteelMaterial(SteelStrengthClass.S355),
            corrosion=2,  # mm
        )
        expected_name_with_corrosion = "UNP300 (corrosion: 2 mm)"
        assert unp_profile_with_corrosion.name == expected_name_with_corrosion
