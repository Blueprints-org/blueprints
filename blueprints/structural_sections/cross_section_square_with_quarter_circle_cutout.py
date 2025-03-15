"""Square cross-section with a quarter circle cutout shape."""

import math
from dataclasses import dataclass

from shapely.geometry import Point, Polygon

from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class SquareWithQuarterCircleCutoutCrossSection:
    """
    Class to represent a square cross-section with a quarter circle cutout for geometric calculations.
    Warning: The moment of inertia and elastic section modulus are approximations. Please use with caution.

    Parameters
    ----------
    a : MM
        The side length of the square cross-section.
    x : MM
        The x-coordinate of the 90 degree corner of the shape.
    y : MM
        The y-coordinate of the 90 degree corner of the shape.
    """

    a: MM
    x: MM = 0
    y: MM = 0

    def __post_init__(self) -> None:
        """Post-initialization to validate the diameter."""
        if self.a <= 0:
            msg = f"a must be a positive value, but got {self.a}"
            raise ValueError(msg)

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
        Shapely Polygon representing the square cross-section with a quarter circle cutout.

        Returns
        -------
        Polygon
            The shapely Polygon representing the shape.
        """
        square = Polygon([(0, 0), (self.a, 0), (self.a, self.a), (0, self.a)])
        quarter_circle = Point(0, 0).buffer(self.a).intersection(Polygon([(0, 0), (self.a, 0), (0, self.a)]))
        return square.difference(quarter_circle)

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the square cross-section with a quarter circle cutout.

        Returns
        -------
        MM2
            The area of the shape.
        """
        square_area = self.a**2
        quarter_circle_area = (math.pi * self.a**2) / 4
        return square_area - quarter_circle_area

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the square cross-section with a quarter circle cutout.

        Returns
        -------
        MM
            The perimeter of the shape.
        """
        square_perimeter = 4 * self.a
        quarter_circle_perimeter = (math.pi * self.a) / 2
        return square_perimeter - 2 * self.a + quarter_circle_perimeter

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the square cross-section with a quarter circle cutout.

        Returns
        -------
        Point
            The centroid of the shape.
        """
        # Approximate centroid calculation
        square_centroid = Point(self.a / 2, self.a / 2)
        quarter_circle_centroid = Point(4 * self.a / (3 * math.pi), 4 * self.a / (3 * math.pi))
        area_square = self.a**2
        area_quarter_circle = (math.pi * self.a**2) / 4
        cx = (square_centroid.x * area_square - quarter_circle_centroid.x * area_quarter_circle) / (area_square - area_quarter_circle)
        cy = (square_centroid.y * area_square - quarter_circle_centroid.y * area_quarter_circle) / (area_square - area_quarter_circle)
        return Point(cx, cy)

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
        Vertices of the square cross-section with a quarter circle cutout. Counter-clockwise order starting from the bottom-left corner.

        Returns
        -------
        list[Point]
            The vertices of the shape.
        """
        return [Point(0, 0), Point(self.a, 0), Point(self.a, self.a), Point(0, self.a)]
