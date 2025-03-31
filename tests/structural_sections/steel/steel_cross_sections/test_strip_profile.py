"""Test suite for StripSteelProfile."""

import matplotlib.pyplot as plt
import pytest

from blueprints.materials.steel import SteelStrengthClass
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import StripStandardProfileClass
from blueprints.structural_sections.steel.steel_cross_sections.strip_profile import StripProfiles, StripSteelProfile


class TestStripSteelProfile:
    """Test suite for StripSteelProfile."""

    @pytest.fixture
    def strip_profile(self) -> StripSteelProfile:
        """Fixture to set up a Strip profile for testing."""
        profile = StripStandardProfileClass.STRIP_160x5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        return StripProfiles(profile=profile, steel_class=steel_class).get_profile()

    def test_str(self) -> None:
        """Test the string representation of the Strip profile."""
        profile = StripStandardProfileClass.STRIP_160x5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        desc = StripProfiles(profile=profile, steel_class=steel_class).__str__()
        expected_str = "Steel class: SteelStrengthClass.EN_10025_2_S355, Profile: StripStandardProfileClass.STRIP_160x5"
        assert desc == expected_str

    def test_code(self) -> None:
        """Test the code of the Strip profile."""
        profile = StripStandardProfileClass.STRIP_160x5
        steel_class = SteelStrengthClass.EN_10025_2_S355
        code = StripProfiles(profile=profile, steel_class=steel_class).code()
        expected_code = "160x5"
        assert code == expected_code

    def test_steel_volume_per_meter(self, strip_profile: StripSteelProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 0.160 * 0.005  # m³/m
        assert pytest.approx(strip_profile.steel_volume_per_meter, rel=1e-6) == expected_volume

    def test_steel_weight_per_meter(self, strip_profile: StripSteelProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight = 0.160 * 0.005 * 7850  # kg/m
        assert pytest.approx(strip_profile.steel_weight_per_meter, rel=1e-6) == expected_weight

    def test_steel_area(self, strip_profile: StripSteelProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 160 * 5  # mm²
        assert pytest.approx(strip_profile.steel_area, rel=1e-6) == expected_area

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

    def test_plastic_section_modulus_about_y(self, strip_profile: StripSteelProfile) -> None:
        """Test the plastic section modulus about the y-axis."""
        expected_plastic_modulus_y = 1 / 4 * 160 * 5**2  # mm³
        assert pytest.approx(strip_profile.plastic_section_modulus_about_y, rel=1e-6) == expected_plastic_modulus_y

    def test_plastic_section_modulus_about_z(self, strip_profile: StripSteelProfile) -> None:
        """Test the plastic section modulus about the z-axis."""
        expected_plastic_modulus_z = 1 / 4 * 160**2 * 5  # mm³
        assert pytest.approx(strip_profile.plastic_section_modulus_about_z, rel=1e-6) == expected_plastic_modulus_z

    def test_vertices(self, strip_profile: StripSteelProfile) -> None:
        """Test the vertices of the cross-section."""
        assert len(strip_profile.vertices) > 0

    def test_plot(self, strip_profile: StripSteelProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig = strip_profile.plot(show=False)
        assert isinstance(fig, plt.Figure)
