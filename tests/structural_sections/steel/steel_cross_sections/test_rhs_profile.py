"""Test suite for the RHSSteelProfile class."""

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.steel.steel_cross_sections.rhs_profile import RHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHS


class TestRHSSteelProfile:
    """Test suite for RHSSteelProfile."""

    def test_name(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the name of the RHS profile."""
        expected_name: str = "RHSCF 400x200x16"
        print(f"Profile name: {rhs_profile.name}")
        assert rhs_profile.name == expected_name

    def test_code(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the code of the RHS profile."""
        expected_alias: str = "RHSCF 400x200x16"
        assert rhs_profile.name == expected_alias

    def test_steel_volume_per_meter(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume: float = 0.017100  # m³/m
        assert pytest.approx(rhs_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_weight_per_meter(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight: float = 0.01700 * 7850  # kg/m
        assert pytest.approx(rhs_profile.weight_per_meter, rel=1e-2) == expected_weight

    def test_area(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area: float = 17100  # mm²
        assert pytest.approx(rhs_profile.area, rel=1e-2) == expected_area

    def test_centroid(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the centroid of the steel cross-section."""
        expected_centroid: tuple[float, float] = (0, 0)  # (x, y) coordinates
        assert pytest.approx(rhs_profile.centroid.x, rel=1e-2) == expected_centroid[0]
        assert pytest.approx(rhs_profile.centroid.y, rel=1e-2) == expected_centroid[1]

    def test_moment_of_inertia_about_y(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the moment of inertia about the y-axis."""
        expected_moi_y: float = 3.7789e8  # mm⁴
        assert pytest.approx(rhs_profile.moment_of_inertia_about_y, rel=1e-2) == expected_moi_y

    def test_moment_of_inertia_about_z(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the moment of inertia about the z-axis."""
        expected_moi_z: float = 1.1056e8  # mm⁴
        assert pytest.approx(rhs_profile.moment_of_inertia_about_z, rel=1e-2) == expected_moi_z

    def test_elastic_section_modulus_about_y_positive(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the positive z side."""
        expected_modulus_y_positive: float = 1.8895e6  # mm³
        assert pytest.approx(rhs_profile.elastic_section_modulus_about_y_positive, rel=1e-2) == expected_modulus_y_positive

    def test_elastic_section_modulus_about_y_negative(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the negative z side."""
        expected_modulus_y_negative: float = 1.8895e6  # mm³
        assert pytest.approx(rhs_profile.elastic_section_modulus_about_y_negative, rel=1e-2) == expected_modulus_y_negative

    def test_elastic_section_modulus_about_z_positive(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the positive y side."""
        expected_modulus_z_positive: float = 1.1060e6  # mm³
        assert pytest.approx(rhs_profile.elastic_section_modulus_about_z_positive, rel=1e-2) == expected_modulus_z_positive

    def test_elastic_section_modulus_about_z_negative(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the negative y side."""
        expected_modulus_z_negative: float = 1.1060e6  # mm³
        assert pytest.approx(rhs_profile.elastic_section_modulus_about_z_negative, rel=1e-2) == expected_modulus_z_negative

    def test_plot(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig: Figure = rhs_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the geometry of the RHS profile."""
        expected_geometry = rhs_profile.geometry
        assert expected_geometry is not None

    def test_section_properties(self, rhs_profile: RHSSteelProfile) -> None:
        """Test the section properties of the RHS profile."""
        section_properties = rhs_profile.section_properties()
        assert section_properties.mass == pytest.approx(expected=rhs_profile.area, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=rhs_profile.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=rhs_profile.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=rhs_profile.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=rhs_profile.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(expected=rhs_profile.elastic_section_modulus_about_y_positive, rel=1e-2)
        assert section_properties.zyy_plus == pytest.approx(expected=rhs_profile.elastic_section_modulus_about_z_positive, rel=1e-2)
        assert section_properties.zxx_minus == pytest.approx(expected=rhs_profile.elastic_section_modulus_about_y_negative, rel=1e-2)
        assert section_properties.zyy_minus == pytest.approx(expected=rhs_profile.elastic_section_modulus_about_z_negative, rel=1e-2)
        assert section_properties.sxx == pytest.approx(expected=rhs_profile.plastic_section_modulus_about_y, rel=1e-2)
        assert section_properties.syy == pytest.approx(expected=rhs_profile.plastic_section_modulus_about_z, rel=1e-2)

    def test_get_profile_with_corrosion(self) -> None:
        """Test the RHS profile with corrosion applied."""
        # Ensure the profile raises an error if fully corroded
        with pytest.raises(ValueError, match="The profile has fully corroded."):
            RHSSteelProfile.from_standard_profile(
                profile=RHS.RHS400x200_16,
                steel_material=SteelMaterial(SteelStrengthClass.S355),
                corrosion_outside=16,  # mm
                corrosion_inside=0,  # mm
            )

    def test_corrosion_in_name(self) -> None:
        """Test that the name includes corrosion information."""
        rhs_profile_with_corrosion = RHSSteelProfile.from_standard_profile(
                profile=RHS.RHS400x200_16,
                steel_material=SteelMaterial(SteelStrengthClass.S355),
                corrosion_outside=1,  # mm
                corrosion_inside=1,  # mm
        )
        expected_name_with_corrosion = "RHS 400x200_16 (corrosion in: 1 mm, out: 1 mm)"
        assert rhs_profile_with_corrosion.name == expected_name_with_corrosion
