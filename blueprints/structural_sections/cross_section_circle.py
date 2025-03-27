"""Circular cross-section shape."""

import math
from dataclasses import dataclass

import numpy as np
from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class CircularCrossSection:
    """
    Class to represent a circular cross-section using shapely for geometric calculations.

    Parameters
    ----------
    name : str
        The name of the rectangular cross-section.
    diameter : MM
        The diameter of the circular cross-section [mm].
    x : MM
        The x-coordinate of the circle's center.
    y : MM
        The y-coordinate of the circle's center.
    """

    name: str
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
    def plate_thickness(self) -> MM:
        """
        Get the plate thickness of the circular cross-section.

        Returns
        -------
        MM
            The plate thickness of the circle.
        """
        return self.diameter

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
    def moment_of_inertia_about_y(self) -> MM4:
        """
        Moments of inertia of the cross-section about the y-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the y-axis.
        """
        return (math.pi / 64) * self.diameter**4

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return (math.pi / 64) * self.diameter**4

    @property
    def polar_moment_of_inertia(self) -> MM4:
        """
        Polar moments of inertia of the cross-section [mm⁴].

        Returns
        -------
        MM4
            The polar moment of inertia.
        """
        return (math.pi / 32) * self.diameter**4

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the positive z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / (self.diameter / 2)

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the negative z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / (self.diameter / 2)

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the positive y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / (self.diameter / 2)

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the negative y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / (self.diameter / 2)

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

    def dotted_mesh(self, max_mesh_size: MM = 0) -> list[Point]:
        """
        Mesh the circular cross-section with a given mesh size and return the inner nodes of
        each rectangle they represent.

        Parameters
        ----------
        max_mesh_size : MM
            The maximum mesh size to use for the meshing. Default is a twentieth of the diameter.

        Returns
        -------
        list[Point]
            The inner nodes of the meshed rectangles they represent.
        """
        mesh_size = self.diameter / 20 if max_mesh_size == 0 else self.diameter / np.ceil(self.diameter / max_mesh_size)

        x_min, y_min, x_max, y_max = self.geometry.bounds
        x_range = np.arange(x_min, x_max, mesh_size)
        y_range = np.arange(y_min, y_max, mesh_size)
        return [
            Point(x + mesh_size / 2, y + mesh_size / 2)
            for x in x_range
            for y in y_range
            if (x + mesh_size / 2 - self.x) ** 2 + (y + mesh_size / 2 - self.y) ** 2 <= self.radius**2
        ]
