"""Test suite for SheetpileZProfile."""

import matplotlib as mpl

mpl.use("Agg")

from unittest.mock import MagicMock

import pytest
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from blueprints.structural_sections.steel.profile_definitions.sheetpile_z_profile import SheetpileZProfile


class TestSheetpileZProfile:
    """Test suite for SheetpileZProfile."""

    def test_name(self, az_profile: SheetpileZProfile) -> None:
        """Test the name of the Z sheet pile profile."""
        expected_name = "AZ 18"
        assert az_profile.name == expected_name

    def test_maximum_element_thickness(self, az_profile: SheetpileZProfile) -> None:
        """Test the maximum element thickness of the Z sheet pile profile."""
        expected_max_thickness = 9.5  # mm
        assert pytest.approx(az_profile.max_thickness, rel=1e-6) == expected_max_thickness

    def test_steel_volume_per_meter(self, az_profile: SheetpileZProfile) -> None:
        """Test the steel volume per meter."""
        expected_volume = 9.48e-3  # m³/m
        assert pytest.approx(az_profile.volume_per_meter, rel=1e-2) == expected_volume

    def test_steel_area(self, az_profile: SheetpileZProfile) -> None:
        """Test the steel cross-sectional area."""
        expected_area = 9480  # mm²
        assert pytest.approx(az_profile.area, rel=1e-2) == expected_area

    @pytest.mark.slow
    def test_plot(self, az_profile: SheetpileZProfile) -> None:
        """Test the plot method (ensure it runs without errors)."""
        fig: Figure = az_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_plot_mocked(self, az_profile: SheetpileZProfile, mock_section_properties: MagicMock) -> None:  # noqa: ARG002
        """Test the plotting of the Z sheet pile profile shapes with mocked section properties."""
        fig: Figure = az_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_geometry(self, az_profile: SheetpileZProfile) -> None:
        """Test the geometry of the Z sheet pile profile."""
        expected_geometry = az_profile._geometry()  # noqa: SLF001
        assert expected_geometry is not None

    def test_immutability(self, az_profile: SheetpileZProfile) -> None:
        """Test that the SheetpileZProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            az_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, az_profile: SheetpileZProfile) -> None:
        """Test the transform method of the Z sheet pile profile."""
        transformed_profile = az_profile.transform(horizontal_offset=1000, vertical_offset=500, rotation=90)
        assert transformed_profile is not None
        assert isinstance(transformed_profile, SheetpileZProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == az_profile.centroid.x + 1000
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == az_profile.centroid.y + 500

    def test_with_corrosion_negative_value(self, az_profile: SheetpileZProfile) -> None:
        """Test that negative corrosion value raises ValueError."""
        with pytest.raises(ValueError, match=r"Corrosion value must be non-negative"):
            az_profile.with_corrosion(corrosion=-1)

    def test_with_corrosion_zero_value(self, az_profile: SheetpileZProfile) -> None:
        """Test that zero corrosion returns a profile with unchanged dimensions."""
        corroded_profile = az_profile.with_corrosion(corrosion=0)
        # Zero corrosion should return a profile with the same dimensions
        assert corroded_profile.web_thickness == az_profile.web_thickness
        assert corroded_profile.flange_thickness == az_profile.flange_thickness

    def test_with_corrosion_valid_positive_value(self, az_profile: SheetpileZProfile) -> None:
        """Test applying a valid positive corrosion value."""
        corrosion = 1.0  # mm
        corroded_profile = az_profile.with_corrosion(corrosion=corrosion)

        # Check that a new instance is returned
        assert corroded_profile is not az_profile

        # Check thicknesses are reduced by 2 * corrosion (both sides)
        assert pytest.approx(corroded_profile.web_thickness, rel=1e-6) == az_profile.web_thickness - corrosion * 2
        assert pytest.approx(corroded_profile.flange_thickness, rel=1e-6) == az_profile.flange_thickness - corrosion * 2

        # Check name is updated with corrosion info
        expected_name = "AZ 18 (corrosion: 1.0 mm)"
        assert corroded_profile.name == expected_name
        # Approximate area reduction based on paint area. However, paint area ignores locks. Therefore 3% tolerance is used to account for the locks.
        corroded_area_estimate = corrosion * 2 * 860
        assert corroded_profile.area == pytest.approx(az_profile.area - corroded_area_estimate, rel=0.03)

    def test_with_corrosion_fully_corroded_profile(self, az_profile: SheetpileZProfile) -> None:
        """Test that applying corrosion that fully corrodes the profile raises ValueError."""
        # AZ18 has web_thickness = 9.5 mm and flange_thickness = 9.5 mm
        # Apply a corrosion large enough to fully corrode the profile
        corrosion = 5.0  # mm - this will cause thickness to be 9.5 - 10 = -0.5 mm
        with pytest.raises(ValueError, match=r"The profile has fully corroded."):
            az_profile.with_corrosion(corrosion=corrosion)

    def test_with_corrosion_existing_corrosion_total_in_name(self, az_profile: SheetpileZProfile) -> None:
        """Test that applying corrosion to a profile with existing corrosion shows total corrosion in name."""
        # First apply 0.5 mm corrosion
        first_corrosion = 0.5  # mm
        first_corroded_profile = az_profile.with_corrosion(corrosion=first_corrosion)
        assert first_corroded_profile.name == "AZ 18 (corrosion: 0.5 mm)"

        # Then apply another 0.5 mm corrosion
        second_corrosion = 0.5  # mm
        second_corroded_profile = first_corroded_profile.with_corrosion(corrosion=second_corrosion)

        # Check that the name shows total corrosion (0.5 + 0.5 = 1.0 mm)
        expected_name = "AZ 18 (corrosion: 1.0 mm)"
        assert second_corroded_profile.name == expected_name

        # Check thicknesses reflect total corrosion
        total_corrosion = first_corrosion + second_corrosion
        assert pytest.approx(second_corroded_profile.web_thickness, rel=1e-6) == az_profile.web_thickness - total_corrosion * 2
        assert pytest.approx(second_corroded_profile.flange_thickness, rel=1e-6) == az_profile.flange_thickness - total_corrosion * 2

    def test_multiple_sheets_single_sheet(self, az_profile: SheetpileZProfile) -> None:
        """Test that multiple_sheets with 1 sheet returns a profile with 1 sheet."""
        single_sheet_profile = az_profile.multiple_sheets(number_of_sheets=1)
        assert single_sheet_profile.number_of_sheets == 1
        # Area should be the same for a single sheet
        assert pytest.approx(single_sheet_profile.area, rel=1e-6) == az_profile.area

    def test_multiple_sheets_multiple_sheets(self, az_profile: SheetpileZProfile) -> None:
        """Test that multiple_sheets with multiple sheets returns correct profile."""
        number_of_sheets = 4
        multi_sheet_profile = az_profile.multiple_sheets(number_of_sheets=number_of_sheets)
        assert multi_sheet_profile.number_of_sheets == number_of_sheets
        # Area should be approximately number_of_sheets times the single sheet area
        # (with small connectors added)
        assert multi_sheet_profile.area > az_profile.area * number_of_sheets * 0.99

    def test_multiple_sheets_invalid_number(self, az_profile: SheetpileZProfile) -> None:
        """Test that multiple_sheets with invalid number raises ValueError."""
        with pytest.raises(ValueError, match=r"Number of sheets must be at least 1"):
            az_profile.multiple_sheets(number_of_sheets=0)

        with pytest.raises(ValueError, match=r"Number of sheets must be at least 1"):
            az_profile.multiple_sheets(number_of_sheets=-1)

    @pytest.mark.slow
    def test_plot_multiple_sheets(self, az_profile: SheetpileZProfile) -> None:
        """Test plotting a profile with multiple sheets."""
        multi_sheet_profile = az_profile.multiple_sheets(number_of_sheets=3)
        fig: Figure = multi_sheet_profile.plot()
        assert isinstance(fig, plt.Figure)

    def test_coordinates_property(self, az_profile: SheetpileZProfile) -> None:
        """Test that coordinates property returns correct type."""
        assert isinstance(az_profile.coordinates, list)
        assert all(isinstance(coord, tuple) and len(coord) == 2 for coord in az_profile.coordinates)

    def test_interlocking_ctc(self, az_profile: SheetpileZProfile) -> None:
        """Test the interlocking center-to-center distance."""
        # AZ18 has interlocking_ctc of 630 mm
        expected_interlocking_ctc = 630.0  # mm
        assert pytest.approx(az_profile.interlocking_ctc, rel=1e-6) == expected_interlocking_ctc
