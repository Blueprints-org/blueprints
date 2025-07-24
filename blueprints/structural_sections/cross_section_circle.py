"""Circular cross-section shape."""

from dataclasses import dataclass

from sectionproperties.pre import Geometry
from shapely import Point, Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import MM


@dataclass(frozen=True)
class CircularCrossSection(CrossSection):
    """
    Class to represent a circular cross-section using shapely for geometric calculations.

    Parameters
    ----------
    diameter : MM
        The diameter of the circular cross-section [mm].
    x : MM
        The x-coordinate of the circle's center.
    y : MM
        The y-coordinate of the circle's center.
    name : str
        The name of the rectangular cross-section, default is "Circle".
    """

    diameter: MM
    x: MM
    y: MM
    name: str = "Circle"

    def __post_init__(self) -> None:
        """Post-initialization to validate the diameter."""
        if self.diameter <= 0:
            msg = f"Diameter must be a positive value, but got {self.diameter}"
            raise ValueError(msg)

    @property
    def radius(self) -> MM:
        """
        Calculate the radius of the circular cross-section [mm].

        Returns
        -------
        MM
            The radius of the circle.
        """
        return self.diameter / 2.0

    @property
    def polygon(self) -> Polygon:
        """
        Shapely Polygon representing the circular cross-section.

        Returns
        -------
        Polygon
            The shapely Polygon representing the circle.
        """
        centroid = Point(self.x, self.y)
        return centroid.buffer(self.radius)

    def geometry(
        self,
        mesh_size: MM | None = None,
    ) -> Geometry:
        """Return the geometry of the circular cross-section.

        Properties
        ----------
        mesh_size : MM
            Maximum mesh element area to be used within
            the Geometry-object finite-element mesh. If not provided, a default value will be used.

        """
        if mesh_size is None:
            minimum_mesh_size = 2.0
            mesh_length = max(self.diameter / 20, minimum_mesh_size)
            mesh_size = mesh_length**2

        circular = Geometry(geom=self.polygon)
        circular.create_mesh(mesh_sizes=mesh_size)
        return circular
