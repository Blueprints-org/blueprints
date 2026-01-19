"""Triangular profile shape."""

from dataclasses import dataclass
from functools import partial

import numpy as np
from sectionproperties.pre import Geometry
from shapely import Polygon

from blueprints.structural_sections._profile import Profile
from blueprints.type_alias import MM


@dataclass(frozen=True)
class RightAngledTriangularProfile(Profile):
    """
    Class to represent a right-angled triangular with a right angle at the bottom left corner profile for geometric calculations.

    Parameters
    ----------
    base : MM
        The base length of the triangular profile.
    height : MM
        The height of the triangular profile.
    x : MM
        The x-coordinate of the 90-degree angle. Default is 0.
    y : MM
        The y-coordinate of the 90-degree angle. Default is 0.
    mirrored_horizontally : bool
        Whether the triangle is mirrored horizontally. Default is False.
    mirrored_vertically : bool
        Whether the triangle is mirrored vertically. Default is False.
    name : str
        The name of the triangle profile, default is "Triangle".
    """

    base: MM
    height: MM
    x: MM = 0
    y: MM = 0
    mirrored_horizontally: bool = False
    mirrored_vertically: bool = False
    name: str = "Triangle"

    def __post_init__(self) -> None:
        """Post-initialization to validate the width and height."""
        if self.base < 0:
            raise ValueError(f"Base must be a positive value, but got {self.base}")
        if self.height < 0:
            raise ValueError(f"Height must be a positive value, but got {self.height}")

    @property
    def max_profile_thickness(self) -> MM:
        """Maximum element thickness of the triangular profile [mm]."""
        return min(self.base, self.height)

    @property
    def mesh_creator(self) -> partial:
        """Mesh settings for the geometrical calculations of the triangular profile."""
        # The equation for the mesh length is the result of a fitting procedure to ensure
        # a maximum of 0.1% deviation of the calculated profile properties compared to
        # the analytical solution for various triangular geometries.
        mesh_length = max(min(self.base, self.height) / 20, 2.0)
        return partial(Geometry.create_mesh, mesh_sizes=mesh_length**2)

    @property
    def _polygon(self) -> Polygon:
        """
        Shapely Polygon representing the right-angled triangular profile.

        Returns
        -------
        Polygon
            The shapely Polygon representing the triangle.
        """
        left_lower = (self.x, self.y)
        right_lower = (self.x + self.base, self.y)
        top = (self.x, self.y + self.height)

        if self.mirrored_horizontally:
            right_lower = (2 * left_lower[0] - right_lower[0], right_lower[1])
        if self.mirrored_vertically:
            top = (top[0], 2 * left_lower[1] - top[1])

        return Polygon(np.round([left_lower, right_lower, top], self.accuracy))
