"""Triangular cross-section shape."""

import math
from dataclasses import dataclass

import numpy as np
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
        The x-coordinate of the 90-degree angle. Default is 0.
    y : MM
        The y-coordinate of the 90-degree angle. Default is 0.
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
        left_lower = (self.x, self.y)
        right_lower = (self.x + self.base, self.y)
        top = (self.x, self.y + self.height)

        if self.flipped_horizontally:
            right_lower = (2 * left_lower[0] - right_lower[0], right_lower[1])
        if self.flipped_vertically:
            top = (top[0], 2 * left_lower[1] - top[1])

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
    def plate_thickness(self) -> MM:
        """
        Calculate the plate thickness of the triangular cross-section.

        Returns
        -------
        MM
            The plate thickness of the triangle.
        """
        return min(self.base, self.height)

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
        return Point(self.x + self.base / 3, self.y + self.height / 3)

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

    def dotted_mesh(self, max_mesh_size: MM = 0) -> list[Point]:
        """
        Mesh the right-angled triangular cross-section with a given mesh size and return the inner nodes
        of each rectangle they represent.

        Parameters
        ----------
        max_mesh_size : MM
            The maximum mesh size to use for the meshing. Default is a twentieth of the smallest dimension.

        Returns
        -------
        list[Point]
            The inner nodes of the meshed rectangles they represent.
        """
        if max_mesh_size == 0:
            mesh_size_width = self.base / 20
            mesh_size_height = self.height / 20
        else:
            mesh_size_width = self.base / np.ceil(self.base / max_mesh_size)
            mesh_size_height = self.height / np.ceil(self.height / max_mesh_size)

        x_min, y_min, x_max, y_max = self.geometry.bounds
        x_range = np.arange(x_min, x_max, mesh_size_width)
        y_range = np.arange(y_min, y_max, mesh_size_height)

        # Shift the x-range by 1/100th of the mesh size to avoid diagonal issues with the mesh
        x_range = np.array([x + ((i % 2) * 2 - 1) * mesh_size_width / 100 for i, x in enumerate(x_range)])

        return [
            Point(x + mesh_size_width / 2, y + mesh_size_height / 2)
            for x in x_range
            for y in y_range
            if self.geometry.contains(Point(x + mesh_size_width / 2, y + mesh_size_height / 2))
        ]


if __name__ == "__main__":
    # Example usage of RightAngledTriangularCrossSection to get the mesh
    triangle_section = RightAngledTriangularCrossSection(base=10, height=20)
    mesh = triangle_section.dotted_mesh()

    import matplotlib.pyplot as plt

    # Extract x and y coordinates from the mesh nodes
    x_coords = [node.x for node in mesh]
    y_coords = [node.y for node in mesh]

    # Create the plot
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, s=10, c="blue", marker="o")
    plt.title("Mesh Points of Right-Angled Triangular Cross-Section" + f", amount of nodes: {len(mesh)}")
    plt.xlabel("X Coordinate (mm)")
    plt.ylabel("Y Coordinate (mm)")
    plt.grid(True)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()
