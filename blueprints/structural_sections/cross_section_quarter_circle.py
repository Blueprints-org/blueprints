"""Quarter circular cross-section shape."""

import math
from dataclasses import dataclass

from shapely.geometry import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class QuarterCircularCrossSection:
    """
    Class to represent a quarter circular cross-section using shapely for geometric calculations.

    Parameters
    ----------
    diameter : MM
        The diameter of the quarter circular cross-section [mm].
    x : MM
        The x-coordinate of the quarter circle's center.
    y : MM
        The y-coordinate of the quarter circle's center.
    flip_horizontal : bool
        Whether to flip the quarter circle horizontally.
    flip_vertical : bool
        Whether to flip the quarter circle vertically.
    """

    diameter: MM
    x: MM
    y: MM
    flip_horizontal: bool = False
    flip_vertical: bool = False

    def __post_init__(self) -> None:
        """Post-initialization to validate the diameter."""
        if self.diameter <= 0:
            msg = f"Diameter must be a positive value, but got {self.diameter}"
            raise ValueError(msg)

    @property
    def radius(self) -> MM:
        """
        Calculate the radius of the quarter circular cross-section [mm].

        Returns
        -------
        MM
            The radius of the quarter circle.
        """
        return self.diameter / 2.0

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the quarter circular cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the quarter circle.
        """
        center = Point(self.x, self.y)
        circle = center.buffer(self.radius)
        if self.flip_horizontal and self.flip_vertical:
            quarter_circle = Polygon(
                [
                    (self.x, self.y),
                    (self.x - self.radius, self.y),
                    (self.x - self.radius, self.y - self.radius),
                    (self.x, self.y - self.radius),
                    (self.x, self.y),
                ]
            )
        elif self.flip_horizontal:
            quarter_circle = Polygon(
                [
                    (self.x, self.y),
                    (self.x - self.radius, self.y),
                    (self.x - self.radius, self.y + self.radius),
                    (self.x, self.y + self.radius),
                    (self.x, self.y),
                ]
            )
        elif self.flip_vertical:
            quarter_circle = Polygon(
                [
                    (self.x, self.y),
                    (self.x + self.radius, self.y),
                    (self.x + self.radius, self.y - self.radius),
                    (self.x, self.y - self.radius),
                    (self.x, self.y),
                ]
            )
        else:
            quarter_circle = Polygon(
                [
                    (self.x, self.y),
                    (self.x + self.radius, self.y),
                    (self.x + self.radius, self.y + self.radius),
                    (self.x, self.y + self.radius),
                    (self.x, self.y),
                ]
            )
        return quarter_circle.intersection(circle)

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the quarter circular cross-section [mm²].

        Returns
        -------
        MM2
            The area of the quarter circle.
        """
        return (math.pi * self.radius**2.0) / 4.0

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the quarter circular cross-section [mm].

        Returns
        -------
        MM
            The perimeter of the quarter circle.
        """
        return (math.pi * self.radius / 2.0) + 2 * self.radius

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the quarter circular cross-section.

        Returns
        -------
        Point
            The centroid of the quarter circle.
        """
        return Point(self.x + (4 * self.radius) / (3 * math.pi), self.y + (4 * self.radius) / (3 * math.pi))

    @property
    def moment_of_inertia_about_y(self) -> MM4:
        """
        Moments of inertia of the cross-section about the y-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the y-axis.
        """
        return (math.pi / 64) * self.diameter**4 / 4 - self.area * (self.radius - (4 * self.radius) / (3 * math.pi)) ** 2

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return (math.pi / 64) * self.diameter**4 / 4 - self.area * (self.radius - (4 * self.radius) / (3 * math.pi)) ** 2

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the positive z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        distance_to_end = self.radius - (4 * self.radius) / (3 * math.pi)
        return self.moment_of_inertia_about_y / distance_to_end

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the negative z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        distance_to_end = (4 * self.radius) / (3 * math.pi)
        return self.moment_of_inertia_about_y / distance_to_end

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the positive y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        distance_to_end = self.radius - (4 * self.radius) / (3 * math.pi)
        return self.moment_of_inertia_about_z / distance_to_end

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the negative y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        distance_to_end = (4 * self.radius) / (3 * math.pi)
        return self.moment_of_inertia_about_z / distance_to_end

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """
        Plastic section modulus about the y-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return (self.diameter**3) / 6

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return (self.diameter**3) / 6

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
