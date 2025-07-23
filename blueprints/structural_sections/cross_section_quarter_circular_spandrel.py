"""Square minus quarter circle shape: Quarter Circular Spandrel."""

import math
from dataclasses import dataclass

from sectionproperties.pre import Geometry
from shapely.geometry import Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM


@dataclass(frozen=True)
class QuarterCircularSpandrelCrossSection(CrossSection):
    """
    Class to represent a square cross-section with a quarter circle cutout for geometric calculations, named as Quarter Circular Spandrel .

    Parameters
    ----------
    radius : MM
        The length of the two sides of the cross-section.
    x : MM
        The x-coordinate of the 90-degree angle when thickness_horizontal would be zero. Default is 0.
    y : MM
        The y-coordinate of the 90-degree angle when thickness_vertical would be zero. Default is 0.
    mirrored_horizontally : bool
        Whether the shape is mirrored horizontally. Default is False.
    mirrored_vertically : bool
        Whether the shape is mirrored vertically. Default is False.
    thickness_at_horizontal : MM
        Thickness at the horizontal side of the cross-section. Default is 0.
    thickness_at_vertical : MM
        Thickness at the vertical side of the cross-section. Default is 0.
    name : str
        The name of the radius cross-section. Default is "QCS".
    """

    radius: MM
    x: MM = 0
    y: MM = 0
    mirrored_horizontally: bool = False
    mirrored_vertically: bool = False
    thickness_at_horizontal: MM = 0
    thickness_at_vertical: MM = 0
    name: str = "QCS"

    def __post_init__(self) -> None:
        """Post-initialization to validate the side length."""
        if self.radius < 0:
            msg = f"Radius must be non-negative, but got {self.radius}"
            raise ValueError(msg)
        if self.thickness_at_horizontal < 0:
            msg = f"Thickness at horizontal must be non-negative, but got {self.thickness_at_horizontal}"
            raise ValueError(msg)
        if self.thickness_at_vertical < 0:
            msg = f"Thickness at vertical must be non-negative, but got {self.thickness_at_vertical}"
            raise ValueError(msg)

    @property
    def polygon(self) -> Polygon:
        """
        Shapely Polygon representing the cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the shape.
        """
        left_lower = (-self.thickness_at_horizontal, -self.thickness_at_vertical)
        left_upper = (-self.thickness_at_horizontal, self.radius)
        right_lower = (self.radius, -self.thickness_at_vertical)

        # Approximate the quarter circle with 25 straight lines.
        # This resolution was chosen to balance performance and accuracy.
        # Increasing the number of segments (e.g., to 50) would improve accuracy but at the cost of computational performance.
        # Ensure this resolution meets the requirements of your specific application before using.
        quarter_circle_points = [
            (self.radius - self.radius * math.cos(math.pi / 2 * i / 25), self.radius - self.radius * math.sin(math.pi / 2 * i / 25))
            for i in range(26)
        ]

        # Create the polygon by combining the points
        polygon = [*quarter_circle_points]
        if self.thickness_at_horizontal > 0:
            polygon = [left_upper, *polygon]
        if self.thickness_at_vertical > 0:
            polygon = [*polygon, right_lower]
        polygon = [left_lower, *polygon]

        # mirror the points if specified
        if self.mirrored_horizontally:
            polygon = [(-x, y) for x, y in polygon]
        if self.mirrored_vertically:
            polygon = [(x, -y) for x, y in polygon]

        # translate the points to the specified x and y coordinates
        polygon = [(x + self.x, y + self.y) for x, y in polygon]

        return Polygon(polygon)

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


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    section = QuarterCircularSpandrelCrossSection(radius=100, thickness_at_vertical=10, thickness_at_horizontal=5)
    poly = section.polygon

    x, y = poly.exterior.xy
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, "b-")
    plt.fill(x, y, alpha=0.3)
    plt.axis("equal")
    plt.title("Quarter Circular Spandrel Cross Section")
    plt.show()
