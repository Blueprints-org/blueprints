"""Test suite for StripSteelProfile."""

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

    def test_centroid(self, strip_profile: StripSteelProfile) -> None:
        """Test the centroid of the steel cross-section."""
        expected_centroid = (0, 0)  # (x, y) coordinates
        assert pytest.approx(strip_profile.centroid.x, rel=1e-6) == expected_centroid[0]
        assert pytest.approx(strip_profile.centroid.y, rel=1e-6) == expected_centroid[1]

    def test_moment_of_inertia_about_y(self, strip_profile: StripSteelProfile) -> None:
        """Test the moment of inertia about the y-axis."""
        expected_moi_y = 1 / 12 * 160 * 5**3  # mm⁴
        assert pytest.approx(strip_profile.moment_of_inertia_about_y, rel=1e-6) == expected_moi_y

    def test_moment_of_inertia_about_z(self, strip_profile: StripSteelProfile) -> None:
        """Test the moment of inertia about the z-axis."""
        expected_moi_z = 1 / 12 * 160**3 * 5  # mm⁴
        assert pytest.approx(strip_profile.moment_of_inertia_about_z, rel=1e-6) == expected_moi_z

    def test_elastic_section_modulus_about_y_positive(self, strip_profile: StripSteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the positive z side."""
        expected_modulus_y_positive = 1 / 6 * 160 * 5**2  # mm³
        assert pytest.approx(strip_profile.elastic_section_modulus_about_y_positive, rel=1e-6) == expected_modulus_y_positive

    def test_elastic_section_modulus_about_y_negative(self, strip_profile: StripSteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the negative z side."""
        expected_modulus_y_negative = 1 / 6 * 160 * 5**2  # mm³
        assert pytest.approx(strip_profile.elastic_section_modulus_about_y_negative, rel=1e-6) == expected_modulus_y_negative

    def test_elastic_section_modulus_about_z_positive(self, strip_profile: StripSteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the positive y side."""
        expected_modulus_z_positive = 1 / 6 * 160**2 * 5  # mm³
        assert pytest.approx(strip_profile.elastic_section_modulus_about_z_positive, rel=1e-6) == expected_modulus_z_positive

    def test_elastic_section_modulus_about_z_negative(self, strip_profile: StripSteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the negative y side."""
        expected_modulus_z_negative = 1 / 6 * 160**2 * 5  # mm³
        assert pytest.approx(strip_profile.elastic_section_modulus_about_z_negative, rel=1e-6) == expected_modulus_z_negative

    def test_plot(self, strip_profile: StripSteelProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig = strip_profile.plot(show=False)
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, strip_profile: StripSteelProfile) -> None:
        """Test the geometry of the Strip profile."""
        expected_geometry = strip_profile.geometry
        assert expected_geometry is not None

    def test_section_properties(self, strip_profile: StripSteelProfile) -> None:
        """Test the section properties of the Strip profile."""
        section_properties = strip_profile.section_properties()
        assert section_properties.mass == pytest.approx(expected=strip_profile.area, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=strip_profile.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=strip_profile.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=strip_profile.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=strip_profile.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(expected=strip_profile.elastic_section_modulus_about_y_positive, rel=1e-2)
        assert section_properties.zyy_plus == pytest.approx(expected=strip_profile.elastic_section_modulus_about_z_positive, rel=1e-2)
        assert section_properties.zxx_minus == pytest.approx(expected=strip_profile.elastic_section_modulus_about_y_negative, rel=1e-2)
        assert section_properties.zyy_minus == pytest.approx(expected=strip_profile.elastic_section_modulus_about_z_negative, rel=1e-2)

    def test_yield_strength(self, strip_profile: StripSteelProfile) -> None:
        """Test the yield strength of the Strip profile."""
        assert strip_profile.yield_strength == 355

    def test_ultimate_strength(self, strip_profile: StripSteelProfile) -> None:
        """Test the ultimate strength of the Strip profile."""
        assert strip_profile.ultimate_strength == 490

    def test_plastic_section_modulus_about_y(self, strip_profile: StripSteelProfile) -> None:
        """Test the plastic section modulus about the y-axis."""
        expected_plastic_modulus_y = 1 / 4 * 160 * 5**2
        assert pytest.approx(strip_profile.plastic_section_modulus_about_y, rel=1e-6) == expected_plastic_modulus_y

    def test_plastic_section_modulus_about_z(self, strip_profile: StripSteelProfile) -> None:
        """Test the plastic section modulus about the z-axis."""
        expected_plastic_modulus_z = 1 / 4 * 5 * 160**2
        assert pytest.approx(strip_profile.plastic_section_modulus_about_z, rel=1e-6) == expected_plastic_modulus_z

    def test_get_profile_with_corrosion(self) -> None:
        """Test the Strip profile with 2 mm corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match="The profile has fully corroded."):
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
