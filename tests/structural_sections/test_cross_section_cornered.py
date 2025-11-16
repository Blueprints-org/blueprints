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
        with pytest.raises(ValueError, match="reference_point must be one of 'bottom_left', 'bottom_right', 'top_left', or 'top_right', got center"):
            CircularCorneredCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
                reference_point="reference_point_that_does_not_exist",
            )

    def test_invalid_slope_angle(self) -> None:
        """Test initialization with invalid slope angles."""
        with pytest.raises(
            ValueError, match="Sum of inner_slope_at_vertical and inner_slope_at_horizontal must be less than 90 degrees. Got 100.0 degrees."
        ):
            CircularCorneredCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
                inner_slope_at_vertical=683,
            )
