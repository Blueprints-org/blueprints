"""Hexagonal cross-section shape."""

import math
from dataclasses import dataclass

from shapely.geometry import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class HexagonalCrossSection:
    """
    Class to represent a hexagonal cross-section using shapely for geometric calculations.

    Parameters
    ----------
    side_length : MM
        The side length of the hexagonal cross-section [mm].
    x : MM
        The x-coordinate of the hexagon's center.
    y : MM
        The y-coordinate of the hexagon's center.
    """

    side_length: MM
    x: MM
    y: MM

    def __post_init__(self) -> None:
        """Post-initialization to validate the side length."""
        if self.side_length <= 0:
            msg = f"Side length must be a positive value, but got {self.side_length}"
            raise ValueError(msg)

    @property
    def radius(self) -> MM:
        """
        Calculate the radius of the circumscribed circle of the hexagon [mm].

        Returns
        -------
        MM
            The radius of the circumscribed circle.
        """
        return self.side_length * math.sqrt(3) / 2.0

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the hexagonal cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the hexagon.
        """
        angle = math.pi / 3
        points = [(self.x + self.radius * math.cos(i * angle), self.y + self.radius * math.sin(i * angle)) for i in range(6)]
        return Polygon(points)

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the hexagonal cross-section [mm²].

        Returns
        -------
        MM2
            The area of the hexagon.
        """
        return (3 * math.sqrt(3) / 2) * self.side_length**2

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the hexagonal cross-section [mm].

        Returns
        -------
        MM
            The perimeter of the hexagon.
        """
        return 6 * self.side_length

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the hexagonal cross-section.

        Returns
        -------
        Point
            The centroid of the hexagon.
        """
        return Point(self.x, self.y)

    @property
    def moment_of_inertia_about_y(self) -> MM4:
        """
        Moments of inertia of the cross-section about the y-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the y-axis.
        """
        return (5 / 16) * math.sqrt(3) * self.side_length**4

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return (5 / 16) * math.sqrt(3) * self.side_length**4

    @property
    def polar_moment_of_inertia(self) -> MM4:
        """
        Polar moments of inertia of the cross-section [mm⁴].

        Returns
        -------
        MM4
            The polar moment of inertia.
        """
        return (5 / 8) * math.sqrt(3) * self.side_length**4

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the positive z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / (self.side_length * math.sqrt(3) / 2)

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the negative z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / (self.side_length * math.sqrt(3) / 2)

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the positive y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / (self.side_length * math.sqrt(3) / 2)

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the negative y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / (self.side_length * math.sqrt(3) / 2)

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """
        Plastic section modulus about the y-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return (self.side_length**3) * math.sqrt(3) / 4

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return (self.side_length**3) * math.sqrt(3) / 4

    @property
    def vertices(self) -> list[Point]:
        """
        Vertices of the hexagonal cross-section.

        Returns
        -------
        list[Point]
            The vertices of the hexagon.
        """
        return [Point(x, y) for x, y in self.geometry.exterior.coords]
