"""Test suite for the CHSSteelProfile class."""

import matplotlib as mpl

from blueprints.validations import NegativeValueError

mpl.use("Agg")

from unittest.mock import MagicMock

import matplotlib.pyplot as plt
import pytest

from blueprints.structural_sections.steel.profile_definitions.chs_profile import CHSProfile
from blueprints.structural_sections.steel.standard_profiles.chs import CHS


class TestCHSSteelProfile:
    """Test suite for CHSSteelProfile."""

    def test_name(self, chs_profile: CHSProfile) -> None:
        """Test the name of the CHS profile."""
        expected_name: str = "CHS 508x16"
        assert chs_profile.name == expected_name

    def test_code(self, chs_profile: CHSProfile) -> None:
        """Test the code of the CHS profile."""
        expected_alias: str = "CHS 508x16"
        assert chs_profile.name == expected_alias

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

    def test_profile_with_corrosion_negative_values(self) -> None:
        """Test the CHS profile with negative corrosion values."""
        with pytest.raises(NegativeValueError):
            CHS.CHS508x16.with_corrosion(
                corrosion_outside=-1,  # mm
                corrosion_inside=1,  # mm
            )

    def test_profile_with_corrosion_zero_corrosion(self) -> None:
        """Test that the CHS profile with zero corrosion returns the original profile."""
        original_profile = CHS.CHS508x16
        corroded_profile = original_profile.with_corrosion(
            corrosion_outside=0,  # mm
            corrosion_inside=0,  # mm
        )
        assert corroded_profile == original_profile

    def test_profile_with_corrosion_fully_corroded(self) -> None:
        """Test that the CHS profile with corrosion raises an error when fully corroded."""
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            CHS.CHS508x16.with_corrosion(
                corrosion_outside=5,  # mm
                corrosion_inside=11,  # mm
            )

    def test_corrosion_in_name(self) -> None:
        """Test that the name includes corrosion information."""
        chs_profile_with_corrosion = CHS.CHS508x16.with_corrosion(
            corrosion_outside=1,  # mm
            corrosion_inside=2,  # mm
        )
        expected_name_with_corrosion = "CHS 508x16 (corrosion inside: 2 mm, corrosion outside: 1 mm)"
        assert chs_profile_with_corrosion.name == expected_name_with_corrosion

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
