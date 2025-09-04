"""Hexagonal cross-section shape."""

import math
from dataclasses import dataclass

import numpy as np
from sectionproperties.pre import Geometry
from shapely.geometry import Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM


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
        points = np.round([(self.x + self.radius * math.cos(i * angle), self.y + self.radius * math.sin(i * angle)) for i in range(6)], self.ACCURACY)
        return Polygon(points)

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
