"""Tests for geometry operations."""

import math

import pytest
from shapely import Point

from blueprints.geometry.operations import CoordinateSystemOptions, calculate_rotation_angle
from blueprints.type_alias import RAD


class TestCalculateRotationAngle:
    """Tests for the calculate_rotation_angle function."""

    @pytest.mark.parametrize(
        ("start_point", "end_point"),
        [
            (Point(0, 0), Point(0, 0)),
            (Point(1, 1), Point(1, 1)),
        ],
    )
    def test_identical_points(self, start_point: Point, end_point: Point) -> None:
        """Test if ValueError is raised when start and end points are the same."""
        with pytest.raises(ValueError):
            calculate_rotation_angle(start_point=start_point, end_point=end_point)

    @pytest.mark.parametrize(
        ("start_point", "end_point", "coordinate_system"),
        [
            (Point(0, 0), Point(1, 1), CoordinateSystemOptions.XZ),
            (Point(0, 0), Point(1, 1), CoordinateSystemOptions.YZ),
        ],
    )
    def test_missing_z_value(self, start_point: Point, end_point: Point, coordinate_system: CoordinateSystemOptions) -> None:
        """Test if ValueError is raised when start or end point do not have z value when rotation
        angle in XZ or YZ plane is requested.
        """
        with pytest.raises(ValueError):
            calculate_rotation_angle(
                start_point=start_point,
                end_point=end_point,
                coordinate_system=coordinate_system,
            )

    @pytest.mark.parametrize(
        ("start_point", "end_point", "coordinate_system", "expected_result"),
        [
            (Point(0, 0), Point(1, 0), CoordinateSystemOptions.XY, 0),
            (Point(0, 0), Point(1, 1), CoordinateSystemOptions.XY, math.pi / 4),
            (Point(0, 0), Point(0, 1), CoordinateSystemOptions.XY, math.pi / 2),
            (Point(0, 0), Point(-1, 1), CoordinateSystemOptions.XY, (3 / 4) * math.pi),
            (Point(0, 0), Point(-1, 0), CoordinateSystemOptions.XY, math.pi),
            (Point(0, 0), Point(-1, -1), CoordinateSystemOptions.XY, (5 / 4) * math.pi),
            (Point(0, 0), Point(0, -1), CoordinateSystemOptions.XY, (3 / 2) * math.pi),
            (Point(0, 0), Point(1, -1), CoordinateSystemOptions.XY, (7 / 4) * math.pi),
            (Point(0, 0, 0), Point(1, 0, 0), CoordinateSystemOptions.XZ, 0),
            (Point(0, 0, 0), Point(1, 0, 1), CoordinateSystemOptions.XZ, math.pi / 4),
            (Point(0, 0, 0), Point(0, 0, 1), CoordinateSystemOptions.XZ, math.pi / 2),
            (Point(0, 0, 0), Point(-1, 0, 1), CoordinateSystemOptions.XZ, (3 / 4) * math.pi),
            (Point(0, 0, 0), Point(-1, 0, 0), CoordinateSystemOptions.XZ, math.pi),
            (Point(0, 0, 0), Point(-1, 0, -1), CoordinateSystemOptions.XZ, (5 / 4) * math.pi),
            (Point(0, 0, 0), Point(0, 0, -1), CoordinateSystemOptions.XZ, (3 / 2) * math.pi),
            (Point(0, 0, 0), Point(1, 0, -1), CoordinateSystemOptions.XZ, (7 / 4) * math.pi),
            (Point(0, 0, 0), Point(0, 1, 0), CoordinateSystemOptions.YZ, 0),
            (Point(0, 0, 0), Point(0, 1, 1), CoordinateSystemOptions.YZ, math.pi / 4),
            (Point(0, 0, 0), Point(0, 0, 1), CoordinateSystemOptions.YZ, math.pi / 2),
            (Point(0, 0, 0), Point(0, -1, 1), CoordinateSystemOptions.YZ, (3 / 4) * math.pi),
            (Point(0, 0, 0), Point(0, -1, 0), CoordinateSystemOptions.YZ, math.pi),
            (Point(0, 0, 0), Point(0, -1, -1), CoordinateSystemOptions.YZ, (5 / 4) * math.pi),
            (Point(0, 0, 0), Point(0, 0, -1), CoordinateSystemOptions.YZ, (3 / 2) * math.pi),
            (Point(0, 0, 0), Point(0, 1, -1), CoordinateSystemOptions.YZ, (7 / 4) * math.pi),
        ],
    )
    def test_keypoints_coordinate_system(
        self,
        start_point: Point,
        end_point: Point,
        coordinate_system: CoordinateSystemOptions,
        expected_result: RAD,
    ) -> None:
        """Test if the rotation angle is calculated correctly for the given keypoints and coordinate system."""
        result = calculate_rotation_angle(start_point=start_point, end_point=end_point, coordinate_system=coordinate_system)
        assert result == expected_result
