"""Test suite for the CHSSteelProfile class."""

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.materials.steel import SteelStrengthClass
from blueprints.structural_sections.steel.steel_cross_sections.chs_profile import CHSProfiles, CHSSteelProfile
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHSStandardProfileClass


class TestCHSSteelProfile:
    """Test suite for CHSSteelProfile."""

    @pytest.fixture
    def chs_profile(self) -> CHSSteelProfile:
        """Fixture to set up a CHS profile for testing."""
        profile: CHSStandardProfileClass = CHSStandardProfileClass.CHS_508x16
        steel_class: SteelStrengthClass = SteelStrengthClass.EN_10025_2_S355
        return CHSProfiles(profile=profile, steel_class=steel_class).get_profile()

    def test_str(self) -> None:
        """Test the string representation of the CHS profile."""
        profile: CHSStandardProfileClass = CHSStandardProfileClass.CHS_508x16
        steel_class: SteelStrengthClass = SteelStrengthClass.EN_10025_2_S355
        expected_str: str = "Steel class: SteelStrengthClass.EN_10025_2_S355, Profile: CHSStandardProfileClass.CHS_508x16"
        assert CHSProfiles(profile=profile, steel_class=steel_class).__str__() == expected_str

    def test_code(self) -> None:
        """Test the code of the CHS profile."""
        profile: CHSStandardProfileClass = CHSStandardProfileClass.CHS_508x16
        steel_class: SteelStrengthClass = SteelStrengthClass.EN_10025_2_S355
        code: str = CHSProfiles(profile=profile, steel_class=steel_class).code()
        expected_code: str = "CHS 508x16"
        assert code == expected_code

    def test_steel_volume_per_meter(self, chs_profile: CHSSteelProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume: float = 2.47e-2  # m³/m
        assert pytest.approx(chs_profile.steel_volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_weight_per_meter(self, chs_profile: CHSSteelProfile) -> None:
        """Test the steel weight per meter."""
        expected_weight: float = 2.47e-2 * 7850  # kg/m
        assert pytest.approx(chs_profile.steel_weight_per_meter, rel=1e-2) == expected_weight

    def test_steel_area(self, chs_profile: CHSSteelProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area: float = 2.47e4  # mm²
        assert pytest.approx(chs_profile.steel_area, rel=1e-2) == expected_area

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

    def test_plastic_section_modulus_about_y(self, chs_profile: CHSSteelProfile) -> None:
        """Test the plastic section modulus about the y-axis."""
        expected_plastic_modulus_y: float = 3.874e6  # mm³
        assert pytest.approx(chs_profile.plastic_section_modulus_about_y, rel=1e-2) == expected_plastic_modulus_y

    def test_plastic_section_modulus_about_z(self, chs_profile: CHSSteelProfile) -> None:
        """Test the plastic section modulus about the z-axis."""
        expected_plastic_modulus_z: float = 3.874e6  # mm³
        assert pytest.approx(chs_profile.plastic_section_modulus_about_z, rel=1e-2) == expected_plastic_modulus_z

    def test_vertices(self, chs_profile: CHSSteelProfile) -> None:
        """Test the vertices of the cross-section."""
        assert len(chs_profile.vertices) > 0

    def test_plot(self, chs_profile: CHSSteelProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig: Figure = chs_profile.plot()
        assert isinstance(fig, plt.Figure)
