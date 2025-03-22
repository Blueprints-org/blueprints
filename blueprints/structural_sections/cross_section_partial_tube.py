"""Partial ring cross-section shape."""

import math
from dataclasses import dataclass

import numpy as np
from shapely.affinity import rotate
from shapely.geometry import Point, Polygon

from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class PartialRingCrossSection:
    """
    Class to represent a partial ring cross-section using shapely for geometric calculations.
    Warning: The moment of inertia and elastic section modulus are approximations. Please use with caution.

    Parameters
    ----------
    radius_centerline : MM
        The radius of the centerline of the partial ring cross-section [mm].
    thickness : MM
        The thickness of the partial ring cross-section [mm].
    start_angle : float
        The start angle of the partial ring in degrees (top = 0 degrees, clockwise is positive).
    end_angle : float
        The end angle of the partial ring in degrees (must be larger than start angle but not more than 360 degrees more).
    x : MM
        The x-coordinate of the partial ring's center.
    y : MM
        The y-coordinate of the partial ring's center.
    """

    radius_centerline: MM
    thickness: MM
    start_angle: float
    end_angle: float
    x: MM
    y: MM

    def __post_init__(self) -> None:
        """Post-initialization to validate the inputs."""
        if self.radius_centerline <= 0:
            raise ValueError(f"Radius must be a positive value, but got {self.radius_centerline}")
        if self.thickness <= 0:
            raise ValueError(f"Thickness must be a positive value, but got {self.thickness}")
        if not (-360 < self.start_angle < 360):
            raise ValueError(f"Start angle must be between -360 and 360 degrees, but got {self.start_angle}")
        if not (self.start_angle < self.end_angle < self.start_angle + 360):
            raise ValueError(f"End angle must be larger than start angle and not more than 360 degrees more, but got {self.end_angle}")

    @property
    def inner_radius(self) -> MM:
        """Calculate the inner radius of the partial ring [mm]."""
        return self.radius_centerline - self.thickness / 2.0

    @property
    def outer_radius(self) -> MM:
        """Calculate the outer radius of the partial ring [mm]."""
        return self.radius_centerline + self.thickness / 2.0

    @property
    def height(self) -> MM:
        """
        Calculate the height of the partial ring cross-section [mm].

        Returns
        -------
        MM
            The height of the partial ring.
        """
        min_y = min(point.y for point in self.vertices)
        max_y = max(point.y for point in self.vertices)
        return max_y - min_y

    @property
    def width(self) -> MM:
        """
        Calculate the width of the partial ring cross-section [mm].

        Returns
        -------
        MM
            The width of the partial ring.
        """
        min_x = min(point.x for point in self.vertices)
        max_x = max(point.x for point in self.vertices)
        return max_x - min_x

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the partial ring cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the partial ring.
        """
        center = Point(self.x, self.y)
        inner_circle = center.buffer(self.inner_radius, resolution=64)
        outer_circle = center.buffer(self.outer_radius, resolution=64)

        inner_ring = rotate(inner_circle, self.start_angle, origin=center)
        outer_ring = rotate(outer_circle, self.start_angle, origin=center)

        partial_ring = outer_ring.difference(inner_ring)
        return rotate(partial_ring, self.end_angle - self.start_angle, origin=center)

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the partial ring cross-section [mm²].

        Returns
        -------
        MM2
            The area of the partial ring.
        """
        angle_radians = math.radians(self.end_angle - self.start_angle)
        return 0.5 * angle_radians * (self.outer_radius**2 - self.inner_radius**2)

    @property
    def plate_thickness(self) -> MM:
        """
        Get the plate thickness of the partial ring cross-section.

        Returns
        -------
        MM
            The plate thickness of the partial ring.
        """
        return self.thickness

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the partial ring cross-section [mm].

        Returns
        -------
        MM
            The perimeter of the partial ring.
        """
        angle_radians = math.radians(self.end_angle - self.start_angle)
        return angle_radians * (self.outer_radius + self.inner_radius) + 2 * self.thickness

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the partial ring cross-section.

        Returns
        -------
        Point
            The centroid of the partial ring.
        """
        angle_radians = math.radians(self.end_angle - self.start_angle)
        centroid_radius = (2 * self.radius_centerline * math.sin(angle_radians / 2)) / (3 * angle_radians)
        centroid_angle = math.radians((self.start_angle + self.end_angle) / 2)
        return Point(self.x + centroid_radius * math.cos(centroid_angle), self.y + centroid_radius * math.sin(centroid_angle))

    @property
    def moment_of_inertia_about_y(self) -> MM4:
        """
        Moments of inertia of the cross-section about the y-axis [mm⁴].
        Note: No closed form equation was found, therefore this approximation is used.

        Returns
        -------
        MM4
            The moment of inertia about the y-axis.
        """
        representative_width = self.area / self.height
        return RectangularCrossSection(width=representative_width, height=self.height, x=self.x, y=self.y).moment_of_inertia_about_y

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].
        Note: No closed form equation was found, therefore this approximation is used.

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        representative_height = self.area / self.width
        return RectangularCrossSection(width=self.width, height=representative_height, x=self.x, y=self.y).moment_of_inertia_about_z

    @property
    def polar_moment_of_inertia(self) -> MM4:
        """
        Polar moment of inertia of the cross-section [mm⁴].
        Note: No closed form equation was found, therefore this approximation is used.

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
        Note: No closed form equation was found, therefore this approximation is used.

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        distance_to_top = max(point.y for point in self.vertices) - self.centroid.y
        return self.moment_of_inertia_about_y / distance_to_top

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the negative z side [mm³].
        Note: No closed form equation was found, therefore this approximation is used.

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        distance_to_bottom = self.centroid.y - min(point.y for point in self.vertices)
        return self.moment_of_inertia_about_y / distance_to_bottom

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the positive y side [mm³].
        Note: No closed form equation was found, therefore this approximation is used.

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        distance_to_right = max(point.x for point in self.vertices) - self.centroid.x
        return self.moment_of_inertia_about_z / distance_to_right

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the negative y side [mm³].
        Note: No closed form equation was found, therefore this approximation is used.

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        distance_to_left = self.centroid.x - min(point.x for point in self.vertices)
        return self.moment_of_inertia_about_z / distance_to_left

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """
        Plastic section modulus about the y-axis [mm³].
        Note: No closed form equation was found, therefore this approximation is used.

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return max(self.elastic_section_modulus_about_y_positive, self.elastic_section_modulus_about_y_negative)

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].
        Note: No closed form equation was found, therefore this approximation is used.

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return max(self.elastic_section_modulus_about_z_positive, self.elastic_section_modulus_about_z_negative)

    @property
    def vertices(self) -> list[Point]:
        """
        Vertices of the partial ring cross-section.

        Returns
        -------
        list[Point]
            The vertices of the partial ring.
        """
        return [Point(x, y) for x, y in self.geometry.exterior.coords]

    def dotted_mesh(self, mesh_size: MM = 0) -> list[Point]:
        """
        Mesh the partial ring cross-section with a given mesh size and return the inner nodes of
        each rectangle  they represent.

        Parameters
        ----------
        mesh_size : MM
            The mesh size to use for the meshing. Default is a third of the thickness.

        Returns
        -------
        list[Point]
            The inner nodes of the meshed rectangles they represent.
        """
        if mesh_size == 0:
            mesh_size = self.thickness / 3

        x_min, y_min, x_max, y_max = self.geometry.bounds
        x_range = np.arange(x_min, x_max, mesh_size)
        y_range = np.arange(y_min, y_max, mesh_size)
        return [
            Point(x + mesh_size / 2, y + mesh_size / 2)
            for x in x_range
            for y in y_range
            if self.geometry.contains(Point(x + mesh_size / 2, y + mesh_size / 2))
        ]


if __name__ == "__main__":
    # Example usage of PartialRingCrossSection to get the mesh
    partial_ring = PartialRingCrossSection(radius_centerline=100, thickness=10, start_angle=0, end_angle=180, x=0, y=0)
    mesh = partial_ring.dotted_mesh()

    import matplotlib.pyplot as plt

    # Extract x and y coordinates from the mesh nodes
    x_coords = [node.x for node in mesh]
    y_coords = [node.y for node in mesh]

    # Create the plot
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, s=10, c="blue", marker="o")
    plt.title("Mesh Points of Partial Ring Cross-Section")
    plt.xlabel("X Coordinate (mm)")
    plt.ylabel("Y Coordinate (mm)")
    plt.grid(True)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()
