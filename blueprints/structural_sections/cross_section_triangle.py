"""Triangular cross-section shape."""

import math
from dataclasses import dataclass

from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class RightAngledTriangularCrossSection:
    """
    Class to represent a right-angled triangular with a right angle at the bottom left corner cross-section for geometric calculations.

    Parameters
    ----------
    base : MM
        The base length of the triangular cross-section.
    height : MM
        The height of the triangular cross-section.
    x : MM
        The x-coordinate of the centroid of the triangle. Default is 0.
    y : MM
        The y-coordinate of the centroid of the triangle. Default is 0.
    flipped_horizontally : bool
        Whether the triangle is flipped horizontally. Default is False.
    flipped_vertically : bool
        Whether the triangle is flipped vertically. Default is False.
    """

    base: MM
    height: MM
    x: MM = 0
    y: MM = 0
    flipped_horizontally: bool = False
    flipped_vertically: bool = False

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the right-angled triangular cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the triangle.
        """
        left_lower = (self.x - self.base / 2, self.y - self.height / 2)
        right_lower = (self.x + self.base / 2, self.y - self.height / 2)
        top = (self.x - self.base / 2, self.y + self.height / 2)

        if self.flipped_horizontally:
            left_lower, right_lower = right_lower, left_lower
        if self.flipped_vertically:
            left_lower, top = top, left_lower

        return Polygon([left_lower, right_lower, top])

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the triangular cross-section.

        Returns
        -------
        MM2
            The area of the triangle.
        """
        return self.base * self.height / 2

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the triangular cross-section.

        Returns
        -------
        MM
            The perimeter of the triangle.
        """
        return self.base + self.height + math.sqrt(self.base**2 + self.height**2)

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the triangular cross-section.

        Returns
        -------
        Point
            The centroid of the triangle.
        """
        return Point(self.x - self.base / 6, self.y - self.height / 6)

    @property
    def moment_of_inertia_about_y(self) -> MM4:
        """
        Moments of inertia of the cross-section about the y-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the y-axis.
        """
        return (self.base * self.height**3) / 36

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return (self.height * self.base**3) / 36

    @property
    def polar_moment_of_inertia(self) -> MM4:
        """
        Polar moments of inertia of the cross-section [mm⁴].

        Returns
        -------
        MM4
            The polar moment of inertia.
        """
        return self.moment_of_inertia_about_y + self.moment_of_inertia_about_z

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the positive z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        distance_to_end = self.height / 3 * 2
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
        distance_to_end = self.height / 3
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
        distance_to_end = self.base / 3 * 2
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
        distance_to_end = self.base / 3
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
        return (self.base * self.height**2) / 4

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return (self.height * self.base**2) / 4

    @property
    def vertices(self) -> list[Point]:
        """
        Vertices of the triangular cross-section.

        Returns
        -------
        list[Point]
            The vertices of the triangle.
        """
        return [Point(x, y) for x, y in self.geometry.exterior.coords]
