"""Test suite for the CHSSteelProfile class."""

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS


class TestCHSSteelProfile:
    """Test suite for CHSSteelProfile."""

    def test_name(self, chs_profile: CHSSteelProfile) -> None:
        """Test the name of the CHS profile."""
        expected_name: str = "CHS 508x16"
        assert chs_profile.name == expected_name

    def test_code(self, chs_profile: CHSSteelProfile) -> None:
        """Test the code of the CHS profile."""
        expected_alias: str = "CHS 508x16"
        assert chs_profile.name == expected_alias

    def test_steel_volume_per_meter(self, chs_profile: CHSSteelProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume: float = 2.47e-2  # m³/m
        assert pytest.approx(chs_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_weight_per_meter(self, chs_profile: CHSSteelProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight: float = 2.47e-2 * 7850  # kg/m
        assert pytest.approx(chs_profile.weight_per_meter, rel=1e-2) == expected_weight

    def test_area(self, chs_profile: CHSSteelProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area: float = 2.47e4  # mm²
        assert pytest.approx(chs_profile.area, rel=1e-2) == expected_area

    def test_centroid(self, chs_profile: CHSSteelProfile) -> None:
        """Test the centroid of the steel cross-section."""
        expected_centroid: tuple[float, float] = (0, 0)  # (x, y) coordinates
        assert pytest.approx(chs_profile.centroid.x, rel=1e-2) == expected_centroid[0]
        assert pytest.approx(chs_profile.centroid.y, rel=1e-2) == expected_centroid[1]

    def test_moment_of_inertia_about_y(self, chs_profile: CHSSteelProfile) -> None:
        """Test the moment of inertia about the y-axis."""
        expected_moi_y: float = 7.4909e8  # mm⁴
        assert pytest.approx(chs_profile.moment_of_inertia_about_y, rel=1e-2) == expected_moi_y

    def test_moment_of_inertia_about_z(self, chs_profile: CHSSteelProfile) -> None:
        """Test the moment of inertia about the z-axis."""
        expected_moi_z: float = 7.4909e8  # mm⁴
        assert pytest.approx(chs_profile.moment_of_inertia_about_z, rel=1e-2) == expected_moi_z

    def test_elastic_section_modulus_about_y_positive(self, chs_profile: CHSSteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the positive z side."""
        expected_modulus_y_positive: float = 2.9490e6  # mm³
        assert pytest.approx(chs_profile.elastic_section_modulus_about_y_positive, rel=1e-2) == expected_modulus_y_positive

    def test_elastic_section_modulus_about_y_negative(self, chs_profile: CHSSteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the negative z side."""
        expected_modulus_y_negative: float = 2.9490e6  # mm³
        assert pytest.approx(chs_profile.elastic_section_modulus_about_y_negative, rel=1e-2) == expected_modulus_y_negative

    def test_elastic_section_modulus_about_z_positive(self, chs_profile: CHSSteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the positive y side."""
        expected_modulus_z_positive: float = 2.9490e6  # mm³
        assert pytest.approx(chs_profile.elastic_section_modulus_about_z_positive, rel=1e-2) == expected_modulus_z_positive

    def test_elastic_section_modulus_about_z_negative(self, chs_profile: CHSSteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the negative y side."""
        expected_modulus_z_negative: float = 2.9490e6  # mm³
        assert pytest.approx(chs_profile.elastic_section_modulus_about_z_negative, rel=1e-2) == expected_modulus_z_negative

    def test_plot(self, chs_profile: CHSSteelProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig: Figure = chs_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, chs_profile: CHSSteelProfile) -> None:
        """Test the geometry of the CHS profile."""
        expected_geometry = chs_profile.geometry
        assert expected_geometry is not None

    def test_section_properties(self, chs_profile: CHSSteelProfile) -> None:
        """Test the section properties of the CHS profile."""
        section_properties = chs_profile.section_properties()
        assert section_properties.mass == pytest.approx(expected=chs_profile.area, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=chs_profile.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=chs_profile.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=chs_profile.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=chs_profile.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(expected=chs_profile.elastic_section_modulus_about_y_positive, rel=1e-2)
        assert section_properties.zyy_plus == pytest.approx(expected=chs_profile.elastic_section_modulus_about_z_positive, rel=1e-2)
        assert section_properties.zxx_minus == pytest.approx(expected=chs_profile.elastic_section_modulus_about_y_negative, rel=1e-2)
        assert section_properties.zyy_minus == pytest.approx(expected=chs_profile.elastic_section_modulus_about_z_negative, rel=1e-2)

    def test_get_profile_with_corrosion(self) -> None:
        """Test the CHS profile with 20 mm corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match="The profile has fully corroded."):
            CHSSteelProfile.from_standard_profile(
                profile=CHS.CHS508x16,
                steel_material=SteelMaterial(SteelStrengthClass.S355),
                corrosion_outside=5,  # mm
                corrosion_inside=11,  # mm
            )

    def test_corrosion_in_name(self) -> None:
        """Test that the name includes corrosion information."""
        chs_profile_with_corrosion = CHSSteelProfile.from_standard_profile(
            profile=CHS.CHS508x16,
            steel_material=SteelMaterial(SteelStrengthClass.S355),
            corrosion_outside=1,  # mm
            corrosion_inside=2,  # mm
        )
        expected_name_with_corrosion = "CHS 508x16 (corrosion  in: 2 mm, out: 1 mm)"
        assert chs_profile_with_corrosion.name == expected_name_with_corrosion
