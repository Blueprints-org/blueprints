"""Square minus quarter circle shape: Quarter Circular Spandrel."""

import math
from dataclasses import dataclass

import numpy as np
from sectionproperties.pre import Geometry
from shapely.geometry import Point, Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class QuarterCircularSpandrelCrossSection(CrossSection):
    """
    Class to represent a square cross-section with a quarter circle cutout for geometric calculations, named as Quarter Circular Spandrel .

    Parameters
    ----------
    radius : MM
        The length of the two sides of the cross-section.
    x : MM
        The x-coordinate of the 90-degree angle. Default is 0.
    y : MM
        The y-coordinate of the 90-degree angle. Default is 0.
    mirrored_horizontally : bool
        Whether the shape is mirrored horizontally. Default is False.
    mirrored_vertically : bool
        Whether the shape is mirrored vertically. Default is False.
    name : str
        The name of the radius cross-section. Default is "QCS".
    """

    radius: MM
    x: MM = 0
    y: MM = 0
    mirrored_horizontally: bool = False
    mirrored_vertically: bool = False
    name: str = "QCS"

    @property
    def polygon(self) -> Polygon:
        """
        Shapely Polygon representing the cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the shape.
        """
        left_lower = (self.x, self.y)

        # Approximate the quarter circle with 25 straight lines.
        # This resolution was chosen to balance performance and accuracy.
        # Increasing the number of segments (e.g., to 50) would improve accuracy but at the cost of computational performance.
        # Ensure this resolution meets the requirements of your specific application before using.
        quarter_circle_points = [
            (self.x + self.radius - self.radius * math.cos(math.pi / 2 * i / 25), self.y + self.radius - self.radius * math.sin(math.pi / 2 * i / 25))
            for i in range(26)
        ]
        for i in range(26):
            if self.mirrored_horizontally:
                quarter_circle_points[i] = (2 * left_lower[0] - quarter_circle_points[i][0], quarter_circle_points[i][1])
            if self.mirrored_vertically:
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
        Get the centroid of the cross-section, taking into account the mirrored status.

        Returns
        -------
        Point
            The centroid of the shape.
        """
        if self.radius == 0:
            return Point(self.x, self.y)

        centroid_x = (10 - 3 * np.pi) / (12 - 3 * np.pi) * self.radius + self.x
        centroid_y = (10 - 3 * np.pi) / (12 - 3 * np.pi) * self.radius + self.y

        if self.mirrored_horizontally:
            centroid_x = 2 * self.x - centroid_x
        if self.mirrored_vertically:
            centroid_y = 2 * self.y - centroid_y

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
        return (9 * np.pi**2 - 84 * np.pi + 176) / (144 * (4 - np.pi)) * self.radius**4

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return (9 * np.pi**2 - 84 * np.pi + 176) / (144 * (4 - np.pi)) * self.radius**4

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the positive z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        distance_to_end = max(y for _, y in self.polygon.exterior.coords) - self.centroid.y
        return self.moment_of_inertia_about_y / distance_to_end if self.area != 0 else 0

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the negative z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        distance_to_end = self.centroid.y - min(y for _, y in self.polygon.exterior.coords)
        return self.moment_of_inertia_about_y / distance_to_end if self.area != 0 else 0

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the positive y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        distance_to_end = max(x for x, _ in self.polygon.exterior.coords) - self.centroid.x
        return self.moment_of_inertia_about_z / distance_to_end if self.area != 0 else 0

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the negative y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        distance_to_end = self.centroid.x - min(x for x, _ in self.polygon.exterior.coords)
        return self.moment_of_inertia_about_z / distance_to_end if self.area != 0 else 0

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """
        Plastic section modulus about the y-axis [mm³].
        Note: This is an approximation based on a very small mesh.

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return self.radius**3 / 31.6851045070407

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].
        Note: This is an approximation based on a very small mesh.

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return self.radius**3 / 31.6851045070407

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the square-with-cutout cross-section.

        Properties
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        """
        if mesh_size is None:
            minimum_mesh_size = 1.0
            mesh_length = max(self.radius / 5, minimum_mesh_size)
            mesh_size = mesh_length**2

        square_with_cutout = Geometry(geom=self.polygon)
        square_with_cutout.create_mesh(mesh_sizes=mesh_size)
        return square_with_cutout
