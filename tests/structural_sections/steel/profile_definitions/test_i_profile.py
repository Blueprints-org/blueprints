"""Test suite for IProfile."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.validations import NegativeValueError


class TestIProfile:
    """Test suite for IProfile."""

    def test_alias(self, h_profile: IProfile) -> None:
        """Test the alias of the I-profile."""
        expected_alias = "HEB360"
        assert h_profile.name == expected_alias

    def test_maximum_element_thickness(self, h_profile: IProfile) -> None:
        """Test the maximum element thickness of the I-profile."""
        expected_max_thickness = 22.5  # mm
        assert pytest.approx(h_profile.max_profile_thickness, rel=1e-6) == expected_max_thickness

    def test_steel_volume_per_meter(self, h_profile: IProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 1.806e-2  # m³/m
        assert pytest.approx(h_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_area(self, h_profile: IProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 1.806e4  # mm²
        assert pytest.approx(h_profile.area, rel=1e-2) == expected_area

    @pytest.mark.slow
    def test_plot_ipe_profile(self, ipe_profile: IProfile) -> None:
        """Test the plot method for an IPE profile (ensure it runs without errors)."""
        fig: Figure = ipe_profile.plot()
        assert isinstance(fig, plt.Figure)

    @pytest.mark.slow
    def test_plot_h_profile(self, h_profile: IProfile) -> None:
        """Test the plot method for an H-shaped profile (ensure it runs without errors)."""
        fig: Figure = h_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, h_profile: IProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the I-profile shapes with mocked section properties."""
        fig: Figure = h_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, h_profile: IProfile) -> None:
        """Test the geometry of the I profile."""
        expected_geometry = h_profile._geometry()  # noqa: SLF001
        assert expected_geometry is not None

    def test_immutability(self, h_profile: IProfile) -> None:
        """Test that the IProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            h_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, h_profile: IProfile) -> None:
        """Test the transform method of the I profile."""
        transformed_profile = h_profile.transform(horizontal_offset=1000, vertical_offset=500, rotation=90)
        assert transformed_profile is not None
        assert isinstance(transformed_profile, IProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == h_profile.centroid.x + 1000
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == h_profile.centroid.y + 500
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == h_profile.profile_width

    def test_with_corrosion_negative_value(self, h_profile: IProfile) -> None:
        """Test that negative corrosion value raises NegativeValueError."""
        with pytest.raises(NegativeValueError, match=r"corrosion"):
            h_profile.with_corrosion(corrosion=-1)

    def test_with_corrosion_zero_value(self, h_profile: IProfile) -> None:
        """Test that zero corrosion returns the same profile instance."""
        corroded_profile = h_profile.with_corrosion(corrosion=0)
        # Zero corrosion should return the same instance
        assert corroded_profile is h_profile
        assert corroded_profile.name == h_profile.name

    def test_with_corrosion_valid_positive_value(self, h_profile: IProfile) -> None:
        """Test applying a valid positive corrosion value."""
        corrosion = 2.0  # mm
        corroded_profile = h_profile.with_corrosion(corrosion=corrosion)

        # Check that a new instance is returned
        assert corroded_profile is not h_profile

        # Check dimensions are reduced by 2 * corrosion (both sides)
        assert pytest.approx(corroded_profile.top_flange_width, rel=1e-6) == h_profile.top_flange_width - corrosion * 2
        assert pytest.approx(corroded_profile.top_flange_thickness, rel=1e-6) == h_profile.top_flange_thickness - corrosion * 2
        assert pytest.approx(corroded_profile.bottom_flange_width, rel=1e-6) == h_profile.bottom_flange_width - corrosion * 2
        assert pytest.approx(corroded_profile.bottom_flange_thickness, rel=1e-6) == h_profile.bottom_flange_thickness - corrosion * 2
        assert pytest.approx(corroded_profile.total_height, rel=1e-6) == h_profile.total_height - corrosion * 2
        assert pytest.approx(corroded_profile.web_thickness, rel=1e-6) == h_profile.web_thickness - corrosion * 2

        # Check radius values are increased by corrosion
        assert corroded_profile.top_radius == h_profile.top_radius + corrosion
        assert corroded_profile.bottom_radius == h_profile.bottom_radius + corrosion

        # Check name is updated with corrosion info
        expected_name = "HEB360 (corrosion: 2.0 mm)"
        assert corroded_profile.name == expected_name

    def test_with_corrosion_fully_corroded_profile(self, h_profile: IProfile) -> None:
        """Test that applying corrosion that fully corrodes the profile raises ValueError."""
        # HEB360 has web_thickness = 12.5 mm and flange_thickness = 22.5 mm
        # Apply a corrosion large enough to fully corrode the web
        corrosion = 10.0  # mm - this will cause web_thickness to be 12.5 - 20 = -7.5 mm
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            h_profile.with_corrosion(corrosion=corrosion)

    def test_with_corrosion_existing_corrosion_total_in_name(self, h_profile: IProfile) -> None:
        """Test that applying corrosion to a profile with existing corrosion shows total corrosion in name."""
        # First apply 1 mm corrosion
        first_corrosion = 1.0  # mm
        first_corroded_profile = h_profile.with_corrosion(corrosion=first_corrosion)
        assert first_corroded_profile.name == "HEB360 (corrosion: 1.0 mm)"

        # Then apply another 1.5 mm corrosion
        second_corrosion = 1.5  # mm
        second_corroded_profile = first_corroded_profile.with_corrosion(corrosion=second_corrosion)

        # Check that the name shows total corrosion (1.0 + 1.5 = 2.5 mm)
        expected_name = "HEB360 (corrosion: 2.5 mm)"
        assert second_corroded_profile.name == expected_name

        # Check dimensions reflect total corrosion
        total_corrosion = first_corrosion + second_corrosion
        assert pytest.approx(second_corroded_profile.top_flange_width, rel=1e-6) == h_profile.top_flange_width - total_corrosion * 2
        assert pytest.approx(second_corroded_profile.top_flange_thickness, rel=1e-6) == h_profile.top_flange_thickness - total_corrosion * 2
        assert pytest.approx(second_corroded_profile.bottom_flange_width, rel=1e-6) == h_profile.bottom_flange_width - total_corrosion * 2
        assert pytest.approx(second_corroded_profile.bottom_flange_thickness, rel=1e-6) == h_profile.bottom_flange_thickness - total_corrosion * 2
        assert pytest.approx(second_corroded_profile.total_height, rel=1e-6) == h_profile.total_height - total_corrosion * 2
        assert pytest.approx(second_corroded_profile.web_thickness, rel=1e-6) == h_profile.web_thickness - total_corrosion * 2
