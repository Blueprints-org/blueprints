"""Line module."""
# ruff: noqa: TRY004

from enum import Enum
from typing import Self  # type: ignore[attr-defined]

import numpy as np
from shapely import Point

from blueprints.geometry.operations import CoordinateSystemOptions, calculate_rotation_angle
from blueprints.type_alias import DEG
from blueprints.unit_conversion import RAD_TO_DEG


class Reference(Enum):
    """Enum of the reference options start/end."""

    START = 0
    END = 1


class Line:
    """Represents a line in the modelling space.

    Parameters
    ----------
    start_point : Point
        Starting point
    end_point : Point
        End point
    name : str
        Name of the Line; will get 'Line_{id}' if '' is given
    """

    id: int = 0

    def __init__(self, start_point: Point, end_point: Point, name: str = "") -> None:
        self.name = name
        if start_point == end_point:
            msg = f"Start and end point can't be equal. start={start_point} | end={end_point}"
            raise ValueError(msg)
        self.start_point = start_point
        self.end_point = end_point
        Line.id += 1

    @property
    def midpoint(self) -> Point:
        """Midpoint of the line."""
        midpoint_x_coordinate = self.start_point.x + ((self.length / 2) / self.length) * (self.end_point.x - self.start_point.x)
        midpoint_y_coordinate = self.start_point.y + ((self.length / 2) / self.length) * (self.end_point.y - self.start_point.y)
        midpoint_z_coordinate = self.start_point.z + ((self.length / 2) / self.length) * (self.end_point.z - self.start_point.z)
        return Point(midpoint_x_coordinate, midpoint_y_coordinate, midpoint_z_coordinate)

    @property
    def delta_x(self) -> float:
        """Difference in X-coordinate between starting and end point (X end - X start)."""
        return self.end_point.x - self.start_point.x

    @property
    def delta_y(self) -> float:
        """Difference in Y-coordinate between starting and end point (Y end - Y start)."""
        return self.end_point.y - self.start_point.y

    @property
    def delta_z(self) -> float:
        """Difference in Z-coordinate between starting and end point (Z end - Z start)."""
        return self.end_point.z - self.start_point.z

    @property
    def length(self) -> float:
        """Return the total length of the line."""
        return np.sqrt(
            (self.end_point.x - self.start_point.x) ** 2 + (self.end_point.y - self.start_point.y) ** 2 + (self.end_point.z - self.start_point.z) ** 2
        )

    def angle(self, coordinate_system: CoordinateSystemOptions = CoordinateSystemOptions.XY) -> DEG:
        """
        Calculates angle of rotation of the end point in relation to the start point in a given plane/coordinate system.
        Start point lies in the origin center of the quadrant [deg].

        Parameters
        ----------
        coordinate_system: CoordinateSystemOptions
            Desired plane that will be used as reference to calculate the rotation. Standard is XY-plane.

        Returns
        -------
        DEG
            rotation of end point relative to begin node in degrees in the given plane [deg].

        """
        return calculate_rotation_angle(self.start_point, self.end_point, coordinate_system) * RAD_TO_DEG

    def get_internal_point(self, distance: float, reference_point: Reference = Reference.START) -> Point:
        """Return an internal point within the line in a given distance from the reference point.

        Parameters
        ----------
        distance : float
            Distance from the given reference point following the axis of the line
        reference_point: Reference
            Reference point in the line where given distance is declared. Default -> Reference.START

        Returns
        -------
        Point
            Point within the line in a given distance from the reference point.
        """
        if distance > self.length:
            msg = f"Distance from start point must be equal or less than total length of the line. Length={self.length}"
            raise ValueError(msg)
        if distance < 0:
            msg = "Given Distance must be a positive number."
            raise ValueError(msg)

        match reference_point:
            case Reference.START:
                internal_x_coordinate = self.start_point.x + (distance / self.length) * (self.end_point.x - self.start_point.x)
                internal_y_coordinate = self.start_point.y + (distance / self.length) * (self.end_point.y - self.start_point.y)
                internal_z_coordinate = self.start_point.z + (distance / self.length) * (self.end_point.z - self.start_point.z)
            case Reference.END:
                internal_x_coordinate = self.end_point.x + (distance / self.length) * (self.start_point.x - self.end_point.x)
                internal_y_coordinate = self.end_point.y + (distance / self.length) * (self.start_point.y - self.end_point.y)
                internal_z_coordinate = self.end_point.z + (distance / self.length) * (self.start_point.z - self.end_point.z)
            case _:
                msg = "Invalid input for 'reference_point', use Reference.START or Reference.END"
                raise ValueError(msg)
        return Point(internal_x_coordinate, internal_y_coordinate, internal_z_coordinate)

    def extend(self, extra_length: float, direction: Reference = Reference.END) -> None:
        """Extends the line in a given direction. The end of the line is the default direction.

        Parameters
        ----------
        extra_length : float
            Distance to add to the total length of the line
        direction: Reference
            Given direction where the line needs to be extended. Default -> Direction.END

        Returns
        -------
        None
            It overrides the end point of the line. It does not have a return
        """
        match direction:
            case Reference.END:
                extra_x_coordinate = self.start_point.x + ((self.length + extra_length) / self.length) * (self.end_point.x - self.start_point.x)
                extra_y_coordinate = self.start_point.y + ((self.length + extra_length) / self.length) * (self.end_point.y - self.start_point.y)
                extra_z_coordinate = self.start_point.z + ((self.length + extra_length) / self.length) * (self.end_point.z - self.start_point.z)
                self.end_point = Point(extra_x_coordinate, extra_y_coordinate, extra_z_coordinate)
            case Reference.START:
                extra_x_coordinate = self.end_point.x + ((self.length + extra_length) / self.length) * (self.start_point.x - self.end_point.x)
                extra_y_coordinate = self.end_point.y + ((self.length + extra_length) / self.length) * (self.start_point.y - self.end_point.y)
                extra_z_coordinate = self.end_point.z + ((self.length + extra_length) / self.length) * (self.start_point.z - self.end_point.z)
                self.start_point = Point(extra_x_coordinate, extra_y_coordinate, extra_z_coordinate)
            case _:
                msg = "Invalid input for 'direction', use Reference.START or Reference.END"
                raise ValueError(msg)

    def get_evenly_spaced_points(self, n: int = 2) -> list[Point]:
        """Return a list of evenly spaced internal points of the line from start to end point with an n number of desired points.

        Parameters
        ----------
        n : int
            A minimum of 2 points are required.

        """
        if not isinstance(n, int):
            msg = "n must be an integer"
            raise ValueError(msg)
        if n < 2:
            msg = "n must be equal or greater than 2"
            raise ValueError(msg)

        internal_points = []

        evenly_spaced_points = np.linspace(0, self.length, num=n, endpoint=True)
        for distance in evenly_spaced_points:
            new_x_coordinate = self.start_point.x + (distance / self.length) * (self.end_point.x - self.start_point.x)
            new_y_coordinate = self.start_point.y + (distance / self.length) * (self.end_point.y - self.start_point.y)
            new_z_coordinate = self.start_point.z + (distance / self.length) * (self.end_point.z - self.start_point.z)
            internal_points.append(Point(new_x_coordinate, new_y_coordinate, new_z_coordinate))

        return internal_points

    def divide_into_n_lines(self, n: int = 2) -> list[Self]:
        """Return a list of evenly divided lines.

        Parameters
        ----------
        n : int
            A minimum of 2 segments are required.

        """
        if not isinstance(n, int):
            msg = "n must be an integer"
            raise ValueError(msg)
        if n < 2:
            msg = "n must be equal or greater than 2"
            raise ValueError(msg)

        evenly_spaced_points = self.get_evenly_spaced_points(n + 1)
        return [
            Line(start_point=evenly_spaced_points[position], end_point=evenly_spaced_points[position + 1])
            for position in range(len(evenly_spaced_points) - 1)
        ]

    def __eq__(self, other: object) -> bool:
        """Return True if the lines are equal."""
        if not isinstance(other, Line):
            raise NotImplementedError
        return self.length == other.length
