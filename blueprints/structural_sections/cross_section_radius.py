"""Triangular cross-section shape with a quarter circle."""

import math
from dataclasses import dataclass

import numpy as np
from shapely.geometry import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class RightAngleCurvedCrossSection:
    """
    Class to represent a right-angled triangular cross-section with a quarter circle for geometric calculations.

    Parameters
    ----------
    radius : MM
        The length of the two sides of the triangular cross-section.
    x : MM
        The x-coordinate of the 90-degree angle. Default is 0.
    y : MM
        The y-coordinate of the 90-degree angle. Default is 0.
    flipped_horizontally : bool
        Whether the triangle is flipped horizontally. Default is False.
    flipped_vertically : bool
        Whether the triangle is flipped vertically. Default is False.
    """

    radius: MM
    x: MM = 0
    y: MM = 0
    flipped_horizontally: bool = False
    flipped_vertically: bool = False

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the right-angled triangular cross-section with a quarter circle.

        Returns
        -------
        Polygon
            The shapely Polygon representing the shape.
        """
        left_lower = (self.x, self.y)

        # Approximate the quarter circle with 25 straight lines
        quarter_circle_points = [
            (self.x + self.radius - self.radius * math.cos(math.pi / 2 * i / 25), self.y + self.radius - self.radius * math.sin(math.pi / 2 * i / 25))
            for i in range(26)
        ]
        for i in range(26):
            if self.flipped_horizontally:
                quarter_circle_points[i] = (2 * left_lower[0] - quarter_circle_points[i][0], quarter_circle_points[i][1])
            if self.flipped_vertically:
                quarter_circle_points[i] = (quarter_circle_points[i][0], 2 * left_lower[1] - quarter_circle_points[i][1])

        return Polygon([left_lower, *quarter_circle_points])

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the cross-section.

        Returns
        -------
        MM2
            The area of the shape.
        """
        return self.radius**2 - (math.pi * self.radius**2 / 4)

    @property
    def plate_thickness(self) -> MM:
        """
        Calculate the plate thickness of the cross-section.

        Returns
        -------
        MM
            The plate thickness of the shape.
        """
        return self.radius

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the cross-section.

        Returns
        -------
        MM
            The perimeter of the shape.
        """
        return 2 * self.radius + (math.pi * self.radius / 2)

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the cross-section.

        Returns
        -------
        Point
            The centroid of the shape.
        """
        return Point(self.x + self.radius / 2, self.y + self.radius / 2)

    @property
    def moment_of_inertia_about_y(self) -> MM4:
        """
        Moments of inertia of the cross-section about the y-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the y-axis.
        """
        return (self.radius**4 / 36) + (math.pi * self.radius**4 / 64)

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return (self.radius**4 / 36) + (math.pi * self.radius**4 / 64)

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
        distance_to_end = self.radius / 3 * 2
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
        distance_to_end = self.radius / 3
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
        distance_to_end = self.radius / 3 * 2
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
        distance_to_end = self.radius / 3
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
        return (self.radius**3) / 4

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return (self.radius**3) / 4

    @property
    def vertices(self) -> list[Point]:
        """
        Vertices of the cross-section.

        Returns
        -------
        list[Point]
            The vertices of the shape.
        """
        return [Point(x, y) for x, y in self.geometry.exterior.coords]

    def dotted_mesh(self, max_mesh_size: MM = 0) -> list[Point]:
        """
        Mesh the right-angled triangular cross-section with a quarter circle with a given mesh size and
        return the inner nodes of each rectangle they represent.

        Parameters
        ----------
        max_mesh_size : MM
            The maximum mesh size to use for the meshing. Default is a twentieth of the radius.

        Returns
        -------
        list[Point]
            The inner nodes of the meshed rectangles they represent.
        """
        mesh_size = self.radius / 20 if max_mesh_size == 0 else self.radius / np.ceil(self.radius / max_mesh_size)

        x_min, y_min, x_max, y_max = self.geometry.bounds
        x_range = np.arange(x_min, x_max, mesh_size)
        y_range = np.arange(y_min, y_max, mesh_size)
        return [
            Point(x + mesh_size / 2, y + mesh_size / 2)
            for x in x_range
            for y in y_range
            if self.geometry.contains(Point(x + mesh_size / 2, y + mesh_size / 2))
            if self.geometry.contains(Point(x + mesh_size / 2, y + mesh_size / 2))
        ]


if __name__ == "__main__":
    # Example usage of RectangularCrossSection to get the mesh
    curve_section = RightAngleCurvedCrossSection(radius=100)
    mesh = curve_section.dotted_mesh()

    import matplotlib.pyplot as plt

    # Extract x and y coordinates from the mesh nodes
    x_coords = [node.x for node in mesh]
    y_coords = [node.y for node in mesh]

    # Create the plot
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, s=10, c="blue", marker="o")
    plt.title("Mesh Points of Right-Angle Curved Cross-Section" + f", amount of nodes: {len(mesh)}")
    plt.xlabel("X Coordinate (mm)")
    plt.ylabel("Y Coordinate (mm)")
    plt.grid(True)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()
