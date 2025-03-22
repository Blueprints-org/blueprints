"""Hexagonal cross-section shape."""

import math
from dataclasses import dataclass

import numpy as np
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
    def plate_thickness(self) -> MM:
        """
        Calculate the plate thickness of the hexagonal cross-section [mm].

        Returns
        -------
        MM
            The plate thickness of the hexagon.
        """
        return self.side_length * math.sqrt(3)

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

    def dotted_mesh(self, mesh_size: MM = 0) -> list[tuple[Point, MM2]]:
        """
        Mesh the hexagonal cross-section with a given mesh size and return the inner nodes of
        each rectangle along with the area they represent.

        Parameters
        ----------
        mesh_size : MM
            The mesh size to use for the meshing. Default is a tenth of the side length.

        Returns
        -------
        list[tuple[Point, MM2]]
            The inner nodes of the meshed rectangles along with the area they represent.
        """
        if mesh_size == 0:
            mesh_size = self.side_length / 10

        x_min, y_min, x_max, y_max = self.geometry.bounds
        x_range = np.arange(x_min, x_max, mesh_size)
        y_range = np.arange(y_min, y_max, mesh_size)
        return [
            (Point(x + mesh_size / 2, y + mesh_size / 2), mesh_size**2)
            for x in x_range
            for y in y_range
            if self.geometry.contains(Point(x + mesh_size / 2, y + mesh_size / 2))
        ]


if __name__ == "__main__":
    # Example usage of HexagonalCrossSection to get the mesh
    hex_section = HexagonalCrossSection(side_length=100, x=0, y=0)
    mesh = hex_section.dotted_mesh()

    import matplotlib.pyplot as plt

    # Extract x and y coordinates from the mesh nodes
    x_coords = [node.x for node, _ in mesh]
    y_coords = [node.y for node, _ in mesh]

    # Create the plot
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, s=10, c="blue", marker="o")
    plt.title("Mesh Points of Hexagonal Cross-Section")
    plt.xlabel("X Coordinate (mm)")
    plt.ylabel("Y Coordinate (mm)")
    plt.grid(True)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()
