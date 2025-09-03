"""Triangular cross-section shape."""

from dataclasses import dataclass

import numpy as np
from sectionproperties.pre import Geometry
from shapely import Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM


@dataclass(frozen=True)
class RightAngledTriangularCrossSection(CrossSection):
    """
    Class to represent a right-angled triangular with a right angle at the bottom left corner cross-section for geometric calculations.

    Parameters
    ----------
    base : MM
        The base length of the triangular cross-section.
    height : MM
        The height of the triangular cross-section.
    x : MM
        The x-coordinate of the 90-degree angle. Default is 0.
    y : MM
        The y-coordinate of the 90-degree angle. Default is 0.
    mirrored_horizontally : bool
        Whether the triangle is mirrored horizontally. Default is False.
    mirrored_vertically : bool
        Whether the triangle is mirrored vertically. Default is False.
    name : str
        The name of the rectangular cross-section, default is "Triangle".
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
    def polygon(self) -> Polygon:
        """
        Shapely Polygon representing the right-angled triangular cross-section.

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

        return Polygon(np.round([left_lower, right_lower, top], self.ACCURACY))

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the triangular cross-section.

        Parameters
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        Returns
        -------
        Geometry
            The Geometry object representing the triangular cross-section.
        """
        if mesh_size is None:
            minimum_mesh_size = 2.0
            mesh_length = max(min(self.base, self.height) / 20, minimum_mesh_size)
            mesh_size = mesh_length**2

        triangular = Geometry(geom=self.polygon)
        triangular.create_mesh(mesh_sizes=mesh_size)
        return triangular
