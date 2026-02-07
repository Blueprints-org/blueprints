"""Rectangular profile shape."""

from dataclasses import dataclass
from functools import partial

import numpy as np
from sectionproperties.pre import Geometry
from shapely import Polygon

from blueprints.structural_sections._profile import Profile
from blueprints.type_alias import MM


@dataclass(frozen=True)
class RectangularProfile(Profile):
    """
    Class to represent a rectangular profile for geometric calculations.

    Parameters
    ----------
    width : MM
        The width of the rectangular profile.
    height : MM
        The height of the rectangular profile.
    x : MM
        The x-coordinate of the centroid of the rectangle. Default is 0.
    y : MM
        The y-coordinate of the centroid of the rectangle. Default is 0.
    name : str
        The name of the rectangular profile, default is "Rectangle".
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
    def mesh_creator(self) -> partial:
        """Mesh settings for the geometrical calculations of the rectangular profile."""
        # The equation for the mesh length is the result of a fitting procedure to ensure
        # a maximum of 0.1% deviation of the calculated profile properties compared to
        # the analytical solution for various rectangular geometries.
        mesh_length = max(min(self.width, self.height) / 20, 2.0)
        return partial(Geometry.create_mesh, mesh_sizes=mesh_length**2)

    @property
    def max_profile_thickness(self) -> MM:
        """Maximum element thickness of the rectangular profile [mm]."""
        return min(self.width, self.height)

    @property
    def _polygon(self) -> Polygon:
        """
        Shapely Polygon representing the rectangular profile. Defines the coordinates of the rectangle based on width, height, x,
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
        return Polygon(np.round([left_lower, right_lower, right_upper, left_upper], self.accuracy))
