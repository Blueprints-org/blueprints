"""Hexagonal cross-section shape."""

import math
from dataclasses import dataclass

from sectionproperties.pre import Geometry
from shapely.geometry import Point, Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class HexagonalCrossSection(CrossSection):
    """
    Class to represent a hexagonal cross-section flat on ground, using shapely for geometric calculations.

    Parameters
    ----------
    side_length : MM
        The side length of the hexagonal cross-section [mm].
    x : MM
        The x-coordinate of the hexagon's center. Default is 0.
    y : MM
        The y-coordinate of the hexagon's center. Default is 0.
    name : str
        The name of the rectangular cross-section, default is "Hexagon".
    """

    side_length: MM
    x: MM = 0
    y: MM = 0
    name: str = "Hexagon"

    def __post_init__(self) -> None:
        """Post-initialization to validate the side length."""
        if self.side_length <= 0:
            msg = f"Side length must be a positive value, but got {self.side_length}"
            raise ValueError(msg)

    @property
    def radius(self) -> MM:
        """
        Calculate the radius of the circumscribed circle of the hexagon (farthest point from the center) [mm].

        Returns
        -------
        MM
            The radius of the circumscribed circle.
        """
        return self.side_length

    @property
    def apothem(self) -> MM:
        """
        Calculate the apothem of the hexagon (distance from center to midpoint of a side) [mm].

        Returns
        -------
        MM
            The apothem of the hexagon.
        """
        return self.side_length * math.sqrt(3) / 2

    @property
    def polygon(self) -> Polygon:
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
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the positive z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / self.apothem

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the negative z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / self.apothem

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the positive y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / self.side_length

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the negative y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / self.side_length

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """
        Plastic section modulus about the y-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return self.side_length * math.sqrt(3) * 2 / 9 * self.area

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        area_center_rectangle = (self.side_length / 2) * (self.side_length * math.sqrt(3))
        distance_center_rectangle = self.side_length / 4

        area_outer_triangle = 1 / 2 * (self.side_length * math.sqrt(3)) * (self.side_length / 2)
        distance_outer_triangle = self.side_length / 2 + self.side_length / 6

        return 2 * (area_center_rectangle * distance_center_rectangle + area_outer_triangle * distance_outer_triangle)

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the hexagon cross-section.

        Properties
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        """
        if mesh_size is None:
            minimum_mesh_size = 2.0
            mesh_length = max(self.side_length / 10, minimum_mesh_size)
            mesh_size = mesh_length**2

        hexagon = Geometry(geom=self.polygon)
        hexagon.create_mesh(mesh_sizes=mesh_size)
        return hexagon
