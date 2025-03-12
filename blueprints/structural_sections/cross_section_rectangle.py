"""Rectangular cross-section shape."""

from dataclasses import dataclass

from shapely import Point, Polygon

from blueprints.type_alias import MM, MM2, MM3, MM4


@dataclass(frozen=True)
class RectangularCrossSection:
    """
    Class to represent a rectangular cross-section for geometric calculations.

    Parameters
    ----------
    width : MM
        The width of the rectangular cross-section.
    height : MM
        The height of the rectangular cross-section.
    x : MM
        The x-coordinate of the centroid of the rectangle. Default is 0.
    y : MM
        The y-coordinate of the centroid of the rectangle. Default is 0.
    """

    width: MM
    height: MM
    x: MM = 0
    y: MM = 0

    @property
    def geometry(self) -> Polygon:
        """
        Shapely Polygon representing the rectangular cross-section. Defines the coordinates of the rectangle based on width, height, x,
        and y. Counter-clockwise order.

        Returns
        -------
        Polygon
            The shapely Polygon representing the rectangle.
        """
        left_lower = (self.x - self.width / 2, self.y - self.height / 2)
        right_lower = (self.x + self.width / 2, self.y - self.height / 2)
        right_upper = (self.x + self.width / 2, self.y + self.height / 2)
        left_upper = (self.x - self.width / 2, self.y + self.height / 2)
        return Polygon(
            [
                left_lower,
                right_lower,
                right_upper,
                left_upper,
            ]
        )

    @property
    def area(self) -> MM2:
        """
        Calculate the area of the rectangular cross-section.

        Returns
        -------
        MM2
            The area of the rectangle.
        """
        return self.geometry.area

    @property
    def perimeter(self) -> MM:
        """
        Calculate the perimeter of the rectangular cross-section.

        Returns
        -------
        MM
            The perimeter of the rectangle.
        """
        return self.geometry.length

    @property
    def centroid(self) -> Point:
        """
        Get the centroid of the rectangular cross-section.

        Returns
        -------
        Point
            The centroid of the rectangle.
        """
        return self.geometry.centroid

    @property
    def moment_of_inertia_about_y(self) -> MM4:
        """
        Moments of inertia of the cross-section about the y-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the y-axis.
        """
        return (self.width * self.height**3) / 12

    @property
    def moment_of_inertia_about_z(self) -> MM4:
        """
        Moments of inertia of the cross-section about the z-axis [mm⁴].

        Returns
        -------
        MM4
            The moment of inertia about the z-axis.
        """
        return (self.height * self.width**3) / 12

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
        return self.moment_of_inertia_about_y / (self.height / 2)

    @property
    def elastic_section_modulus_about_y_negative(self) -> MM3:
        """
        Elastic section modulus about the y-axis on the negative z side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the y-axis.
        """
        return self.moment_of_inertia_about_y / (self.height / 2)

    @property
    def elastic_section_modulus_about_z_positive(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the positive y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / (self.width / 2)

    @property
    def elastic_section_modulus_about_z_negative(self) -> MM3:
        """
        Elastic section modulus about the z-axis on the negative y side [mm³].

        Returns
        -------
        MM3
            The elastic section modulus about the z-axis.
        """
        return self.moment_of_inertia_about_z / (self.width / 2)

    @property
    def plastic_section_modulus_about_y(self) -> MM3:
        """
        Plastic section modulus about the y-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the y-axis.
        """
        return (self.width * self.height**2) / 4

    @property
    def plastic_section_modulus_about_z(self) -> MM3:
        """
        Plastic section modulus about the z-axis [mm³].

        Returns
        -------
        MM3
            The plastic section modulus about the z-axis.
        """
        return (self.height * self.width**2) / 4

    @property
    def vertices(self) -> list[Point]:
        """
        Vertices of the rectangular cross-section. Counter-clockwise order starting from the bottom-left corner.

        Returns
        -------
        list[Point]
            The vertices of the rectangle.
        """
        return [Point(x, y) for x, y in self.geometry.exterior.coords]
