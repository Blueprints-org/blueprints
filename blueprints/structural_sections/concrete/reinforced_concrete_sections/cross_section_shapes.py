"""Cross-section shapes for reinforced concrete sections."""

import math
from dataclasses import dataclass, field
from typing import Protocol

from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2


@dataclass
class CircularCrossSection:
    """
    Class to represent a circular cross-section using shapely for geometric calculations.

    Parameters
    ----------
    radius : MM
        The radius of the circular cross-section.
    x : MM
        The x-coordinate of the circle's center.
    y : MM
        The y-coordinate of the circle's center.
    """

    radius: MM
    x: MM
    y: MM

    def __post_init__(self) -> None:
        """Post-initialization to create a shapely Point and buffer it to create a circular polygon."""
        # Create a Point at the specified origin (x, y)
        self.center = Point(self.x, self.y)
        # Create a circular polygon with the given radius
        self.circle = self.center.buffer(self.radius)

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the circular cross-section [mm²].

        Returns
        -------
        float
            The area of the circle.
        """
        return math.pi * self.radius**2.0

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter (circumference) of the circular cross-section [mm].

        Returns
        -------
        float
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
        return self.circle.centroid

    @property
    def vertices(self) -> list[Point]:
        """Vertices of the circular cross-section."""
        return [Point(x, y) for x, y in self.circle.exterior.coords]

    def contains_point(self, x: MM, y: MM) -> bool:
        """
        Check if a point (x, y) is inside the circular cross-section.

        Parameters
        ----------
        x : MM
            The x-coordinate of the point [mm].
        y : MM
            The y-coordinate of the point [mm].

        Returns
        -------
        bool
            True if the point is inside the circle, False otherwise.
        """
        # Check if the point is within the circular polygon
        return self.circle.contains(Point(x, y))


@dataclass
class RectangularCrossSection:
    """
    Class to represent a rectangular cross-section for geometric calculations.

    Parameters
    ----------
    width : MM
        The width of the rectangular cross-section.
    height : MM
        The height of the rectangular cross-section.
    origin : Point
        The centroid of the rectangle, given as a shapely Point. Default is (0, 0).
    """

    width: MM
    height: MM
    origin: Point = field(default_factory=lambda: Point(0, 0))

    def __post_init__(self) -> None:
        """
        Post-initialization to create a shapely Polygon representing the rectangle
        with the origin as the centroid.
        """
        # Calculate the bottom-left corner coordinates based on the centroid (origin)
        self.x = self.origin.x - self.width / 2
        self.y = self.origin.y - self.height / 2

        # Define the coordinates of the rectangle based on width, height, x, and y. Counter-clockwise order.
        self.rectangle = Polygon(
            [
                (self.x, self.y),
                (self.x + self.width, self.y),
                (self.x + self.width, self.y + self.height),
                (self.x, self.y + self.height),
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
        return self.rectangle.area

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the rectangular cross-section.

        Returns
        -------
        MM
            The perimeter of the rectangle.
        """
        return self.rectangle.length

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the rectangular cross-section.

        Returns
        -------
        Point
            The centroid of the rectangle.
        """
        return self.rectangle.centroid

    @property
    def vertices(self) -> list[Point]:
        """Vertices of the rectangular cross-section. Counter-clockwise order starting from the bottom-left corner."""
        return [Point(x, y) for x, y in self.rectangle.exterior.coords]

    def contains_point(self, x: MM, y: MM) -> bool:
        """
        Check if a point (x, y) is inside the rectangular cross-section.

        Parameters
        ----------
        x : MM
            The x-coordinate of the point.
        y : MM
            The y-coordinate of the point.

        Returns
        -------
        bool
            True if the point is inside the rectangle, False otherwise.
        """
        # Check if the point is within the rectangular polygon
        return self.rectangle.contains(Point(x, y))


class CrossSection(Protocol):
    """Protocol for a cross-section."""

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

    def contains_point(self, x: MM, y: MM) -> bool:
        """Check if a point (x, y) is inside the cross-section."""
