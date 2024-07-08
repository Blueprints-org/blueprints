"""Tests for geometry operations."""

import math

import pytest
from shapely import Point

from blueprints.geometry.operations import CoordinateSystemOptions, calculate_rotation_angle


class TestCalculateRotationAngle:
    """Tests for the calculate_rotation_angle function."""

    def test_type_errors_are_raised(self) -> None:
        """Test if TypeError is raised when parameters are not of the expected type."""
        with pytest.raises(TypeError):
            calculate_rotation_angle(0, Point(1, 1))
        with pytest.raises(TypeError):
            calculate_rotation_angle(Point(0, 0), 1)
        with pytest.raises(TypeError):
            calculate_rotation_angle(Point(0, 0), Point(1, 1), coordinate_system="Invalid")

    def test_identical_points(self) -> None:
        """Test if ValueError is raised when start and end points are the same."""
        with pytest.raises(ValueError):
            calculate_rotation_angle(Point(0, 0), Point(0, 0))

    def test_missing_z_value(self) -> None:
        """Test if ValueError is raised when start or end point do not have z value when rotation
        angle in XZ or YZ plane is requested.
        """
        with pytest.raises(ValueError, match="start_point"):
            calculate_rotation_angle(Point(0, 0), Point(1, 1, 1), CoordinateSystemOptions.XZ)
        with pytest.raises(ValueError, match="start_point"):
            calculate_rotation_angle(Point(0, 0), Point(1, 1, 1), CoordinateSystemOptions.YZ)
        with pytest.raises(ValueError, match="end_point"):
            calculate_rotation_angle(Point(0, 0, 1), Point(1, 1), CoordinateSystemOptions.XZ)
        with pytest.raises(ValueError, match="end_point"):
            calculate_rotation_angle(Point(0, 0, 1), Point(1, 1), CoordinateSystemOptions.YZ)

    def test_quadrant_1(self) -> None:
        """Test correct result if the vector between the start and end point falls in the first quadrant."""
        pytest.approx(calculate_rotation_angle(Point(0, 0), Point(1, 1)), math.atan(1))

    def test_quadrant_2(self) -> None:
        """Test correct result if the vector between the start and end point falls in the second quadrant."""
        pytest.approx(calculate_rotation_angle(Point(1, 0), Point(0, 1)), math.pi - math.atan(1))

    def test_quadrant_3(self) -> None:
        """Test correct result if the vector between the start and end point falls in the third quadrant."""
        pytest.approx(calculate_rotation_angle(Point(1, 1), Point(0, 0)), (1.5 * math.pi) - math.atan(1))

    def test_quadrant_4(self) -> None:
        """Test correct result if the vector between the start and end point falls in the fourth quadrant."""
        pytest.approx(calculate_rotation_angle(Point(0, 1), Point(1, 0)), (2 * math.pi) - math.atan(1))

    def test_vertical_up(self) -> None:
        """Test correct result if the end point is above the start point."""
        pytest.approx(calculate_rotation_angle(Point(0, 0), Point(0, 1)), math.pi / 2)

    def test_vertical_down(self) -> None:
        """Test correct result if the end point is below the start point."""
        pytest.approx(calculate_rotation_angle(Point(0, 1), Point(0, 0)), math.pi * 1.5)

    def test_horizontal_left(self) -> None:
        """Test correct result if the end point is to the left of the start point."""
        pytest.approx(calculate_rotation_angle(Point(1, 0), Point(0, 0)), math.pi)

    def test_horizontal_right(self) -> None:
        """Test correct result if the end point is to the right of the start point."""
        pytest.approx(calculate_rotation_angle(Point(0, 0), Point(1, 0)), 0.0)

    def test_xz_plane(self) -> None:
        """Test correct result in the XZ plane."""
        pytest.approx(calculate_rotation_angle(Point(0, 0, 0), Point(1, 0, 1), CoordinateSystemOptions.XZ), math.atan(1))

    def test_yz_plane(self) -> None:
        """Test correct result in the YZ plane."""
        pytest.approx(calculate_rotation_angle(Point(0, 0, 0), Point(0, 1, 1), CoordinateSystemOptions.YZ), math.atan(1))
