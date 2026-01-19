"""Circular profile shape."""

from dataclasses import dataclass
from functools import partial

from sectionproperties.pre import Geometry
from shapely import Point, Polygon

from blueprints.structural_sections._profile import Profile
from blueprints.type_alias import MM


@dataclass(frozen=True)
class CircularProfile(Profile):
    """
    Class to represent a circular profile using shapely for geometric calculations.

    Parameters
    ----------
    diameter : MM
        The diameter of the circular profile [mm].
    x : MM
        The x-coordinate of the circle's center.
    y : MM
        The y-coordinate of the circle's center.
    name : str
        The name of the circular profile, default is "Circle".
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
    def max_profile_thickness(self) -> MM:
        """Maximum element thickness of the circular profile [mm]."""
        return self.diameter

    @property
    def mesh_creator(self) -> partial:
        """Mesh settings for the geometrical calculations of the circular profile."""
        # The equation for the mesh length is the result of a fitting procedure to ensure
        # a maximum of 0.1% deviation of the calculated profile properties compared to
        # the analytical solution for various circular geometries.
        mesh_length = max(self.diameter / 20, 2.0)
        return partial(Geometry.create_mesh, mesh_sizes=mesh_length**2)

    @property
    def radius(self) -> MM:
        """
        Calculate the radius of the circular profile [mm].

        Returns
        -------
        MM
            The radius of the circle.
        """
        return self.diameter / 2.0

    @property
    def _polygon(self) -> Polygon:
        """
        Shapely Polygon representing the circular profile.

        Returns
        -------
        Polygon
            The shapely Polygon representing the circle.
        """
        centroid = Point(self.x, self.y)
        return centroid.buffer(self.radius)
