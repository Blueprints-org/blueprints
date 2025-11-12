"""Test suite for StripSteelProfile."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import matplotlib.pyplot as plt
import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import StripSteelProfile


class TestStripSteelProfile:
    """Test suite for StripSteelProfile."""

    def test_code(self, strip_profile: StripSteelProfile) -> None:
        """Test the code of the Strip profile."""
        expected_alias = "160x5"
        assert strip_profile.name == expected_alias

    def test_steel_volume_per_meter(self, strip_profile: StripSteelProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 0.160 * 0.005  # m³/m
        assert pytest.approx(strip_profile.volume_per_meter, rel=1e-6) == expected_volume

    def test_steel_weight_per_meter(self, strip_profile: StripSteelProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight = 0.160 * 0.005 * 7850  # kg/m
        assert pytest.approx(strip_profile.weight_per_meter, rel=1e-6) == expected_weight

    def test_area(self, strip_profile: StripSteelProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 160 * 5  # mm²
        assert pytest.approx(strip_profile.area, rel=1e-6) == expected_area

    @pytest.mark.slow
    def test_plot(self, strip_profile: StripSteelProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig = strip_profile.plot(show=False)
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, strip_profile: StripSteelProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the Strip profile shapes with mocked section properties."""
        fig = strip_profile.plot(show=False)
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, strip_profile: StripSteelProfile) -> None:
        """Test the geometry of the Strip profile."""
        expected_geometry = strip_profile.geometry
        assert expected_geometry is not None

    def test_yield_strength(self, strip_profile: StripSteelProfile) -> None:
        """Test the yield strength of the Strip profile."""
        assert strip_profile.yield_strength == 355

    def test_ultimate_strength(self, strip_profile: StripSteelProfile) -> None:
        """Test the ultimate strength of the Strip profile."""
        assert strip_profile.ultimate_strength == 490

    def test_get_profile_with_corrosion(self) -> None:
        """Test the Strip profile with 2 mm corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            StripSteelProfile.from_standard_profile(
                profile=Strip.STRIP160x5,
                steel_material=SteelMaterial(SteelStrengthClass.S355),
                corrosion=2.5,
            )

    def test_corrosion_in_name(self, strip_profile: StripSteelProfile) -> None:
        """Test that the corrosion is included in the profile name."""
        profile_with_corrosion = StripSteelProfile.from_standard_profile(
            profile=Strip.STRIP160x5,
            steel_material=SteelMaterial(SteelStrengthClass.S355),
            corrosion=1,
        )
        expected_name = f"{strip_profile.name} (corrosion: 1 mm)"
        assert profile_with_corrosion.name == expected_name
