"""Annular sector cross-section shape."""

import math
from dataclasses import dataclass

import numpy as np
from shapely.affinity import rotate
from shapely.geometry import Point, Polygon

from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class AnnularSectorCrossSection:
    """
    Class to represent an annular sector cross-section using shapely for geometric calculations.
    Warning: The moment of inertia and elastic section modulus are approximations. Please use with caution.

    Parameters
    ----------
    name : str
        The name of the rectangular cross-section.
    radius_centerline : MM
        The radius of the centerline of the annular sector cross-section [mm].
    thickness : MM
        The thickness of the annular sector cross-section [mm].
    start_angle : float
        The start angle of the annular sector in degrees (top = 0 degrees, clockwise is positive).
    end_angle : float
        The end angle of the annular sector in degrees (must be larger than start angle but not more than 360 degrees more).
    x : MM
        The x-coordinate of the annular sector's center.
    y : MM
        The y-coordinate of the annular sector's center.
    """

    name: str
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
        """Calculate the inner radius of the annular sector [mm]."""
        return self.radius_centerline - self.thickness / 2.0

    @property
    def outer_radius(self) -> MM:
        """Calculate the outer radius of the annular sector [mm]."""
        return self.radius_centerline + self.thickness / 2.0

    @property
    def height(self) -> MM:
        """
        Calculate the height of the annular sector cross-section [mm].

        Returns
        -------
        MM
            The height of the annular sector.
        """
        min_y = min(point.y for point in self.vertices)
        max_y = max(point.y for point in self.vertices)
        return max_y - min_y

    @property
    def width(self) -> MM:
        """
        Calculate the width of the annular sector cross-section [mm].

        Returns
        -------
        MM
            The width of the annular sector.
        """
        min_x = min(point.x for point in self.vertices)
        max_x = max(point.x for point in self.vertices)
        return max_x - min_x

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the annular sector cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the annular sector.
        """
        center = Point(self.x, self.y)
        inner_circle = center.buffer(self.inner_radius, resolution=64)
        outer_circle = center.buffer(self.outer_radius, resolution=64)

        inner_ring = rotate(inner_circle, -self.start_angle, origin=center)
        outer_ring = rotate(outer_circle, -self.start_angle, origin=center)

        # Create the annular sector by intersecting with a sector
        sector_points = [center]
        angle_step = (self.end_angle - self.start_angle) / 8
        for i in range(9):
            angle = math.radians(90 - self.start_angle - i * angle_step)
            sector_points.append(Point(center.x + 2 * self.outer_radius * math.cos(angle), center.y + 2 * self.outer_radius * math.sin(angle)))
        sector_points.append(center)
        sector = Polygon(sector_points).buffer(0)

        return outer_ring.difference(inner_ring).intersection(sector)

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the annular sector cross-section [mm²].

        Returns
        -------
        MM2
            The area of the annular sector.
        """
        angle_radians = math.radians(self.end_angle - self.start_angle)
        return 0.5 * angle_radians * (self.outer_radius**2 - self.inner_radius**2)

    @property
    def plate_thickness(self) -> MM:
        """
        Get the plate thickness of the annular sector cross-section.

        Returns
        -------
        MM
            The plate thickness of the annular sector.
        """
        return self.thickness

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the annular sector cross-section [mm].

        Returns
        -------
        MM
            The perimeter of the annular sector.
        """
        angle_radians = math.radians(self.end_angle - self.start_angle)
        return angle_radians * (self.outer_radius + self.inner_radius) + 2 * self.thickness

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the annular sector cross-section.

        Returns
        -------
        Point
            The centroid of the annular sector.
        """
        angle_radians = math.radians(self.end_angle - self.start_angle)
        centroid_radius = (
            (2 * np.sin(angle_radians) / 3 / angle_radians)
            * (self.outer_radius**3 - self.inner_radius**3)
            / (self.outer_radius**2 - self.inner_radius**2)
        )
        centroid_angle = math.radians((self.start_angle + self.end_angle) / 2)
        centroid_x = self.x + centroid_radius * math.cos(math.radians(90) - centroid_angle)
        centroid_y = self.y + centroid_radius * math.sin(math.radians(90) - centroid_angle)
        return Point(centroid_x, centroid_y)

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
        Vertices of the annular sector cross-section.

        Returns
        -------
        list[Point]
            The vertices of the annular sector.
        """
        return [Point(x, y) for x, y in self.geometry.exterior.coords]

    def dotted_mesh(self, max_mesh_size: MM = 0) -> list[Point]:
        """
        Mesh the annular sector cross-section with a given mesh size and return the inner nodes of
        each rectangle they represent.

        Parameters
        ----------
        max_mesh_size : MM
            The maximum mesh size to use for the meshing. Default is a third of the thickness and 10th of radius.,
            whichever is the minimum of the two.

        Returns
        -------
        list[Point]
            The inner nodes of the meshed rectangles they represent.
        """
        if self.area == 0:
            return [Point(self.x, self.y)]
        if max_mesh_size == 0:
            mesh_size = min(self.plate_thickness / 3, self.inner_radius / 10)
        else:
            mesh_size = self.thickness / np.ceil(self.thickness / max_mesh_size)

        x_min, y_min, x_max, y_max = self.geometry.bounds
        x_range = np.arange(x_min, x_max, mesh_size)
        y_range = np.arange(y_min, y_max, mesh_size)
        return [
            Point(x + mesh_size / 2, y + mesh_size / 2)
            for x in x_range
            for y in y_range
            if self.inner_radius <= math.hypot(x + mesh_size / 2 - self.x, y + mesh_size / 2 - self.y) <= self.outer_radius
            and self.start_angle <= 90 - math.degrees(math.atan2(y + mesh_size / 2 - self.y, x + mesh_size / 2 - self.x)) <= self.end_angle
        ]
