"""Test suite for the CHSSteelProfile class."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import matplotlib.pyplot as plt
import pytest

from blueprints.structural_sections.steel.profile_definitions.chs_profile import CHSProfile
from blueprints.validations import NegativeValueError


class TestCHSSteelProfile:
    """Test suite for CHSSteelProfile."""

    def test_name(self, chs_profile: CHSProfile) -> None:
        """Test the name of the CHS profile."""
        expected_name: str = "CHS 508x16"
        assert chs_profile.name == expected_name

    def test_maximum_element_thickness(self, chs_profile: CHSProfile) -> None:
        """Test the maximum element thickness of the CHS profile."""
        expected_max_thickness: float = 16.0  # mm
        assert pytest.approx(chs_profile.max_thickness, rel=1e-6) == expected_max_thickness

    def test_steel_volume_per_meter(self, chs_profile: CHSProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume: float = 2.47e-2  # m³/m
        assert pytest.approx(chs_profile.volume_per_meter, rel=1e-2) == expected_volume

    @pytest.mark.slow
    def test_plot(self, chs_profile: CHSProfile) -> None:
        """Test the plotting of the CHS profile shapes."""
        fig = chs_profile.plot(show=False)
        assert fig is not None
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, chs_profile: CHSProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the CHS profile shapes with mocked section properties."""
        fig = chs_profile.plot(show=False)
        assert fig is not None
        assert isinstance(fig, plt.Figure)

    def test_immutability(self, chs_profile: CHSProfile) -> None:
        """Test that the CHSProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            chs_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, chs_profile: CHSProfile) -> None:
        """Test the transform method of the CHS profile."""
        transformed_profile = chs_profile.transform(horizontal_offset=1000, vertical_offset=500, rotation=0)
        assert transformed_profile is not None
        assert isinstance(transformed_profile, CHSProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == chs_profile.centroid.x + 1000
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == chs_profile.centroid.y + 500

    def test_negative_inner_diameter(self) -> None:
        """Test that NegativeValueError is raised when inner_diameter becomes negative."""
        # When wall_thickness > outer_diameter / 2, inner_diameter will be negative
        with pytest.raises(NegativeValueError, match=r"inner_diameter"):
            CHSProfile(outer_diameter=100, wall_thickness=60)

    def test_with_corrosion_negative_value(self, chs_profile: CHSProfile) -> None:
        """Test that negative corrosion value raises NegativeValueError."""
        with pytest.raises(NegativeValueError, match=r"corrosion"):
            chs_profile.with_corrosion(corrosion_outside=-1)

    def test_with_corrosion_zero_value(self, chs_profile: CHSProfile) -> None:
        """Test that zero corrosion returns the same profile instance."""
        corroded_profile = chs_profile.with_corrosion(corrosion_outside=0, corrosion_inside=0)
        # Zero corrosion should return the same instance
        assert corroded_profile is chs_profile
        assert corroded_profile.name == chs_profile.name

    def test_with_corrosion_valid_positive_value(self, chs_profile: CHSProfile) -> None:
        """Test applying a valid positive corrosion value."""
        corrosion_outside = 2.0  # mm
        corrosion_inside = 1.5  # mm
        corroded_profile = chs_profile.with_corrosion(corrosion_outside=corrosion_outside, corrosion_inside=corrosion_inside)

        # Check that a new instance is returned
        assert corroded_profile is not chs_profile

        # Check dimensions are reduced correctly
        # Outer diameter is reduced by 2 * corrosion_outside (both sides)
        assert pytest.approx(corroded_profile.outer_diameter, rel=1e-6) == chs_profile.outer_diameter - corrosion_outside * 2
        # Wall thickness is reduced by corrosion_outside + corrosion_inside
        assert pytest.approx(corroded_profile.wall_thickness, rel=1e-6) == chs_profile.wall_thickness - corrosion_outside - corrosion_inside

        # Check name is updated with corrosion info
        expected_name = "CHS 508x16 (corrosion inside: 1.5 mm, outside: 2.0 mm)"
        assert corroded_profile.name == expected_name

    def test_with_corrosion_fully_corroded_profile(self, chs_profile: CHSProfile) -> None:
        """Test that applying corrosion that fully corrodes the profile raises ValueError."""
        # CHS 508x16 has wall_thickness = 16 mm
        # Apply a corrosion large enough to fully corrode the wall
        corrosion_outside = 10.0  # mm
        corrosion_inside = 10.0  # mm - this will cause wall_thickness to be 16 - 10 - 10 = -4 mm
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            chs_profile.with_corrosion(corrosion_outside=corrosion_outside, corrosion_inside=corrosion_inside)

    def test_with_corrosion_existing_corrosion_total_in_name(self, chs_profile: CHSProfile) -> None:
        """Test that applying corrosion to a profile with existing corrosion shows total corrosion in name."""
        # First apply 1 mm outside and 0.5 mm inside corrosion
        first_corrosion_outside = 1.0  # mm
        first_corrosion_inside = 0.5  # mm
        first_corroded_profile = chs_profile.with_corrosion(
            corrosion_outside=first_corrosion_outside,
            corrosion_inside=first_corrosion_inside,
        )
        assert first_corroded_profile.name == "CHS 508x16 (corrosion inside: 0.5 mm, outside: 1.0 mm)"

        # Then apply another 1.5 mm outside and 1.0 mm inside corrosion
        second_corrosion_outside = 1.5  # mm
        second_corrosion_inside = 1.0  # mm
        second_corroded_profile = first_corroded_profile.with_corrosion(
            corrosion_outside=second_corrosion_outside,
            corrosion_inside=second_corrosion_inside,
        )

        # Check that the name shows total corrosion
        expected_name = "CHS 508x16 (corrosion inside: 1.5 mm, outside: 2.5 mm)"
        assert second_corroded_profile.name == expected_name

        # Check dimensions reflect total corrosion
        total_corrosion_outside = first_corrosion_outside + second_corrosion_outside
        total_corrosion_inside = first_corrosion_inside + second_corrosion_inside
        assert pytest.approx(second_corroded_profile.outer_diameter, rel=1e-6) == chs_profile.outer_diameter - total_corrosion_outside * 2
        assert (
            pytest.approx(second_corroded_profile.wall_thickness, rel=1e-6)
            == chs_profile.wall_thickness - total_corrosion_outside - total_corrosion_inside
        )
