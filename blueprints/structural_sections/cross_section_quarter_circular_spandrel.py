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
