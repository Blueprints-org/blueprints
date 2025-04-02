"""Circular tube cross-section shape."""

import math
from dataclasses import dataclass

import numpy as np
from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class TubeCrossSection:
    """
    Class to represent a circular tube cross-section using shapely for geometric calculations.

    Parameters
    ----------
    outer_diameter : MM
        The outer diameter of the circular tube cross-section [mm].
    inner_diameter : MM
        The inner diameter of the circular tube cross-section [mm].
    x : MM
        The x-coordinate of the tube's center.
    y : MM
        The y-coordinate of the tube's center.
    name : str
        The name of the rectangular cross-section, default is "Tube".
    """

    outer_diameter: MM
    inner_diameter: MM
    x: MM
    y: MM
    name: str = "Tube"

    def __post_init__(self) -> None:
        """Post-initialization to validate the diameters."""
        if self.outer_diameter <= 0:
            msg = f"Outer diameter must be a positive value, but got {self.outer_diameter}"
            raise ValueError(msg)
        if self.inner_diameter < 0:
            msg = f"Inner diameter cannot be negative, but got {self.inner_diameter}"
            raise ValueError(msg)
        if self.inner_diameter >= self.outer_diameter:
            msg = f"Inner diameter must be smaller than outer diameter, but got inner: {self.inner_diameter}, outer: {self.outer_diameter}"
            raise ValueError(msg)

    @property
    def outer_radius(self) -> MM:
        """
        Calculate the outer radius of the circular tube cross-section [mm].

        Returns
        -------
        MM
            The outer radius of the tube.
        """
        return self.outer_diameter / 2.0

    @property
    def inner_radius(self) -> MM:
        """
        Calculate the inner radius of the circular tube cross-section [mm].

        Returns
        -------
        MM
            The inner radius of the tube.
        """
        return self.inner_diameter / 2.0

    @property
    def wall_thickness(self) -> MM:
        """
        Calculate the thickness of the tube wall [mm].

        Returns
        -------
        MM
            The thickness of the tube wall.
        """
        return self.outer_radius - self.inner_radius

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the circular tube cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the tube.
        """
        resolution = 100
        outer_circle = self.centroid.buffer(self.outer_radius, resolution=resolution)
        inner_circle = self.centroid.buffer(self.inner_radius, resolution=resolution)
        return Polygon(outer_circle.difference(inner_circle))

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the circular tube cross-section [mm²].

        Returns
        -------
        MM2
            The area of the tube.
        """
        return math.pi * (self.outer_radius**2.0 - self.inner_radius**2.0)

    @property
    def plate_thickness(self) -> MM:
        """
        Calculate the thickness of the tube wall [mm].

        Returns
        -------
        MM
            The thickness of the tube wall.
        """
        return (self.outer_diameter - self.inner_diameter) / 2.0

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter (circumference) of the circular tube cross-section [mm].

        Returns
        -------
        MM
            The perimeter of the tube.
        """
        return 2.0 * math.pi * (self.outer_radius + self.inner_radius)

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the circular tube cross-section.

        Returns
        -------
        Point
            The centroid of the tube.
        """
        return Point(self.x, self.y)

    @property
    def moment_of_inertia_about_y(self) -> MM4:
        """
        Moments of inertia of the tube cross-section about the y-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the y-axis.
        """
        return (math.pi / 64) * (self.outer_diameter**4 - self.inner_diameter**4)

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the tube cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return (math.pi / 64) * (self.outer_diameter**4 - self.inner_diameter**4)

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the positive z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / self.outer_radius

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the negative z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / self.outer_radius

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the positive y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / self.outer_radius

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the negative y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / self.outer_radius

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """
        Plastic section modulus about the y-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return (self.outer_diameter**3 - self.inner_diameter**3) / 6

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return (self.outer_diameter**3 - self.inner_diameter**3) / 6

    @property
    def vertices(self) -> list[Point]:
        """
        Vertices of the circular tube cross-section.

        Returns
        -------
        list[Point]
            The vertices of the tube.
        """
        return [Point(x, y) for x, y in self.geometry.exterior.coords]

    def dotted_mesh(self, max_mesh_size: MM = 0) -> list[Point]:
        """
        Mesh the circular tube cross-section with a given mesh size and return the inner nodes of each
        rectangle they represent.

        Parameters
        ----------
        max_mesh_size : MM
            The maximum mesh size to use for the meshing. Default is a quarter of the thickness and 20th of diameter,
            whichever is less.

        Returns
        -------
        list[Point]
            The inner nodes of the meshed rectangles they represent.
        """
        if max_mesh_size == 0:
            mesh_size = min(self.plate_thickness / 4, self.outer_diameter / 20)
        else:
            mesh_size = self.plate_thickness / np.ceil(self.plate_thickness / max_mesh_size)

        x_min, y_min, x_max, y_max = self.geometry.bounds
        x_range = np.arange(x_min, x_max, mesh_size)
        y_range = np.arange(y_min, y_max, mesh_size)
        return [
            Point(float(x + mesh_size / 2), float(y + mesh_size / 2))
            for x in x_range
            for y in y_range
            if self.inner_radius < math.sqrt(float((x + mesh_size / 2 - self.x) ** 2 + (y + mesh_size / 2 - self.y) ** 2)) < self.outer_radius
        ]
