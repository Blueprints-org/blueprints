"""Shape of a circular cornered section."""

from dataclasses import dataclass
from functools import partial

import numpy as np
from sectionproperties.pre import Geometry
from shapely.geometry import Polygon

from blueprints.structural_sections._profile import Profile
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


@dataclass(frozen=True)
class CircularCorneredProfile(Profile):
    """
    Class to represent a square profile with a quarter circle cutout for geometric calculations, named as a circular cornered profile.

        .---- outer arc
        ∨
    . . .+-----------------------+
    .  ⁄                         |
    .⁄                           |<-- thickness_vertical
    +                            |
    |                        _ _ |<-- inner arc
    |                      /
    |                    /
    |                   |
    +-------------------+<-- thickness_horizontal

    Parameters
    ----------
    thickness_vertical : MM
        Thickness of the vertical section
    thickness_horizontal : MM
        Thickness of the horizontal section
    inner_radius : MM
        Inner radius of the corner
    outer_radius : MM
        Outer radius of the corner
    corner_direction : int
        ↰ = 0, ↱ = 1, ↳ = 2, ↲ = 3
    x : MM
        x-coordinate of the center of the inner_radius (default 0)
    y : MM
        y-coordinate of the center of the inner_radius (default 0)
    name : str
        Name of the profile (default "Corner")
    """

    thickness_vertical: MM
    thickness_horizontal: MM
    inner_radius: MM
    outer_radius: MM
    x: MM = 0
    y: MM = 0
    corner_direction: int = 0  # 0 = ↰, 1 = ↱, 2 = ↳, 3 = ↲
    name: str = "Corner"

    def __post_init__(self) -> None:
        """Validate input parameters after initialization."""
        raise_if_negative(
            thickness_vertical=self.thickness_vertical,
            thickness_horizontal=self.thickness_horizontal,
            inner_radius=self.inner_radius,
            outer_radius=self.outer_radius,
        )
        if self.outer_radius > self.inner_radius + min(self.thickness_vertical, self.thickness_horizontal):
            raise ValueError(
                f"Outer radius {self.outer_radius} must be smaller than or equal to inner radius {self.inner_radius} "
                f"plus the thickness {min(self.thickness_vertical, self.thickness_horizontal)}"
            )
        if self.corner_direction not in (0, 1, 2, 3):
            raise ValueError(f"corner_direction must be one of 0, 1, 2, or 3, got {self.corner_direction}")

    @property
    def max_thickness(self) -> MM:
        """Maximum element thickness of the corner profile [mm]."""
        return min(self.thickness_vertical, self.thickness_horizontal)

    @property
    def mesh_creator(self) -> partial:
        """Mesh settings for the geometrical calculations of the corner profile."""
        # The equation for the mesh length is the result of a fitting procedure to ensure
        # a maximum of 0.1% deviation of the calculated profile properties compared to
        # the analytical solution for various cornered geometries.
        mesh_length = max(min(self.thickness_vertical, self.thickness_horizontal) / 2, 2.0)
        return partial(Geometry.create_mesh, mesh_sizes=mesh_length**2)

    @property
    def width_rectangle(self) -> MM:
        """Width of the rectangle part of the corner profile [mm]."""
        return self.thickness_horizontal + self.inner_radius

    @property
    def height_rectangle(self) -> MM:
        """Height of the rectangle part of the corner profile [mm]."""
        return self.thickness_vertical + self.inner_radius

    @property
    def _polygon(self) -> Polygon:
        """Shapely Polygon representing the corner profile."""
        lr = (self.x + self.width_rectangle, self.y)
        ul = (self.x, self.y + self.height_rectangle)

        n = 16

        # Outer arc (from vertical to horizontal)
        theta_outer = np.linspace(0, np.pi / 2, n)
        outer_arc = np.column_stack(
            (
                self.x + self.width_rectangle - self.outer_radius + self.outer_radius * np.cos(theta_outer),
                self.y + self.height_rectangle - self.outer_radius + self.outer_radius * np.sin(theta_outer),
            )
        )

        # Inner arc (from horizontal to vertical, reversed)
        theta_inner = np.linspace(0, np.pi / 2, n)
        inner_arc = np.column_stack(
            (
                self.x + self.inner_radius * np.cos(theta_inner),
                self.y + self.inner_radius * np.sin(theta_inner),
            )
        )[::-1]

        # Combine points
        points = np.vstack([lr, outer_arc, ul, inner_arc])

        # Remove consecutive duplicate points
        diff = np.diff(points, axis=0)
        mask = np.any(diff != 0, axis=1)
        mask = np.insert(mask, 0, True)
        points = points[mask]

        # Create transformation matrices for flipping
        flip_x = np.array([[-1, 0], [0, 1]])
        flip_y = np.array([[1, 0], [0, -1]])

        # Center points around (self.x, self.y)
        points_centered = points - np.array([self.x, self.y])

        # Apply flips based on corner_direction
        if self.corner_direction in (1, 2):
            points_centered = points_centered @ flip_x
        if self.corner_direction in (2, 3):
            points_centered = points_centered @ flip_y

        # Shift points back
        points = points_centered + np.array([self.x, self.y])

        points = np.array([tuple(pt) for pt in points])

        return Polygon(np.round(points, self.accuracy))
