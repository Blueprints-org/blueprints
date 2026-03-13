"""Geometry operations module."""

import math
from enum import Enum, auto

import numpy as np
from shapely import LinearRing, Point

from blueprints.type_alias import RAD


class CoordinateSystemOptions(Enum):
    """Enum of the coordinate system options."""

    XY = auto()
    XZ = auto()
    YZ = auto()


def calculate_rotation_angle(
    start_point: Point,
    end_point: Point,
    coordinate_system: CoordinateSystemOptions = CoordinateSystemOptions.XY,
) -> RAD:
    """
    Calculates rotation of an end point in relation to the start point in a given plane/coordinate system [rad].

    - Start point lies in the origin center of the quadrant.
    - The rotation is calculated in the given plane in relation to the start point.
    - The rotation is calculated in the range [0, 2*pi].
    - The rotation is calculated in the counter-clockwise direction.

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
    RAD
        rotation of end point relative to the start point in radians in the given plane [rad].

    Raises
    ------
    ValueError
        If start_point and end_point are the same.
        If start_point or end_point do not have z value when rotation angle in XZ or YZ plane is requested.
    """
    if list(start_point.coords) == list(end_point.coords):
        msg = f"Start and end point can't be equal. {start_point=} | {end_point=}"
        raise ValueError(msg)

    if coordinate_system != CoordinateSystemOptions.XY and (not start_point.has_z or not end_point.has_z):
        msg = f"Coordinate system '{coordinate_system}' requires z value in both points."
        raise ValueError(msg)

    # Map coordinate system to the corresponding attributes
    coordinates_map = {
        CoordinateSystemOptions.XY: ("x", "y"),
        CoordinateSystemOptions.XZ: ("x", "z"),
        CoordinateSystemOptions.YZ: ("y", "z"),
    }
    horizontal_attr, vertical_attr = coordinates_map[coordinate_system]

    # Extract the coordinates for the specified plane
    horizontal_1, vertical_1 = getattr(start_point, horizontal_attr), getattr(start_point, vertical_attr)
    horizontal_2, vertical_2 = getattr(end_point, horizontal_attr), getattr(end_point, vertical_attr)

    # Calculate the differences in coordinates
    dx = horizontal_2 - horizontal_1
    dy = vertical_2 - vertical_1

    # Calculate the angle using atan2 for correct quadrant determination
    angle = math.atan2(dy, dx)

    # Normalize angle to be in the range [0, 2*pi]
    if angle < 0:
        angle += 2 * math.pi

    return angle


def rotate_linearring(linearring: LinearRing, angle_degrees: float) -> LinearRing:
    """
    Rotate a Shapely LinearRing around its centroid by a specified angle.

    Parameters
    ----------
    linearring : LinearRing
        The Shapely LinearRing to be rotated
    angle_degrees : float
        The rotation angle in degrees (positive for counterclockwise)

    Returns
    -------
    LinearRing
        A new LinearRing that has been rotated

    Examples
    --------
    >>> from shapely.geometry import LinearRing
    >>> square = LinearRing([(0, 0), (1, 0), (1, 1), (0, 1)])
    >>> rotated = rotate_linearring(square, 45)
    """
    # Convert angle from degrees to radians
    angle_radians = np.radians(angle_degrees)

    # Get the centroid as the rotation point
    centroid = linearring.centroid

    # Extract coordinates from the LinearRing
    coords = list(linearring.coords)

    # Create rotation matrix
    rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians)], [np.sin(angle_radians), np.cos(angle_radians)]])

    # Initialize an empty list for the rotated coordinates
    rotated_coords = []

    # Define a threshold for floating-point precision
    presition_threshold = 1e-10

    # Rotate each point around the centroid
    for point in coords:
        # Translate point to origin (subtract centroid coordinates)
        translated = np.array([point[0] - centroid.x, point[1] - centroid.y])

        # Apply rotation
        rotated_point = np.dot(rotation_matrix, translated)

        # Apply numerical precision fix - round values very close to zero to exactly zero
        rotated_point = np.where(np.abs(rotated_point) < presition_threshold, 0, rotated_point)

        # Translate back (add centroid coordinates)
        final_point = (rotated_point[0] + centroid.x, rotated_point[1] + centroid.y)

        # Append to the list of rotated coordinates
        rotated_coords.append(final_point)

    # Create and return a new LinearRing with the rotated coordinates
    return LinearRing(rotated_coords)
