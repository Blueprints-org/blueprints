"""Test suite for ISteelProfile."""

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.materials.steel import SteelStrengthClass
from blueprints.structural_sections.steel.steel_cross_sections.i_profile import IProfiles, ISteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB


class TestISteelProfile:
    """Test suite for ISteelProfile."""

    @pytest.fixture
    def i_profile(self) -> ISteelProfile:
        """Fixture to set up an I-profile for testing."""
        profile = HEB.HEB_360
        steel_class = SteelStrengthClass.EN_10025_2_S355
        return IProfiles(profile=profile, steel_class=steel_class).get_profile()

    def test_str(self) -> None:
        """Test the string representation of the I-profile."""
        profile = HEB.HEB_360
        steel_class = SteelStrengthClass.EN_10025_2_S355
        expected_str = "Steel class: SteelStrengthClass.EN_10025_2_S355, Profile: HEB.HEB_360"
        assert IProfiles(profile=profile, steel_class=steel_class).__str__() == expected_str

    def test_code(self) -> None:
        """Test the code of the I-profile."""
        profile = HEB.HEB_360
        code = profile.code
        expected_code = "HEB360"
        assert code == expected_code

    def test_steel_volume_per_meter(self, i_profile: ISteelProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 1.806e-2  # m³/m
        assert pytest.approx(i_profile.steel_volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_weight_per_meter(self, i_profile: ISteelProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight = 1.806e-2 * 7850  # kg/m
        assert pytest.approx(i_profile.steel_weight_per_meter, rel=1e-2) == expected_weight

    def test_steel_area(self, i_profile: ISteelProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 1.806e4  # mm²
        assert pytest.approx(i_profile.steel_area, rel=1e-2) == expected_area

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
