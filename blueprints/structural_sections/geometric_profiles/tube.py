"""Circular tube profile shape."""

from dataclasses import dataclass
from functools import partial

from sectionproperties.pre import Geometry
from shapely import Point, Polygon

from blueprints.structural_sections._profile import Profile
from blueprints.type_alias import MM


@dataclass(frozen=True)
class TubeProfile(Profile):
    """
    Class to represent a circular tube profile using shapely for geometric calculations.

    Parameters
    ----------
    outer_diameter : MM
        The outer diameter of the circular tube profile [mm].
    inner_diameter : MM
        The inner diameter of the circular tube profile [mm].
    x : MM
        The x-coordinate of the tube's center.
    y : MM
        The y-coordinate of the tube's center.
    name : str
        The name of the tube profile, default is "Tube".
    """

    outer_diameter: MM
    inner_diameter: MM
    x: MM
    y: MM
    name: str = "Tube"

    def __post_init__(self) -> None:
        """Post-initialization to validate the diameters."""
        if self.outer_diameter <= 0:
            msg = f"Outer diameter must be a positive value, but got {self.outer_diameter}"
            raise ValueError(msg)
        if self.inner_diameter < 0:
            msg = f"Inner diameter cannot be negative, but got {self.inner_diameter}"
            raise ValueError(msg)
        if self.inner_diameter >= self.outer_diameter:
            msg = f"Inner diameter must be smaller than outer diameter, but got inner: {self.inner_diameter}, outer: {self.outer_diameter}"
            raise ValueError(msg)

    @property
    def max_thickness(self) -> MM:
        """Maximum element thickness of the tube profile [mm]."""
        return self.wall_thickness

    @property
    def mesh_creator(self) -> partial:
        """Mesh settings for the geometrical calculations of the tube profile."""
        # The equation for the mesh length is the result of a fitting procedure to ensure
        # a maximum of 0.1% deviation of the calculated profile properties compared to
        # the analytical solution for various tube geometries.
        mesh_length = max(self.wall_thickness / 3, 1.0)
        return partial(Geometry.create_mesh, mesh_sizes=mesh_length**2)

    @property
    def outer_radius(self) -> MM:
        """
        Calculate the outer radius of the circular tube profile [mm].

        Returns
        -------
        MM
            The outer radius of the tube.
        """
        return self.outer_diameter / 2.0

    @property
    def inner_radius(self) -> MM:
        """
        Calculate the inner radius of the circular tube profile [mm].

        Returns
        -------
        MM
            The inner radius of the tube.
        """
        return self.inner_diameter / 2.0

    @property
    def wall_thickness(self) -> MM:
        """
        Calculate the thickness of the tube wall [mm].

        Returns
        -------
        MM
            The thickness of the tube wall.
        """
        return self.outer_radius - self.inner_radius

    @property
    def _polygon(self) -> Polygon:
        """
        Shapely Polygon representing the circular tube profile.

        Returns
        -------
        Polygon
            The shapely Polygon representing the tube.
        """
        center = Point(self.x, self.y)
        quad_segs = 64
        outer_circle = center.buffer(self.outer_radius, quad_segs=quad_segs)
        inner_circle = center.buffer(self.inner_radius, quad_segs=quad_segs)
        difference = outer_circle.difference(inner_circle)
        return Polygon(difference)  # type: ignore[arg-type]
