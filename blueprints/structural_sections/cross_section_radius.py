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
    name : str
        The name of the radius cross-section. Default is "Right Angle Curved".
    """

    radius: MM
    x: MM = 0
    y: MM = 0
    flipped_horizontally: bool = False
    flipped_vertically: bool = False
    name: str = "Right Angle Curved"

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

        # Approximate the quarter circle with 50 straight lines
        quarter_circle_points = [
            (self.x + self.radius - self.radius * math.cos(math.pi / 2 * i / 50), self.y + self.radius - self.radius * math.sin(math.pi / 2 * i / 50))
            for i in range(51)
        ]
        for i in range(51):
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
        Get the centroid of the cross-section, taking into account the flipped status.

        Returns
        -------
        Point
            The centroid of the shape.
        """
        if self.radius == 0:
            return Point(self.x, self.y)

        area_square = self.radius**2
        cog_square_to_reference_point = self.radius / 2

        area_quarter_circle = math.pi * self.radius**2 / 4
        cog_quarter_circle_to_reference_point = self.radius - 4 * self.radius / 3 / np.pi

        first_moment_square = area_square * cog_square_to_reference_point
        first_moment_quarter_circle = area_quarter_circle * cog_quarter_circle_to_reference_point

        total_first_moment = first_moment_square - first_moment_quarter_circle
        total_area = area_square - area_quarter_circle

        centroid_x = self.x + total_first_moment / total_area
        centroid_y = self.y + total_first_moment / total_area

        if self.flipped_horizontally:
            centroid_x = 2 * self.x - centroid_x
        if self.flipped_vertically:
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
        inertia_square = self.radius**4 / 12
        area_square = self.radius**2
        cog_square_to_reference_point = self.radius / 2

        inertia_quarter_circle = math.pi * self.radius**4 / 64
        area_quarter_circle = math.pi * self.radius**2 / 4
        cog_quarter_circle_to_reference_point = self.radius - 4 * self.radius / 3 / np.pi

        inertia_reference_point_square = inertia_square + area_square * cog_square_to_reference_point**2
        inertia_about_reference_point_quarter_circle = inertia_quarter_circle + area_quarter_circle * cog_quarter_circle_to_reference_point**2
        inertia_reference_point = inertia_reference_point_square - inertia_about_reference_point_quarter_circle

        return inertia_reference_point - (area_square - area_quarter_circle) * (self.centroid.y - self.y) ** 2

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return self.moment_of_inertia_about_y

    @property
    def elastic_section_modulus_about_y_positive(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the positive z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        distance_to_end = max(point.y for point in self.geometry.exterior.coords) - self.centroid.y
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
        distance_to_end = self.centroid.y - min(point.y for point in self.geometry.exterior.coords)
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
        distance_to_end = max(point.x for point in self.geometry.exterior.coords) - self.centroid.x
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
        distance_to_end = self.centroid.x - min(point.x for point in self.geometry.exterior.coords)
        return self.moment_of_inertia_about_z / distance_to_end if self.area != 0 else 0

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """
        Plastic section modulus about the y-axis [mm³].
        Note: This is an approximation.

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return self.radius**3 / 30.73

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].
        Note: This is an approximation.

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return self.plastic_section_modulus_about_y
