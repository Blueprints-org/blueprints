"""Annular sector cross-section shape."""

import math
from dataclasses import dataclass

import numpy as np
from sectionproperties.pre import Geometry
from shapely.affinity import rotate
from shapely.geometry import Point, Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import DEG, MM, MM2, MM3, MM4


@dataclass(frozen=True)
class AnnularSectorCrossSection(CrossSection):
    """
    Class to represent an annular sector cross-section using shapely for geometric calculations.

    Parameters
    ----------
    inner_radius : MM
        The radius of the inner circle of the annular sector [mm].
    thickness : MM
        The thickness of the annular sector cross-section [mm].
    start_angle : DEG
        The start angle of the annular sector in degrees (top = 0 degrees, clockwise is positive).
    end_angle : DEG
        The end angle of the annular sector in degrees (must be larger than start angle but not more than 360 degrees more).
    x : MM
        The x-coordinate of the annular sector's radius center.
    y : MM
        The y-coordinate of the annular sector's radius center.
    name : str
        The name of the rectangular cross-section, default is "Annular Sector".
    """

    inner_radius: MM
    thickness: MM
    start_angle: DEG
    end_angle: DEG
    x: MM
    y: MM
    name: str = "Annular Sector"

    def __post_init__(self) -> None:
        """Post-initialization to validate the inputs."""
        if self.inner_radius < 0:
            raise ValueError(f"Radius must be zero or positive, but got {self.inner_radius}")
        if self.thickness <= 0:
            raise ValueError(f"Thickness must be a positive value, but got {self.thickness}")
        if self.start_angle > 360 or self.start_angle < -360:
            raise ValueError(f"Start angle must be between -360 and 360 degrees, but got {self.start_angle}")
        if self.end_angle <= self.start_angle:
            raise ValueError(f"End angle must be greater than start angle, but got end angle {self.end_angle} and start angle {self.start_angle}")
        if self.end_angle - self.start_angle >= 360:
            raise ValueError(
                f"The total angle made between start and end angle must be less than 360 degrees, but got "
                f"{self.end_angle - self.start_angle} degrees (end {self.end_angle} - start {self.start_angle})\n\n"
                f"In case you want to create a full circle (donut shape), "
                "use a tube cross section instead (TubeCrossSection)."
            )

    @property
    def radius_centerline(self) -> MM:
        """Calculate the inner radius of the annular sector [mm]."""
        return self.inner_radius + self.thickness / 2.0

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
        min_y = min(y for _, y in self.polygon.exterior.coords)
        max_y = max(y for _, y in self.polygon.exterior.coords)
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
        min_x = min(x for x, _ in self.polygon.exterior.coords)
        max_x = max(x for x, _ in self.polygon.exterior.coords)
        return max_x - min_x

    @property
    def polygon(self) -> Polygon:
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

        result = outer_ring.difference(inner_ring).intersection(sector)
        return Polygon(result)  # type: ignore[arg-type]

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the annular sector cross-section [mm²].

        Returns
        -------
        MM2
            The area of the annular sector.
        """
        area_outer_circle = math.pi * self.outer_radius**2
        area_inner_circle = math.pi * self.inner_radius**2
        area_ring = area_outer_circle - area_inner_circle
        return area_ring / 360 * (self.end_angle - self.start_angle)

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
        halve_angle_radians = math.radians(self.end_angle - self.start_angle) / 2
        centroid_radius = (
            (2 * np.sin(halve_angle_radians) / 3 / halve_angle_radians)
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

        Returns
        -------
        MM4
            The moment of inertia about the y-axis.
        """
        # based on https://engineering.stackexchange.com/a/60564
        # with y horizontal and z vertical
        theta = math.radians(self.end_angle - self.start_angle)
        term0 = self.outer_radius**4 - self.inner_radius**4
        term1 = (theta + math.sin(theta)) / 8
        term2 = (8 * math.sin(theta / 2) ** 2) / (9 * theta)
        term3 = (8 * math.sin(theta / 2) ** 2) / (9 * theta * (self.outer_radius + self.inner_radius) ** 2)
        term4 = self.inner_radius**4 * self.outer_radius**2 - self.outer_radius**4 * self.inner_radius**2

        i_z_annulus = term0 * (term1 - term2) + term3 * term4
        i_y_annulus = term0 * (theta - math.sin(theta)) / 8

        beta = np.pi / 2 - math.radians(self.end_angle + self.start_angle) / 2
        return (i_y_annulus + i_z_annulus) / 2 + (i_y_annulus - i_z_annulus) / 2 * math.cos(2 * beta)

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        # based on https://engineering.stackexchange.com/a/60564
        # with y horizontal and z vertical
        theta = math.radians(self.end_angle - self.start_angle)
        term0 = self.outer_radius**4 - self.inner_radius**4
        term1 = (theta + math.sin(theta)) / 8
        term2 = (8 * math.sin(theta / 2) ** 2) / (9 * theta)
        term3 = (8 * math.sin(theta / 2) ** 2) / (9 * theta * (self.outer_radius + self.inner_radius) ** 2)
        term4 = self.inner_radius**4 * self.outer_radius**2 - self.outer_radius**4 * self.inner_radius**2

        i_z_annulus = term0 * (term1 - term2) + term3 * term4
        i_y_annulus = term0 * (theta - math.sin(theta)) / 8

        beta = np.pi / 2 - math.radians(self.end_angle + self.start_angle) / 2
        return (i_y_annulus + i_z_annulus) / 2 - (i_y_annulus - i_z_annulus) / 2 * math.cos(2 * beta)

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
        distance_to_top = max(y for _, y in self.polygon.exterior.coords) - self.centroid.y
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
        distance_to_bottom = self.centroid.y - min(y for _, y in self.polygon.exterior.coords)
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
        distance_to_right = max(x for x, _ in self.polygon.exterior.coords) - self.centroid.x
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
        distance_to_left = self.centroid.x - min(x for x, _ in self.polygon.exterior.coords)
        return self.moment_of_inertia_about_z / distance_to_left

    @property
    def plastic_section_modulus_about_y(self) -> MM3 | None:
        """
        Plastic section modulus about the y-axis [mm³].
        Note: No closed form equation was found, therefore this approximation is used.

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return None

    @property
    def plastic_section_modulus_about_z(self) -> MM3 | None:
        """
        Plastic section modulus about the z-axis [mm³].
        Note: No closed form equation was found, therefore this conservative approximation is used.

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return None

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the annular sector cross-section.

        Parameters
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        Returns
        -------
        Geometry
            The Geometry object representing the annular sector.
        """
        if mesh_size is None:
            minimum_mesh_size = 1.0
            mesh_length = max(self.thickness / 5, minimum_mesh_size)
            mesh_size = mesh_length**2

        annular_sector = Geometry(geom=self.polygon)
        annular_sector.create_mesh(mesh_sizes=mesh_size)
        return annular_sector
