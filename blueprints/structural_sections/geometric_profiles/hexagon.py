"""Hexagonal profile shape."""

import math
from dataclasses import dataclass
from functools import partial

import numpy as np
from sectionproperties.pre import Geometry
from shapely.geometry import Polygon

from blueprints.structural_sections._profile import Profile
from blueprints.type_alias import MM


@dataclass(frozen=True)
class HexagonalProfile(Profile):
    """
    Class to represent a hexagonal profile flat on ground, using shapely for geometric calculations.

    Parameters
    ----------
    side_length : MM
        The side length of the hexagonal profile [mm].
    x : MM
        The x-coordinate of the hexagon's center. Default is 0.
    y : MM
        The y-coordinate of the hexagon's center. Default is 0.
    name : str
        The name of the hexagon profile, default is "Hexagon".
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
    def max_thickness(self) -> MM:
        """Maximum element thickness of the hexagonal profile [mm]."""
        return self.side_length * np.sqrt(3)

    @property
    def mesh_creator(self) -> partial:
        """Mesh settings for the geometrical calculations of the hexagonal profile."""
        # The equation for the mesh length is the result of a fitting procedure to ensure
        # a maximum of 0.1% deviation of the calculated profile properties compared to
        # the analytical solution for various hexagonal geometries.
        mesh_length = max(self.side_length / 10, 2.0)
        return partial(Geometry.create_mesh, mesh_sizes=mesh_length**2)

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
    def _polygon(self) -> Polygon:
        """
        Shapely Polygon representing the hexagonal profile.

        Returns
        -------
        Polygon
            The shapely Polygon representing the hexagon.
        """
        angle = math.pi / 3
        points = np.round([(self.x + self.radius * math.cos(i * angle), self.y + self.radius * math.sin(i * angle)) for i in range(6)], self.accuracy)
        return Polygon(points)
