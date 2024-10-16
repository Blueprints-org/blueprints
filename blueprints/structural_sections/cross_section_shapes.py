"""Cross-section shapes for reinforced concrete sections."""

import math
from dataclasses import dataclass
from typing import Protocol

from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2


@dataclass(frozen=True)
class CircularCrossSection:
    """
    Class to represent a circular cross-section using shapely for geometric calculations.

    Parameters
    ----------
    diameter : MM
        The diameter of the circular cross-section [mm].
    x : MM
        The x-coordinate of the circle's center.
    y : MM
        The y-coordinate of the circle's center.
    """

    diameter: MM
    x: MM
    y: MM

    def __post_init__(self) -> None:
        """Post-initialization to validate the diameter."""
        if self.diameter <= 0:
            msg = f"Diameter must be a positive value, but got {self.diameter}"
            raise ValueError(msg)

    @property
    def radius(self) -> MM:
        """
        Calculate the radius of the circular cross-section [mm].

        Returns
        -------
        MM
            The radius of the circle.
        """
        return self.diameter / 2.0

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the circular cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the circle.
        """
        return self.centroid.buffer(self.radius)

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the circular cross-section [mm²].

        Returns
        -------
        MM2
            The area of the circle.
        """
        return math.pi * self.radius**2.0

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter (circumference) of the circular cross-section [mm].

        Returns
        -------
        MM
            The perimeter of the circle.
        """
        return math.pi * self.radius * 2.0

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the circular cross-section.

        Returns
        -------
        Point
            The centroid of the circle.
        """
        return Point(self.x, self.y)

    @property
    def vertices(self) -> list[Point]:
        """
        Vertices of the circular cross-section.

        Returns
        -------
        list[Point]
            The vertices of the circle.
        """
        return [Point(x, y) for x, y in self.geometry.exterior.coords]


@dataclass(frozen=True)
class RectangularCrossSection:
    """
    Class to represent a rectangular cross-section for geometric calculations.

    Parameters
    ----------
    width : MM
        The width of the rectangular cross-section.
    height : MM
        The height of the rectangular cross-section.
    x : MM
        The x-coordinate of the centroid of the rectangle. Default is 0.
    y : MM
        The y-coordinate of the centroid of the rectangle. Default is 0.
    """

    width: MM
    height: MM
    x: MM = 0
    y: MM = 0

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the rectangular cross-section. Defines the coordinates of the rectangle based on width, height, x,
        and y. Counter-clockwise order.

        Returns
        -------
        Polygon
            The shapely Polygon representing the rectangle.
        """
        left_lower = (self.x - self.width / 2, self.y - self.height / 2)
        right_lower = (self.x + self.width / 2, self.y - self.height / 2)
        right_upper = (self.x + self.width / 2, self.y + self.height / 2)
        left_upper = (self.x - self.width / 2, self.y + self.height / 2)
        return Polygon(
            [
                left_lower,
                right_lower,
                right_upper,
                left_upper,
            ]
        )

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the rectangular cross-section.

        Returns
        -------
        MM2
            The area of the rectangle.
        """
        return self.geometry.area

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the rectangular cross-section.

        Returns
        -------
        MM
            The perimeter of the rectangle.
        """
        return self.geometry.length

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the rectangular cross-section.

        Returns
        -------
        Point
            The centroid of the rectangle.
        """
        return self.geometry.centroid

    @property
    def vertices(self) -> list[Point]:
        """
        Vertices of the rectangular cross-section. Counter-clockwise order starting from the bottom-left corner.

        Returns
        -------
        list[Point]
            The vertices of the rectangle.
        """
        return [Point(x, y) for x, y in self.geometry.exterior.coords]


class CrossSection(Protocol):
    """Protocol for a cross-section."""

    @property
    def geometry(self) -> Polygon:
        """Shapely Polygon representing the cross-section."""

    @property
    def area(self) -> MM2:
        """Area of the cross-section [mm²]."""

    @property
    def perimeter(self) -> MM:
        """Perimeter of the cross-section [mm]."""

    @property
    def centroid(self) -> Point:
        """Centroid of the cross-section [mm]."""

    @property
    def vertices(self) -> list[Point]:
        """Vertices of the cross-section."""
