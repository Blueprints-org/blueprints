"""Line module."""

from itertools import pairwise
from typing import Literal, Self

import numpy as np
from shapely import Point

from blueprints.geometry.operations import CoordinateSystemOptions, calculate_rotation_angle
from blueprints.type_alias import DEG
from blueprints.unit_conversion import RAD_TO_DEG


class Line:
    """Represents a line in a 3D modelling space.

    Parameters
    ----------
    start_point : Point
        Starting point
    end_point : Point
        End point
    """

    id: int = 0

    def __init__(self, start_point: Point, end_point: Point) -> None:
        """Initialize the line."""
        self._start_point = start_point
        self._end_point = end_point
        self._validate_points()
        Line.id += 1

    @property
    def start_point(self) -> Point:
        """Return the start point."""
        return self._start_point

    @start_point.setter
    def start_point(self, value: Point) -> None:
        """Set the start point."""
        self._start_point = value
        self._validate_points()

    @property
    def end_point(self) -> Point:
        """Return the end point."""
        return self._end_point

    @end_point.setter
    def end_point(self, value: Point) -> None:
        """Set the end point."""
        self._end_point = value
        self._validate_points()

    @property
    def _start(self) -> np.ndarray:
        """Return the start point as a numpy array."""
        return np.array(self._start_point.coords)

    @property
    def _end(self) -> np.ndarray:
        """Return the end point as a numpy array."""
        return np.array(self._end_point.coords)

    def _validate_points(self) -> None:
        """Validate if the points are different."""
        # Check if start and end point are the same
        if list(self.start_point.coords) == list(self.end_point.coords):
            msg = f"Start and end point can't be equal. {self.start_point=} | {self.end_point=}"
            raise ValueError(msg)

        # if points have no z value, then declare zero as default
        if not self.start_point.has_z:
            self.start_point = Point(self.start_point.x, self.start_point.y, 0.0)
        if not self.end_point.has_z:
            self.end_point = Point(self.end_point.x, self.end_point.y, 0.0)

    @property
    def midpoint(self) -> Point:
        """Midpoint of the line."""
        return Point((self._start + self._end) / 2)

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
        return float(np.linalg.norm(self._end - self._start))

    def angle(self, coordinate_system: CoordinateSystemOptions = CoordinateSystemOptions.XY) -> DEG:
        """
        Calculates rotation of the end point in relation to the start point in a given plane/coordinate system [deg].

        - The rotation is calculated in the given plane in relation to the start point.
        - The rotation is calculated in the range [0, 2*pi].
        - The rotation is calculated in the counter-clockwise direction.

        Parameters
        ----------
        coordinate_system: CoordinateSystemOptions
            Desired plane that will be used as reference to calculate the rotation. Standard is XY-plane.

        Returns
        -------
        DEG
            rotation of end point relative to the start point in degrees in the given plane [deg].
        """
        return (
            calculate_rotation_angle(
                start_point=self.start_point,
                end_point=self.end_point,
                coordinate_system=coordinate_system,
            )
            * RAD_TO_DEG
        )

    @property
    def unit_vector(self) -> np.ndarray:
        """Return the unit vector of the line."""
        return (self._end - self._start) / self.length

    def get_internal_point(self, distance: float, reference: Literal["start", "end"] = "start") -> Point:
        """Return an internal point within the line in a given distance from the reference point.

        Parameters
        ----------
        distance : float
            Distance from the given reference point following the axis of the line
        reference: Literal["start", "end"]
            Reference point in the line where given distance is declared. Default -> "start"

        Returns
        -------
        Point
            Internal point within the line in a given distance from the reference point.

        Raises
        ------
        ValueError
            If the distance is greater than the total length of the line.
            If the distance is a negative number.
        """
        if distance > self.length:
            msg = f"Distance must be equal or less than total length of the line. Length={self.length} | Distance={distance}"
            raise ValueError(msg)
        if distance < 0:
            msg = "Given Distance must be a positive number."
            raise ValueError(msg)

        match reference.lower():
            case "start":
                internal_point = self._start + distance * self.unit_vector
            case "end":
                internal_point = self._end - distance * self.unit_vector
            case _:
                msg = f"'{reference}' is an invalid input for 'reference_point', use 'start' or 'end'."
                raise ValueError(msg)
        return Point(internal_point)

    def adjust_length(self, distance: float, direction: Literal["start", "end"] = "end") -> Self:
        """Extends or shortens the line in a given direction. The end of the line is the default direction.

        Parameters
        ----------
        distance : float
            Distance to extend or shorten the line. Positive number extends the line, negative number shortens the line.
        direction: Literal["start", "end"]
            Given direction where the line needs to be extended. Default towards the end of the line.

        Returns
        -------
        Line
            The new line with the adjusted length.
        """
        if distance < 0 and abs(distance) >= self.length:
            raise ValueError("When shortening the line, the absolute value of the extra length must be less than the total length of the line.")

        match direction.lower():
            case "end":
                new_point = self._end + distance * self.unit_vector
                self.end_point = Point(new_point)
            case "start":
                new_point = self._start - distance * self.unit_vector
                self.start_point = Point(new_point)
            case _:
                msg = "Invalid input for 'direction', use 'start' or 'end'."
                raise ValueError(msg)
        return self

    def get_evenly_spaced_points(self, n: int = 2) -> list[Point]:
        """Return a list of evenly spaced internal points of the line from start to end point with an n number of desired points.

        Parameters
        ----------
        n : int
            Total number of internal points desired. A minimum of 2 points are required.
        """
        if not isinstance(n, int):
            msg = "n must be an integer"
            raise TypeError(msg)
        if n < 2:
            msg = "n must be equal or greater than 2"
            raise ValueError(msg)

        # Create a list of evenly spaced points
        evenly_spaced_points = np.linspace(start=0, stop=self.length, num=n, endpoint=True)

        return [Point(self._start + distance * self.unit_vector) for distance in evenly_spaced_points]

    def divide_into_n_lines(self, n: int = 2) -> list["Line"]:
        """Return a list of evenly divided lines.

        Parameters
        ----------
        n : int
            Total number of lines desired. A minimum of 2 lines are required.
        """
        if not isinstance(n, int):
            msg = "n must be an integer"
            raise TypeError(msg)
        if n < 2:
            msg = "n must be equal or greater than 2"
            raise ValueError(msg)

        evenly_spaced_points = self.get_evenly_spaced_points(n + 1)
        return [Line(start_point=point_1, end_point=point_2) for point_1, point_2 in pairwise(evenly_spaced_points)]

    def __eq__(self, other: object) -> bool:
        """Return True if the lines are equal."""
        if not isinstance(other, Line):
            raise NotImplementedError("Line can only be compared to other Line object")
        return np.allclose(self._start, other._start) and np.allclose(self._end, other._end)

    def __repr__(self) -> str:
        """Return the representation of the line."""
        return f"Line({self.start_point}, {self.end_point})"
