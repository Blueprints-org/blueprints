"""Rectangular cross-section shape."""

from dataclasses import dataclass

import numpy as np
from sectionproperties.pre import Geometry
from shapely import Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM


@dataclass(frozen=True)
class RectangularCrossSection(CrossSection):
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
    name : str
        The name of the rectangular cross-section, default is "Rectangle".
    mesh_size : MM | None
        The maximum mesh size for the geometry. Default is 2.5 mm.
    """

    width: MM
    height: MM
    x: MM = 0
    y: MM = 0
    name: str = "Rectangle"

    def __post_init__(self) -> None:
        """Post-initialization to validate the width and height."""
        if self.width <= 0:
            raise ValueError(f"Width must be a positive value, but got {self.width}")
        if self.height <= 0:
            raise ValueError(f"Height must be a positive value, but got {self.height}")

    @property
    def polygon(self) -> Polygon:
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
        return Polygon(np.round([left_lower, right_lower, right_upper, left_upper], self.ACCURACY))

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the rectangular cross-section.

        Properties
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        """
        if mesh_size is None:
            minimum_mesh_size = 2.0
            mesh_length = max(min(self.width, self.height) / 20, minimum_mesh_size)
            mesh_size = mesh_length**2

        rectangular = Geometry(geom=self.polygon)
        rectangular.create_mesh(mesh_sizes=mesh_size)
        return rectangular
