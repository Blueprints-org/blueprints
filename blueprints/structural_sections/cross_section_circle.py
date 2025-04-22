"""Circular cross-section shape."""

import math
from dataclasses import dataclass

from sectionproperties.pre import Geometry
from shapely import Point, Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class CircularCrossSection(CrossSection):
    """
    Class to represent a circular cross-section using shapely for geometric calculations.

    Parameters
    ----------
    diameter : MM
        The diameter of the circular cross-section [mm].
    x : MM
        The x-coordinate of the circle's center.
    y : MM
        The y-coordinate of the circle's center.
    name : str
        The name of the rectangular cross-section, default is "Circle".
    """

    diameter: MM
    x: MM
    y: MM
    name: str = "Circle"

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
    def polygon(self) -> Polygon:
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

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the circular cross-section.

        Properties
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        """
        if mesh_size is None:
            minimum_mesh_size = 2.0
            mesh_length = max(self.diameter / 20, minimum_mesh_size)
            mesh_size = mesh_length**2

        circular = Geometry(geom=self.polygon)
        circular.create_mesh(mesh_sizes=mesh_size)
        return circular
