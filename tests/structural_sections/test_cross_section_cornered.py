"""Tests for the circular cornered cross section."""

import pytest

from blueprints.structural_sections.cross_section_cornered import CircularCorneredCrossSection
from blueprints.validations import NegativeValueError


class TestCircularCorneredCrossSection:
    """Tests for the CircularCorneredCrossSection class."""

    def test_polygon(self, qcs_cross_section: CircularCorneredCrossSection) -> None:
        """Test the polygon property."""
        polygon = qcs_cross_section.polygon
        assert polygon.is_valid
        assert len(polygon.exterior.coords) > 0

    def test_geometry(self, qcs_cross_section: CircularCorneredCrossSection) -> None:
        """Test the geometry property."""
        geometry = qcs_cross_section.geometry()
        assert geometry is not None

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"thickness_vertical": -1},
            {"thickness_horizontal": -1},
            {"inner_radius": -1},
            {"outer_radius": -1},
            {"inner_slope_at_vertical": -1},
            {"inner_slope_at_horizontal": -1},
            {"outer_slope_at_vertical": -1},
            {"outer_slope_at_horizontal": -1},
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, kwargs: dict) -> None:
        """Test NegativeValueError is raised for negative values."""
        defaults = {
            "thickness_vertical": 10,
            "thickness_horizontal": 10,
            "inner_radius": 5,
            "outer_radius": 10,
        }
        with pytest.raises(NegativeValueError):
            CircularCorneredCrossSection(**{**defaults, **kwargs})

    def test_invalid_corner_direction(self) -> None:
        """Test initialization with an invalid corner direction."""
        with pytest.raises(ValueError, match="corner_direction must be one of 0, 1, 2, or 3, got 4"):
            CircularCorneredCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
                corner_direction=4,
            )

    def test_invalid_reference_point(self) -> None:
        """Test initialization with an invalid reference point."""
        with pytest.raises(ValueError, match="reference_point must be either 'intersection' or 'outer', got reference_point_that_does_not_exist"):
            CircularCorneredCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
                reference_point="reference_point_that_does_not_exist",
            )

    def test_invalid_slope_angle(self) -> None:
        """Test initialization with invalid slope angles."""
        with pytest.raises(ValueError, match="All slopes must be less than 100%"):
            CircularCorneredCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
                inner_slope_at_vertical=683,
            )

    def test_extensions(self) -> None:
        """Test that extensions are calculated correctly."""
        cross_section = CircularCorneredCrossSection(
            thickness_vertical=2,
            thickness_horizontal=2,
            inner_radius=0,
            outer_radius=10,
        )
        # Accessing the polygon property to trigger extension calculations
        _ = cross_section.polygon
        # If no exception is raised, the test passes

    def test_extreme_corrosion(self) -> None:
        """Test handling of extreme corrosion cases leading to non-90 degree angles."""
        corner_section = CircularCorneredCrossSection(
            thickness_vertical=15,
            thickness_horizontal=30,
            inner_radius=0,
            outer_radius=25,
            corner_direction=0,
            inner_slope_at_vertical=0,
            inner_slope_at_horizontal=0,
            outer_slope_at_vertical=8,
            outer_slope_at_horizontal=0,
        )

        # Accessing the polygon property to trigger extension calculations
        _ = corner_section.polygon

        corner_section = CircularCorneredCrossSection(
            thickness_vertical=30,
            thickness_horizontal=15,
            inner_radius=0,
            outer_radius=25,
            corner_direction=0,
            inner_slope_at_vertical=0,
            inner_slope_at_horizontal=0,
            outer_slope_at_vertical=0,
            outer_slope_at_horizontal=8,
        )

        # Accessing the polygon property to trigger extension calculations
        _ = corner_section.polygon
