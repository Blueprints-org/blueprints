"""Rectangular cross-section shape."""

from dataclasses import dataclass

import numpy as np
from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


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
    name : str
        The name of the rectangular cross-section, default is "Rectangle".
    """

    width: MM
    height: MM
    x: MM = 0
    y: MM = 0
    name: str = "Rectangle"

    def __post_init__(self) -> None:
        """Post-initialization to validate the width and height."""
        if self.width <= 0:
            raise ValueError(f"Width must be a positive value, but got {self.width}")
        if self.height <= 0:
            raise ValueError(f"Height must be a positive value, but got {self.height}")

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
        return self.width * self.height

    @property
    def plate_thickness(self) -> MM:
        """
        Get the thickness of the rectangular cross-section.

        Returns
        -------
        MM
            The thickness of the rectangle.
        """
        return min(self.width, self.height)

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the rectangular cross-section.

        Returns
        -------
        MM
            The perimeter of the rectangle.
        """
        return 2 * (self.width + self.height)

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the rectangular cross-section.

        Returns
        -------
        Point
            The centroid of the rectangle.
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
        return (self.width * self.height**3) / 12

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return (self.height * self.width**3) / 12

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the positive z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / (self.height / 2)

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the negative z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / (self.height / 2)

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the positive y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / (self.width / 2)

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the negative y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / (self.width / 2)

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """
        Plastic section modulus about the y-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return (self.width * self.height**2) / 4

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return (self.height * self.width**2) / 4

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

    def dotted_mesh(self, max_mesh_size: MM = 0) -> list[Point]:
        """
        Mesh the rectangular cross-section with a given mesh size and return the inner nodes of
        each rectangle they represent.

        Parameters
        ----------
        max_mesh_size : MM
            The maximum mesh size to use for the meshing. Default is a fourth of the smallest dimension.

        Returns
        -------
        list[Point]
            The inner nodes of the meshed rectangles they represent.
        """
        if max_mesh_size == 0:
            mesh_size_width = min(self.width, self.height) / 4
            mesh_size_height = mesh_size_width
        else:
            mesh_size_width = self.width / np.ceil(self.width / max_mesh_size)
            mesh_size_height = self.height / np.ceil(self.height / max_mesh_size)

        x_min, y_min, x_max, y_max = self.geometry.bounds
        x_range = np.arange(x_min, x_max, mesh_size_width)
        y_range = np.arange(y_min, y_max, mesh_size_height)
        return [Point(x + mesh_size_width / 2, y + mesh_size_height / 2) for x in x_range for y in y_range]
