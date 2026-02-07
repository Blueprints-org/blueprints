"""Test suite for the LNPProfile class."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.structural_sections.steel.profile_definitions.lnp_profile import LNPProfile
from blueprints.validations import NegativeValueError


class TestLNPProfile:
    """Test suite for LNPProfile."""

    def test_name(self, lnp_profile: LNPProfile) -> None:
        """Test the name of the LNP profile."""
        expected_name: str = "LNP 100x50x6"
        assert lnp_profile.name == expected_name

    def test_maximum_element_thickness(self, lnp_profile: LNPProfile) -> None:
        """Test the maximum element thickness of the LNP profile."""
        expected_max_thickness: float = 6.0  # mm
        assert pytest.approx(lnp_profile.max_profile_thickness, rel=1e-6) == expected_max_thickness

    def test_steel_volume_per_meter(self, lnp_profile: LNPProfile) -> None:
        """Test the steel volume per meter."""
        # Expected volume per meter calculated analytically for LNP 100x50x6: (area 871 mm² = 0.000871 m²) × 1 m = 0.000871 m³/m
        expected_volume: float = 0.000871  # m³/m
        assert pytest.approx(lnp_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_area(self, lnp_profile: LNPProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area: float = 871  # mm²
        assert pytest.approx(lnp_profile.area, rel=1e-2) == expected_area

    @pytest.mark.slow
    def test_plot(self, lnp_profile: LNPProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig: Figure = lnp_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, lnp_profile: LNPProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the LNP profile shapes with mocked section properties."""
        fig: Figure = lnp_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, lnp_profile: LNPProfile) -> None:
        """Test the geometry of the LNP profile."""
        expected_geometry = lnp_profile._geometry()  # noqa: SLF001
        assert expected_geometry is not None

    def test_custom_profile(self) -> None:
        """Test creating an LNPProfile with custom dimensions."""
        profile = LNPProfile(
            total_width=120,
            total_height=60,
            web_thickness=8,
            base_thickness=10,
            root_radius=5,
            back_radius=0,
            web_toe_radius=4,
            base_toe_radius=5,
            name="Custom LNP",
        )
        # Check that default radii are set correctly
        assert profile.area > 0

    def test_invalid_dimensions(self) -> None:
        """Test that invalid dimensions raise errors."""
        # Case with negative web toe straight part
        with pytest.raises(NegativeValueError, match=r"(?i) 'web_toe_straight_part' cannot be negative"):
            LNPProfile(
                total_width=100,
                total_height=50,
                web_thickness=6,
                base_thickness=6,
                root_radius=3,
                back_radius=6,
                web_toe_radius=7,
                base_toe_radius=0,
            )
        # Case with negative base toe straight part
        with pytest.raises(NegativeValueError, match=r"(?i) 'base_toe_straight_part' cannot be negative"):
            LNPProfile(
                total_width=100,
                total_height=0,
                web_thickness=6,
                base_thickness=6,
                root_radius=3,
                back_radius=3,
                web_toe_radius=0,
                base_toe_radius=7,
            )
        # Case with negative base inner width
        with pytest.raises(NegativeValueError, match=r"(?i) 'base_inner_width' cannot be negative"):
            LNPProfile(
                total_width=20,
                total_height=100,
                web_thickness=10,
                base_thickness=8,
                root_radius=6,
                back_radius=3,
                web_toe_radius=0,
                base_toe_radius=6,
            )
        # Case with negative web inner height
        with pytest.raises(NegativeValueError, match=r"(?i) 'web_inner_height' cannot be negative"):
            LNPProfile(
                total_width=100,
                total_height=30,
                web_thickness=12,
                base_thickness=15,
                root_radius=10,
                back_radius=0,
                web_toe_radius=10,
                base_toe_radius=6,
            )

    def test_immutability(self, lnp_profile: LNPProfile) -> None:
        """Test that the LNPProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            lnp_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, lnp_profile: LNPProfile) -> None:
        """Test the transform method of the LNP profile."""
        transformed_profile = lnp_profile.transform(horizontal_offset=1000, vertical_offset=500, rotation=90)
        assert transformed_profile is not None
        assert isinstance(transformed_profile, LNPProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == lnp_profile.centroid.x + 1000
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == lnp_profile.centroid.y + 500
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == lnp_profile.profile_width

    def test_with_corrosion_negative_value_raises_error(self, lnp_profile: LNPProfile) -> None:
        """Test that negative corrosion value raises NegativeValueError."""
        with pytest.raises(NegativeValueError, match=r"corrosion"):
            lnp_profile.with_corrosion(corrosion=-1.0)

    def test_with_corrosion_zero_value(self, lnp_profile: LNPProfile) -> None:
        """Test that zero corrosion value returns the same profile."""
        result = lnp_profile.with_corrosion(corrosion=0)
        assert result is lnp_profile

    def test_with_corrosion_valid_positive_value(self, lnp_profile: LNPProfile) -> None:
        """Test with valid positive corrosion value."""
        # LNP 100x50x6: total_width=100, total_height=50, web_thickness=6, base_thickness=6
        corroded_profile = lnp_profile.with_corrosion(corrosion=0.5)

        assert isinstance(corroded_profile, LNPProfile)
        # Outer dimensions reduced by 2*corrosion
        assert pytest.approx(corroded_profile.total_width, rel=1e-6) == lnp_profile.total_width - 2 * 0.5
        assert pytest.approx(corroded_profile.total_height, rel=1e-6) == lnp_profile.total_height - 2 * 0.5
        # Thicknesses reduced by 2*corrosion
        assert pytest.approx(corroded_profile.web_thickness, rel=1e-6) == lnp_profile.web_thickness - 2 * 0.5
        assert pytest.approx(corroded_profile.base_thickness, rel=1e-6) == lnp_profile.base_thickness - 2 * 0.5
        # Name should include corrosion
        assert corroded_profile.name == "LNP 100x50x6 (corrosion: 0.5 mm)"

    def test_with_corrosion_fully_corroded(self, lnp_profile: LNPProfile) -> None:
        """Test that fully corroded profile raises ValueError."""
        # LNP 100x50x6: web_thickness=6, base_thickness=6, so corrosion=3 will fully corrode
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            lnp_profile.with_corrosion(corrosion=3.0)

    def test_with_corrosion_name_shows_total_corrosion(self, lnp_profile: LNPProfile) -> None:
        """Test that applying corrosion twice shows the total corrosion in the name."""
        # First apply corrosion
        corroded_once = lnp_profile.with_corrosion(corrosion=0.3)
        assert corroded_once.name == "LNP 100x50x6 (corrosion: 0.3 mm)"

        # Apply additional corrosion
        corroded_twice = corroded_once.with_corrosion(corrosion=0.2)
        # Total should be 0.5 mm
        assert corroded_twice.name == "LNP 100x50x6 (corrosion: 0.5 mm)"
