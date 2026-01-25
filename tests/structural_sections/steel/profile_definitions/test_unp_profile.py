"""Test suite for UNPProfile."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.structural_sections.steel.profile_definitions.unp_profile import UNPProfile
from blueprints.validations import NegativeValueError


class TestUNPProfile:
    """Test suite for UNPProfile."""

    def test_alias(self, unp_profile: UNPProfile) -> None:
        """Test the alias of the UNP profile."""
        expected_alias = "UNP200"
        assert unp_profile.name == expected_alias

    def test_steel_volume_per_meter(self, unp_profile: UNPProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 0.322e-2  # m³/m
        assert pytest.approx(unp_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_area(self, unp_profile: UNPProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 3.22e3  # mm²
        assert pytest.approx(unp_profile.area, rel=1e-2) == expected_area

    def test_max_profile_thickness(self, unp_profile: UNPProfile) -> None:
        """Test the maximum profile thickness."""
        expected_max_thickness = 11.5  # mm
        assert pytest.approx(unp_profile.max_profile_thickness, rel=1e-6) == expected_max_thickness

    @pytest.mark.slow
    def test_plot_unp_profile(self, unp_profile: UNPProfile) -> None:
        """Test the plot method for a UNP profile (ensure it runs without errors)."""
        fig: Figure = unp_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, unp_profile: UNPProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the UNP-profile shapes with mocked section properties."""
        fig: Figure = unp_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, unp_profile: UNPProfile) -> None:
        """Test the geometry of the UNP profile."""
        expected_geometry = unp_profile._geometry()  # noqa: SLF001
        assert expected_geometry is not None

    def test_immutability(self, unp_profile: UNPProfile) -> None:
        """Test that the UNPProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            unp_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, unp_profile: UNPProfile) -> None:
        """Test the transform method of the UNP profile."""
        transformed_profile = unp_profile.transform(horizontal_offset=1000, vertical_offset=500, rotation=90)
        assert transformed_profile is not None
        assert isinstance(transformed_profile, UNPProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == unp_profile.centroid.x + 1000
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == unp_profile.centroid.y + 500
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == unp_profile.profile_width

    def test_with_corrosion_negative_value(self, unp_profile: UNPProfile) -> None:
        """Test that negative corrosion value raises NegativeValueError."""
        with pytest.raises(NegativeValueError, match=r"corrosion"):
            unp_profile.with_corrosion(corrosion=-1)

    def test_with_corrosion_zero_value(self, unp_profile: UNPProfile) -> None:
        """Test that zero corrosion returns the same profile instance."""
        corroded_profile = unp_profile.with_corrosion(corrosion=0)
        # Zero corrosion should return the same instance
        assert corroded_profile is unp_profile
        assert corroded_profile.name == unp_profile.name

    def test_with_corrosion_valid_positive_value(self, unp_profile: UNPProfile) -> None:
        """Test applying a valid positive corrosion value."""
        corrosion = 2.0  # mm
        corroded_profile = unp_profile.with_corrosion(corrosion=corrosion)

        # Check that a new instance is returned
        assert corroded_profile is not unp_profile

        # Check dimensions are reduced by 2 * corrosion (both sides)
        assert pytest.approx(corroded_profile.top_flange_total_width, rel=1e-6) == unp_profile.top_flange_total_width - corrosion * 2
        assert pytest.approx(corroded_profile.top_flange_thickness, rel=1e-6) == unp_profile.top_flange_thickness - corrosion * 2
        assert pytest.approx(corroded_profile.bottom_flange_total_width, rel=1e-6) == unp_profile.bottom_flange_total_width - corrosion * 2
        assert pytest.approx(corroded_profile.bottom_flange_thickness, rel=1e-6) == unp_profile.bottom_flange_thickness - corrosion * 2
        assert pytest.approx(corroded_profile.total_height, rel=1e-6) == unp_profile.total_height - corrosion * 2
        assert pytest.approx(corroded_profile.web_thickness, rel=1e-6) == unp_profile.web_thickness - corrosion * 2

        # Check radius values are changed by 1 * corrosion, but not less than zero
        assert corroded_profile.top_outer_corner_radius == max(0, unp_profile.top_outer_corner_radius - corrosion)
        assert corroded_profile.bottom_outer_corner_radius == max(0, unp_profile.bottom_outer_corner_radius - corrosion)
        assert corroded_profile.top_root_fillet_radius == unp_profile.top_root_fillet_radius + corrosion
        assert corroded_profile.bottom_root_fillet_radius == unp_profile.bottom_root_fillet_radius + corrosion
        assert corroded_profile.top_toe_radius == max(0, unp_profile.top_toe_radius - corrosion)
        assert corroded_profile.bottom_toe_radius == max(0, unp_profile.bottom_toe_radius - corrosion)

        # Check name is updated with corrosion info
        expected_name = "UNP200 (corrosion: 2.0 mm)"
        assert corroded_profile.name == expected_name

    def test_with_corrosion_fully_corroded_profile(self, unp_profile: UNPProfile) -> None:
        """Test that applying corrosion that fully corrodes the profile raises ValueError."""
        # UNP200 has web_thickness = 8.5 mm and flange_thickness = 22.5 mm
        # Apply a corrosion large enough to fully corrode the web
        corrosion = 10.0  # mm - this will cause web_thickness to be 8.5 - 20 = -11.5 mm
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            unp_profile.with_corrosion(corrosion=corrosion)

    def test_with_corrosion_existing_corrosion_total_in_name(self, unp_profile: UNPProfile) -> None:
        """Test that applying corrosion to a profile with existing corrosion shows total corrosion in name."""
        # First apply 1 mm corrosion
        first_corrosion = 1.0  # mm
        first_corroded_profile = unp_profile.with_corrosion(corrosion=first_corrosion)
        assert first_corroded_profile.name == "UNP200 (corrosion: 1.0 mm)"

        # Then apply another 1.5 mm corrosion
        second_corrosion = 1.5  # mm
        second_corroded_profile = first_corroded_profile.with_corrosion(corrosion=second_corrosion)

        # Check that the name shows total corrosion (1.0 + 1.5 = 2.5 mm)
        expected_name = "UNP200 (corrosion: 2.5 mm)"
        assert second_corroded_profile.name == expected_name

        # Check dimensions reflect total corrosion
        total_corrosion = first_corrosion + second_corrosion
        assert pytest.approx(second_corroded_profile.top_flange_total_width, rel=1e-6) == unp_profile.top_flange_total_width - total_corrosion * 2
        assert pytest.approx(second_corroded_profile.top_flange_thickness, rel=1e-6) == unp_profile.top_flange_thickness - total_corrosion * 2
        assert (
            pytest.approx(second_corroded_profile.bottom_flange_total_width, rel=1e-6) == unp_profile.bottom_flange_total_width - total_corrosion * 2
        )
        assert pytest.approx(second_corroded_profile.bottom_flange_thickness, rel=1e-6) == unp_profile.bottom_flange_thickness - total_corrosion * 2
        assert pytest.approx(second_corroded_profile.total_height, rel=1e-6) == unp_profile.total_height - total_corrosion * 2
        assert pytest.approx(second_corroded_profile.web_thickness, rel=1e-6) == unp_profile.web_thickness - total_corrosion * 2

    def test_negative_calculated_values(self, unp_profile: UNPProfile) -> None:
        """Test that applying excessive corrosion raises NegativeValueError for calculated properties."""
        with pytest.raises(NegativeValueError):
            unp_profile.with_corrosion(corrosion=4)
