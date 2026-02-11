"""Test suite for StripSteelProfile."""

from unittest.mock import MagicMock

import matplotlib.pyplot as plt
import pytest

from blueprints.structural_sections.steel.profile_definitions.strip_profile import StripProfile
from blueprints.validations import NegativeValueError


class TestStripSteelProfile:
    """Test suite for StripSteelProfile."""

    def test_code(self, strip_profile: StripProfile) -> None:
        """Test the code of the Strip profile."""
        expected_alias = "160x5"
        assert strip_profile.name == expected_alias

    def test_maximum_element_thickness(self, strip_profile: StripProfile) -> None:
        """Test the maximum element thickness of the Strip profile."""
        expected_max_thickness = 5.0  # mm
        assert pytest.approx(strip_profile.max_thickness, rel=1e-6) == expected_max_thickness

    def test_steel_volume_per_meter(self, strip_profile: StripProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 0.160 * 0.005  # m³/m
        assert pytest.approx(strip_profile.volume_per_meter, rel=1e-6) == expected_volume

    def test_area(self, strip_profile: StripProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 160 * 5  # mm²
        assert pytest.approx(strip_profile.area, rel=1e-6) == expected_area

    @pytest.mark.slow
    def test_plot(self, strip_profile: StripProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig = strip_profile.plot(show=False, include_moment_of_inertia=True)
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, strip_profile: StripProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the Strip profile shapes with mocked section properties."""
        fig = strip_profile.plot(show=False)
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, strip_profile: StripProfile) -> None:
        """Test the geometry of the Strip profile."""
        expected_geometry = strip_profile._geometry()  # noqa: SLF001
        assert expected_geometry is not None

    def test_immutability(self, strip_profile: StripProfile) -> None:
        """Test that the StripProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            strip_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, strip_profile: StripProfile) -> None:
        """Test the transform method of the Strip profile."""
        transformed_profile = strip_profile.transform(horizontal_offset=1000, vertical_offset=500, rotation=90)
        assert transformed_profile is not None
        assert isinstance(transformed_profile, StripProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == strip_profile.centroid.x + 1000
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == strip_profile.centroid.y + 500
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == strip_profile.profile_width

    def test_with_corrosion_negative_value_raises_error(self, strip_profile: StripProfile) -> None:
        """Test that negative corrosion value raises NegativeValueError."""
        with pytest.raises(NegativeValueError, match=r"corrosion"):
            strip_profile.with_corrosion(corrosion=-1.0)

    def test_with_corrosion_zero_value(self, strip_profile: StripProfile) -> None:
        """Test that zero corrosion value returns the same profile."""
        result = strip_profile.with_corrosion(corrosion=0)
        assert result is strip_profile

    def test_with_corrosion_valid_positive_value(self, strip_profile: StripProfile) -> None:
        """Test with valid positive corrosion value."""
        # STRIP160x5: width=160, height=5
        corroded_profile = strip_profile.with_corrosion(corrosion=1.0)

        assert isinstance(corroded_profile, StripProfile)
        # Dimensions reduced by 2*corrosion
        assert pytest.approx(corroded_profile.width, rel=1e-6) == strip_profile.width - 2 * 1.0
        assert pytest.approx(corroded_profile.height, rel=1e-6) == strip_profile.height - 2 * 1.0
        # Name should include corrosion
        assert corroded_profile.name == "160x5 (corrosion: 1.0 mm)"

    def test_with_corrosion_fully_corroded(self, strip_profile: StripProfile) -> None:
        """Test that fully corroded profile raises ValueError."""
        # STRIP160x5: height=5, so corrosion=2.5 will fully corrode
        with pytest.raises(ValueError, match=r"The profile has fully corroded"):
            strip_profile.with_corrosion(corrosion=2.5)

    def test_with_corrosion_name_shows_total_corrosion(self, strip_profile: StripProfile) -> None:
        """Test that applying corrosion twice shows the total corrosion in the name."""
        # First apply corrosion
        corroded_once = strip_profile.with_corrosion(corrosion=0.5)
        assert corroded_once.name == "160x5 (corrosion: 0.5 mm)"

        # Apply additional corrosion
        corroded_twice = corroded_once.with_corrosion(corrosion=0.3)
        # Total should be 0.8 mm
        assert corroded_twice.name == "160x5 (corrosion: 0.8 mm)"
