"""Tests for right-angled triangular cross-section shapes with a quarter circle."""

import pytest

from blueprints.structural_sections.cross_section_quarter_circular_spandrel import QuarterCircularSpandrelCrossSection
from blueprints.validations import NegativeValueError


class TestQuarterCircularSpandrelCrossSection:
    """Tests for the QuarterCircularSpandrelCrossSection class."""

    def test_polygon(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the polygon property."""
        polygon = qcs_cross_section.polygon
        assert polygon.is_valid
        assert len(polygon.exterior.coords) > 0

    def test_geometry(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the geometry property."""
        geometry = qcs_cross_section.geometry()
        assert geometry is not None

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"thickness_vertical": -1, "thickness_horizontal": 10, "inner_radius": 5, "outer_radius": 10},
            {"thickness_vertical": 10, "thickness_horizontal": -1, "inner_radius": 5, "outer_radius": 10},
            {"thickness_vertical": 10, "thickness_horizontal": 10, "inner_radius": -1, "outer_radius": 10},
            {"thickness_vertical": 10, "thickness_horizontal": 10, "inner_radius": 5, "outer_radius": -1},
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, kwargs: dict) -> None:
        """Test NegativeValueError is raised for negative values."""
        with pytest.raises(NegativeValueError):
            QuarterCircularSpandrelCrossSection(**kwargs)

    def test_invalid_outer_radius_greater_than_inner_plus_thickness(self) -> None:
        """Test initialization with an outer radius greater than inner radius plus thickness."""
        with pytest.raises(
            ValueError,
            match="Outer radius 20 must be smaller than or equal to inner radius 5 plus the thickness 10",
        ):
            QuarterCircularSpandrelCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=20,
            )

    def test_invalid_corner_direction(self) -> None:
        """Test initialization with an invalid corner direction."""
        with pytest.raises(ValueError, match="corner_direction must be one of 0, 1, 2, or 3, got 4"):
            QuarterCircularSpandrelCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
                corner_direction=4,
            )
