"""Triangular cross-section shape."""

from dataclasses import dataclass

from sectionproperties.pre import Geometry
from shapely import Point, Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class RightAngledTriangularCrossSection(CrossSection):
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
    mirrored_horizontally : bool
        Whether the triangle is mirrored horizontally. Default is False.
    mirrored_vertically : bool
        Whether the triangle is mirrored vertically. Default is False.
    name : str
        The name of the rectangular cross-section, default is "Triangle".
    """

    base: MM
    height: MM
    x: MM = 0
    y: MM = 0
    mirrored_horizontally: bool = False
    mirrored_vertically: bool = False
    name: str = "Triangle"

    def __post_init__(self) -> None:
        """Post-initialization to validate the width and height."""
        if self.base < 0:
            raise ValueError(f"Base must be a positive value, but got {self.base}")
        if self.height < 0:
            raise ValueError(f"Height must be a positive value, but got {self.height}")

    @property
    def polygon(self) -> Polygon:
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

        if self.mirrored_horizontally:
            right_lower = (2 * left_lower[0] - right_lower[0], right_lower[1])
        if self.mirrored_vertically:
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
        return self.polygon.area

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the triangular cross-section.

        Returns
        -------
        MM
            The perimeter of the triangle.
        """
        return self.polygon.exterior.length

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the triangular cross-section.

        Returns
        -------
        Point
            The centroid of the triangle.
        """
        return self.polygon.centroid

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
        return self.base * self.height**2 / 10.2425

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return self.height * self.base**2 / 10.2425

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the triangular cross-section.

        Parameters
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        Returns
        -------
        Geometry
            The Geometry object representing the triangular cross-section.
        """
        if mesh_size is None:
            minimum_mesh_size = 2.0
            mesh_length = max(min(self.base, self.height) / 20, minimum_mesh_size)
            mesh_size = mesh_length**2

        triangular = Geometry(geom=self.polygon)
        triangular.create_mesh(mesh_sizes=mesh_size)
        return triangular
