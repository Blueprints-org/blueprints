"""Test suite for RHSProfiles class."""

import pytest
from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelStrengthClass
from blueprints.structural_sections.steel.steel_cross_sections.rhs_profile import RHSProfiles, RHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhscf import RHSCF


class TestRHSSteelProfile:
    """Test suite for RHSSteelProfile."""

    @pytest.fixture
    def rhs_cold_formed(self) -> RHSSteelProfile:
        """Fixture to set up a cold-formed RHS profile for testing."""
        profile = RHSCF.RHSCF120x80_5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        return RHSProfiles(profile=profile, steel_class=steel_class).get_profile()

    def test_total_width(self) -> None:
        """Test the total width of the RHS profile."""
        profile = RHSCF.RHSCF120x80_5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        rhs_profile = RHSProfiles(profile=profile, steel_class=steel_class)
        assert rhs_profile.total_width() == 80

    def test_total_height(self) -> None:
        """Test the total height of the RHS profile."""
        profile = RHSCF.RHSCF120x80_5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        rhs_profile = RHSProfiles(profile=profile, steel_class=steel_class)
        assert rhs_profile.total_height() == 120

    def test_thickness(self) -> None:
        """Test the wall thickness of the RHS profile."""
        profile = RHSCF.RHSCF120x80_5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        rhs_profile = RHSProfiles(profile=profile, steel_class=steel_class)
        assert rhs_profile.thickness() == 5

    def test_center_radius(self) -> None:
        """Test the corner radius of the RHS profile."""
        profile = RHSCF.RHSCF120x80_5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        rhs_profile = RHSProfiles(profile=profile, steel_class=steel_class)
        expected_radius = 1.5 * 5  # Default center radius is 1.5 * thickness
        assert rhs_profile.center_radius() == expected_radius

    def test_get_profile(self) -> None:
        """Test the get_profile method of RHSProfiles."""
        profile = RHSCF.RHSCF120x80_5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        rhs_profiles = RHSProfiles(profile=profile, steel_class=steel_class)
        rhs_profile = rhs_profiles.get_profile()
        assert isinstance(rhs_profile, RHSSteelProfile)

    def test_str_cold_formed(self) -> None:
        """Test the string representation of the RHS profile."""
        profile = RHSCF.RHSCF120x80_5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        expected_str = "Steel class: SteelStrengthClass.EN_10025_2_S355, Width: 80 mm, Height: 120 mm, Thickness: 5 mm"
        assert RHSProfiles(profile=profile, steel_class=steel_class).__str__() == expected_str

    def test_total_width_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the total width of the RHS profile."""
        width = rhs_cold_formed.total_width
        expected_width = 80
        assert width == expected_width

    def test_total_height_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the total height of the RHS profile."""
        height = rhs_cold_formed.total_height
        expected_height = 120
        assert height == expected_height

    def test_steel_weight_per_meter_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight = 18.40e-4 * 7850  # kg/m
        assert pytest.approx(rhs_cold_formed.steel_weight_per_meter, rel=1e-2) == expected_weight

    def test_steel_area_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 18.40e2  # mm²
        assert pytest.approx(rhs_cold_formed.steel_area, rel=1e-2) == expected_area

    def test_centroid_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the centroid of the steel cross-section."""
        expected_centroid = (0, 0)  # (x, y) coordinates
        assert pytest.approx(rhs_cold_formed.centroid.x, rel=1e-2) == expected_centroid[0]
        assert pytest.approx(rhs_cold_formed.centroid.y, rel=1e-2) == expected_centroid[1]

    def test_moment_of_inertia_about_y_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the moment of inertia about the y-axis."""
        expected_moi_y = 353e4  # mm⁴
        assert pytest.approx(rhs_cold_formed.moment_of_inertia_about_y, rel=1e-2) == expected_moi_y

    def test_moment_of_inertia_about_z_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the moment of inertia about the z-axis."""
        expected_moi_z = 188e4  # mm⁴
        assert pytest.approx(rhs_cold_formed.moment_of_inertia_about_z, rel=1e-2) == expected_moi_z

    def test_elastic_section_modulus_about_y_positive_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the positive z side."""
        expected_modulus_y_positive = 58.9e3  # mm³
        assert pytest.approx(rhs_cold_formed.elastic_section_modulus_about_y_positive, rel=1e-2) == expected_modulus_y_positive

    def test_elastic_section_modulus_about_y_negative_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the elastic section modulus about the y-axis on the negative z side."""
        expected_modulus_y_negative = 58.9e3  # mm³
        assert pytest.approx(rhs_cold_formed.elastic_section_modulus_about_y_negative, rel=1e-2) == expected_modulus_y_negative

    def test_elastic_section_modulus_about_z_positive_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the positive y side."""
        expected_modulus_z_positive = 46.9e3  # mm³
        assert pytest.approx(rhs_cold_formed.elastic_section_modulus_about_z_positive, rel=1e-2) == expected_modulus_z_positive

    def test_elastic_section_modulus_about_z_negative_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the elastic section modulus about the z-axis on the negative y side."""
        expected_modulus_z_negative = 46.9e3  # mm³
        assert pytest.approx(rhs_cold_formed.elastic_section_modulus_about_z_negative, rel=1e-2) == expected_modulus_z_negative

    def test_plastic_section_modulus_about_y_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the plastic section modulus about the y-axis."""
        expected_plastic_modulus_y = 72.4e3  # mm³
        assert pytest.approx(rhs_cold_formed.plastic_section_modulus_about_y, rel=1e-2) == expected_plastic_modulus_y

    def test_plastic_section_modulus_about_z_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the plastic section modulus about the z-axis."""
        expected_plastic_modulus_z = 54.7e3  # mm³
        assert pytest.approx(rhs_cold_formed.plastic_section_modulus_about_z, rel=1e-2) == expected_plastic_modulus_z

    def test_vertices_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the vertices of the cross-section."""
        assert len(rhs_cold_formed.vertices) > 0

    def test_plot_cold_formed(self, rhs_cold_formed: RHSSteelProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig = rhs_cold_formed.plot()
        assert isinstance(fig, plt.Figure)
