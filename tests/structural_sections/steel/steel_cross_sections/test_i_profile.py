"""Test suite for ISteelProfile."""

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import ISteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB


class TestISteelProfile:
    """Test suite for ISteelProfile."""

    def test_alias(self, i_profile: ISteelProfile) -> None:
        """Test the alias of the I-profile."""
        expected_alias = "HEB360"
        assert i_profile.name == expected_alias

    def test_steel_volume_per_meter(self, i_profile: ISteelProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 1.806e-2  # m³/m
        assert pytest.approx(i_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_weight_per_meter(self, i_profile: ISteelProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight = 1.806e-2 * 7850  # kg/m
        assert pytest.approx(i_profile.weight_per_meter, rel=1e-2) == expected_weight

    def test_steel_area(self, i_profile: ISteelProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 1.806e4  # mm²
        assert pytest.approx(i_profile.area, rel=1e-2) == expected_area

    def test_centroid(self, i_profile: ISteelProfile) -> None:
        """Test the centroid of the steel cross-section."""
        expected_centroid = (0, 0)  # (x, y) coordinates
        assert pytest.approx(i_profile.centroid.x, rel=1e-2) == expected_centroid[0]
        assert pytest.approx(i_profile.centroid.y, rel=1e-2) == expected_centroid[1]

    def test_moment_of_inertia_about_y(self, i_profile: ISteelProfile) -> None:
        """Test the moment of inertia about the y-axis."""
        expected_moi_y = 4.319e8  # mm⁴
        assert pytest.approx(i_profile.moment_of_inertia_about_y, rel=1e-2) == expected_moi_y

    def test_moment_of_inertia_about_z(self, i_profile: ISteelProfile) -> None:
        """Test the moment of inertia about the z-axis."""
        expected_moi_z = 1.014e8  # mm⁴
        assert pytest.approx(i_profile.moment_of_inertia_about_z, rel=1e-2) == expected_moi_z

    def test_elastic_section_modulus_about_y_positive(self, i_profile: ISteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the positive z side."""
        expected_modulus_y_positive = 2.4e6  # mm³
        assert pytest.approx(i_profile.elastic_section_modulus_about_y_positive, rel=1e-2) == expected_modulus_y_positive

    def test_elastic_section_modulus_about_y_negative(self, i_profile: ISteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the negative z side."""
        expected_modulus_y_negative = 2.4e6  # mm³
        assert pytest.approx(i_profile.elastic_section_modulus_about_y_negative, rel=1e-2) == expected_modulus_y_negative

    def test_elastic_section_modulus_about_z_positive(self, i_profile: ISteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the positive y side."""
        expected_modulus_z_positive = 6.761e5  # mm³
        assert pytest.approx(i_profile.elastic_section_modulus_about_z_positive, rel=1e-2) == expected_modulus_z_positive

    def test_elastic_section_modulus_about_z_negative(self, i_profile: ISteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the negative y side."""
        expected_modulus_z_negative = 6.761e5  # mm³
        assert pytest.approx(i_profile.elastic_section_modulus_about_z_negative, rel=1e-2) == expected_modulus_z_negative

    def test_plot(self, i_profile: ISteelProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig: Figure = i_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, i_profile: ISteelProfile) -> None:
        """Test the geometry of the I profile."""
        expected_geometry = i_profile.geometry
        assert expected_geometry is not None

    def test_section_properties(self, i_profile: ISteelProfile) -> None:
        """Test the section properties of the I profile."""
        section_properties = i_profile.section_properties()
        assert section_properties.mass == pytest.approx(expected=i_profile.area, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=i_profile.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=i_profile.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=i_profile.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=i_profile.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(expected=i_profile.elastic_section_modulus_about_y_positive, rel=1e-2)
        assert section_properties.zyy_plus == pytest.approx(expected=i_profile.elastic_section_modulus_about_z_positive, rel=1e-2)
        assert section_properties.zxx_minus == pytest.approx(expected=i_profile.elastic_section_modulus_about_y_negative, rel=1e-2)
        assert section_properties.zyy_minus == pytest.approx(expected=i_profile.elastic_section_modulus_about_z_negative, rel=1e-2)

    def test_get_profile_with_corrosion(self) -> None:
        """Test the EHB profile with 20 mm corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match="The profile has fully corroded."):
            ISteelProfile.from_standard_profile(
                profile=HEB.HEB360,
                steel_material=SteelMaterial(SteelStrengthClass.S355),
                corrosion=20,  # mm
            )

    def test_corrosion_in_name(self) -> None:
        """Test that the name includes corrosion information."""
        i_profile_with_corrosion = ISteelProfile.from_standard_profile(
            profile=HEB.HEB360,
            steel_material=SteelMaterial(SteelStrengthClass.S355),
            corrosion=2,  # mm
        )
        expected_name_with_corrosion = "HEB360 (corrosion: 2 mm)"
        assert i_profile_with_corrosion.name == expected_name_with_corrosion
