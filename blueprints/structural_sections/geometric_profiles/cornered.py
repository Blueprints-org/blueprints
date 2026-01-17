"""Shape of a circular cornered section."""

from dataclasses import dataclass
from functools import partial

import numpy as np
from sectionproperties.pre import Geometry
from shapely.geometry import Polygon

from blueprints.structural_sections._profile import Profile
from blueprints.type_alias import MM, PERCENTAGE
from blueprints.validations import raise_if_negative


@dataclass(frozen=True)
class CircularCorneredProfile(Profile):
    """
    Class to represent a square profile with a quarter circle cutout for geometric calculations, named as a circular cornered profile.

    .---- outer reference point
    |
    |   .---- outer arc     .---- o_a_ext_at_vertical
    v   ∨                   v
    x . .+-----------------------+
    .  ⁄                         |
    .⁄                           |<-- thickness_vertical
    +                            |
    |                        _ _ |<-- inner arc
    |                      /
    |                    /
    |                   |
    +-------------------+        x-- intersection reference point
             ^
             .---- thickness_horizontal

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
    inner_slope_at_vertical : PERCENTAGE
        Slope of the tangent to the inner radius at the vertical section (default 0)
    inner_slope_at_horizontal : PERCENTAGE
        Slope of the tangent to the inner radius at the horizontal section (default 0)
    outer_slope_at_vertical : PERCENTAGE
        Slope of the tangent to the outer radius at the vertical section (default 0)
    outer_slope_at_horizontal : PERCENTAGE
        Slope of the tangent to the outer radius at the horizontal section (default 0)
    x : MM
        x-coordinate of reference point
    y : MM
        y-coordinate of reference point
    reference_point : str
        Where x and y are located, options are
        'intersection' (intersection of vertical and horizontal sections),
        'outer' (where corner outer arc would be if it was sharp 90 degree corner)
        (default 'intersection')
    name : str
        Name of the profile (default "Corner")
    """

    thickness_vertical: MM
    thickness_horizontal: MM
    inner_radius: MM
    outer_radius: MM
    corner_direction: int = 0  # 0 = ↰, 1 = ↱, 2 = ↳, 3 = ↲
    inner_slope_at_vertical: PERCENTAGE = 0
    inner_slope_at_horizontal: PERCENTAGE = 0
    outer_slope_at_vertical: PERCENTAGE = 0
    outer_slope_at_horizontal: PERCENTAGE = 0
    reference_point: str = "intersection"
    x: MM = 0
    y: MM = 0
    name: str = "Corner"

    def __post_init__(self) -> None:
        """Validate input parameters after initialization."""
        raise_if_negative(
            thickness_vertical=self.thickness_vertical,
            thickness_horizontal=self.thickness_horizontal,
            inner_radius=self.inner_radius,
            outer_radius=self.outer_radius,
            inner_slope_at_vertical=self.inner_slope_at_vertical,
            inner_slope_at_horizontal=self.inner_slope_at_horizontal,
            outer_slope_at_vertical=self.outer_slope_at_vertical,
            outer_slope_at_horizontal=self.outer_slope_at_horizontal,
        )

        if self.reference_point not in ("intersection", "outer"):
            raise ValueError(f"reference_point must be either 'intersection' or 'outer', got {self.reference_point}")
        if self.corner_direction not in (0, 1, 2, 3):
            raise ValueError(f"corner_direction must be one of 0, 1, 2, or 3, got {self.corner_direction}")
        if any(
            slope >= 100
            for slope in [self.inner_slope_at_vertical, self.inner_slope_at_horizontal, self.outer_slope_at_vertical, self.outer_slope_at_horizontal]
        ):
            raise ValueError("All slopes must be less than 100%")

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
        n = 16

        # Outer arc (from vertical to horizontal)
        outer_arc = np.column_stack(
            (
                self.outer_radius * np.cos(np.linspace(self.outer_angle_at_horizontal, np.pi / 2 - self.outer_angle_at_vertical, n)),
                self.outer_radius * np.sin(np.linspace(self.outer_angle_at_horizontal, np.pi / 2 - self.outer_angle_at_vertical, n)),
            )
        )
        o_a_width = np.max(outer_arc[:, 0]) - np.min(outer_arc[:, 0])
        o_a_height = np.max(outer_arc[:, 1]) - np.min(outer_arc[:, 1])

        # Inner arc (from horizontal to vertical, reversed)
        inner_arc = np.column_stack(
            (
                self.inner_radius * np.cos(np.linspace(self.inner_angle_at_horizontal, np.pi / 2 - self.inner_angle_at_vertical, n)),
                self.inner_radius * np.sin(np.linspace(self.inner_angle_at_horizontal, np.pi / 2 - self.inner_angle_at_vertical, n)),
            )
        )[::-1]
        i_a_width = np.max(inner_arc[:, 0]) - np.min(inner_arc[:, 0])
        i_a_height = np.max(inner_arc[:, 1]) - np.min(inner_arc[:, 1])

        # Based on input it's possible that either the outer arc or the inner arc is wider/taller
        # than the other (plus thickness). To align them, we need to extend one of the arcs.
        if o_a_width > i_a_width + self.thickness_horizontal and o_a_height > i_a_height + self.thickness_vertical:
            a = np.array(
                [
                    [np.sin(self.inner_angle_at_horizontal), np.cos(self.inner_angle_at_vertical)],
                    [np.cos(self.inner_angle_at_horizontal), np.sin(self.inner_angle_at_vertical)],
                ]
            )
            b = np.array([o_a_width - i_a_width - self.thickness_horizontal, o_a_height - i_a_height - self.thickness_vertical])
            i_a_ext_at_horizontal, i_a_ext_at_vertical = np.linalg.solve(a, b)
            o_a_ext_at_horizontal = o_a_ext_at_vertical = 0
        else:
            a = np.array(
                [
                    [np.sin(self.outer_angle_at_horizontal), np.cos(self.outer_angle_at_vertical)],
                    [np.cos(self.outer_angle_at_horizontal), np.sin(self.outer_angle_at_vertical)],
                ]
            )
            b = np.array([i_a_width + self.thickness_horizontal - o_a_width, i_a_height + self.thickness_vertical - o_a_height])
            o_a_ext_at_horizontal, o_a_ext_at_vertical = np.linalg.solve(a, b)
            i_a_ext_at_horizontal = i_a_ext_at_vertical = 0

        total_width = (
            o_a_width + o_a_ext_at_horizontal * np.sin(self.outer_angle_at_horizontal) + o_a_ext_at_vertical * np.cos(self.outer_angle_at_vertical)
        )
        total_height = (
            o_a_height + o_a_ext_at_horizontal * np.cos(self.outer_angle_at_horizontal) + o_a_ext_at_vertical * np.sin(self.outer_angle_at_vertical)
        )

        # Translate outer arc points and allow for corrosion resulting in sharper angle
        outer_arc[:, 0] += o_a_ext_at_vertical * np.cos(self.outer_angle_at_vertical) - np.min(outer_arc[:, 0])
        outer_arc[:, 1] += o_a_ext_at_horizontal * np.cos(self.outer_angle_at_horizontal) - np.min(outer_arc[:, 1])

        # heavy corrosion of for example UNP-elements might lead to situations where the toe radius corrodes
        # into the flat side of the flange. This results in a non-90 degree corner
        if o_a_ext_at_horizontal < 0:
            x_at_y_is_zero = np.interp(0, outer_arc[:, 1], outer_arc[:, 0])
            outer_arc = np.vstack([[x_at_y_is_zero, 0], outer_arc[outer_arc[:, 1] >= 0]])
        if o_a_ext_at_vertical < 0:
            y_at_x_is_zero = np.interp(0, outer_arc[:, 0][::-1], outer_arc[:, 1][::-1])
            outer_arc = np.vstack([outer_arc[outer_arc[:, 0] >= 0], [0, y_at_x_is_zero]])

        # Translate inner arc points
        inner_arc[:, 0] += i_a_ext_at_vertical * np.cos(self.inner_angle_at_vertical) - np.min(inner_arc[:, 0])
        inner_arc[:, 1] += i_a_ext_at_horizontal * np.cos(self.inner_angle_at_horizontal) - np.min(inner_arc[:, 1])

        # Combine points
        points = np.vstack(
            [
                (total_width, 0),
                outer_arc,
                (0, total_height),
                (0, total_height - self.thickness_vertical),
                inner_arc,
                (total_width - self.thickness_horizontal, 0),
                (total_width, 0),
            ]
        )

        # Remove redundant points if corrosion has removed part of the arc
        if o_a_ext_at_horizontal < 0:
            points = points[points[:, 0] <= x_at_y_is_zero]
        if o_a_ext_at_vertical < 0:
            points = points[points[:, 1] <= y_at_x_is_zero]

        # Remove consecutive duplicate points
        mask = np.any(np.diff(points, axis=0) != 0, axis=1)
        points = points[np.insert(mask, 0, True)]

        # Shift points to make outer reference point at (x, y)
        if self.reference_point == "outer":
            points[:, 0] -= total_width
            points[:, 1] -= total_height

        # Apply flips based on corner_direction
        if self.corner_direction in (1, 2):
            points = points @ np.array([[-1, 0], [0, 1]])
        if self.corner_direction in (2, 3):
            points = points @ np.array([[1, 0], [0, -1]])

        # Shift points
        points += np.array([self.x, self.y])
        points = np.array([tuple(pt) for pt in points])

        return Polygon(np.round(points, self.accuracy))
