"""Geometry operations module."""
# ruff: noqa: C901, PLR0911, PLR0912

import math
from enum import Enum

from shapely import Point

from blueprints.type_alias import RAD


class CoordinateSystemOptions(Enum):
    """Enum of the coordinate system options."""

    XY = 0
    XZ = 1
    YZ = 2


def calculate_rotation_angle(
    start_point: Point,
    end_point: Point,
    coordinate_system: CoordinateSystemOptions = CoordinateSystemOptions.XY,
) -> RAD:
    """
    Calculates rotation of an end point in relation to the start point in a given plane/coordinate system [rad].
    Start point lies in the origin center of the quadrant.

    Parameters
    ----------
    start_point: Point
        Starting point that will be used as reference.
    end_point: Point
        End point
    coordinate_system: CoordinateSystemOptions
        Desired plane that will be used as reference to calculate the rotation. Standard is XY-plane.

    Returns
    -------
    float
        rotation of end point relative to begin node in radians in the given plane [rad].

    Raises
    ------
    TypeError
        If parameters are not of the expected type.
    ValueError
        If start_point and end_point are the same.
        If start_point or end_point do not have z value when rotation angle in XZ or YZ plane
        is requested.
    """
    # Check types of parameters
    if not isinstance(start_point, Point):
        raise TypeError(f"Expected 'shapely.Point' type for 'start_point', but got '{type(start_point)}'.")

    if not isinstance(end_point, Point):
        raise TypeError(f"Expected 'shapely.Point' type for 'end_point', but got '{type(end_point)}'.")

    if not isinstance(coordinate_system, CoordinateSystemOptions):
        raise TypeError(f"Expected 'CoordinateSystemOptions' type for 'coordinate_system', but got '{type(coordinate_system)}'.")

    # Check that start point and end point are not equal
    if start_point == end_point:
        raise ValueError(f"Start and end point can't be equal. start={start_point} | end={end_point}")

    # Check that start point and end point have z value if coordinate_system is XZ or YZ.
    if coordinate_system != CoordinateSystemOptions.XY:
        if not start_point.has_z:
            raise ValueError(f"Coordinate system {coordinate_system} requires z value in 'start_point'.")
        if not end_point.has_z:
            raise ValueError(f"Coordinate system {coordinate_system} requires z value in 'end_point'.")

    match coordinate_system:
        case CoordinateSystemOptions.XY:
            horizontal_1, vertical_1 = start_point.x, start_point.y
            horizontal_2, vertical_2 = end_point.x, end_point.y
            dx = abs(horizontal_1 - horizontal_2)
            dy = abs(vertical_1 - vertical_2)
        case CoordinateSystemOptions.XZ:
            horizontal_1, vertical_1 = start_point.x, start_point.z
            horizontal_2, vertical_2 = end_point.x, end_point.z
            dx = abs(horizontal_1 - horizontal_2)
            dy = abs(vertical_1 - vertical_2)
        case CoordinateSystemOptions.YZ:
            horizontal_1, vertical_1 = start_point.y, start_point.z
            horizontal_2, vertical_2 = end_point.y, end_point.z
            dx = abs(horizontal_1 - horizontal_2)
            dy = abs(vertical_1 - vertical_2)

    # calculate rotation
    if horizontal_1 < horizontal_2 and vertical_1 < vertical_2:
        return math.atan(dy / dx)
    if horizontal_1 == horizontal_2 and vertical_1 < vertical_2:
        return math.pi / 2
    if horizontal_1 > horizontal_2 and vertical_1 < vertical_2:
        return math.pi - math.atan(dy / dx)
    if horizontal_1 > horizontal_2 and vertical_1 == vertical_2:
        return math.pi
    if horizontal_1 > horizontal_2 and vertical_1 > vertical_2:
        return (1.5 * math.pi) - math.atan(dx / dy)
    if horizontal_1 == horizontal_2 and vertical_1 > vertical_2:
        return math.pi * 1.5
    if horizontal_1 < horizontal_2 and vertical_1 > vertical_2:
        return (2 * math.pi) - math.atan(dy / dx)
    return 0.0
