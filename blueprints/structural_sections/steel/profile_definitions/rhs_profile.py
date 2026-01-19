"""RHS- and SHS-Profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

from blueprints.structural_sections._polygon_builder import PolygonBuilder
from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.profile_definitions.corrosion_utils import FULL_CORROSION_TOLERANCE, update_name_with_corrosion
from blueprints.structural_sections.steel.profile_definitions.plotters.general_steel_plotter import plot_shapes
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


@dataclass(frozen=True, kw_only=True)
class RHSProfile(Profile):
    """Representation of an SHS or RHS profile.

    Attributes
    ----------
    total_width : MM
        The width of the profile [mm].
    total_height : MM
        The height of the profile [mm].
    left_wall_thickness : MM
        The thickness of the left wall [mm].
    right_wall_thickness : MM
        The thickness of the right wall [mm].
    top_wall_thickness : MM
        The thickness of the top wall [mm].
    bottom_wall_thickness : MM
        The thickness of the bottom wall [mm].
    top_right_inner_radius : MM
        The inner radius of the top right corner. Default is 0.
    top_left_inner_radius : MM
        The inner radius of the top left corner. Default is 0.
    bottom_right_inner_radius : MM
        The inner radius of the bottom right corner. Default is 0.
    bottom_left_inner_radius : MM
        The inner radius of the bottom left corner. Default is 0.
    top_right_outer_radius : MM
        The outer radius of the top right corner. Default is 0.
    top_left_outer_radius : MM
        The outer radius of the top left corner. Default is 0.
    bottom_right_outer_radius : MM
        The outer radius of the bottom right corner. Default is 0.
    bottom_left_outer_radius : MM
        The outer radius of the bottom left corner. Default is 0.
    name : str
        The name of the profile. Default is "RHS-Profile". If corrosion is applied, the name will include the corrosion value.
    plotter : Callable[[Profile], plt.Figure]
        The plotter function to visualize the profile (default: `plot_shapes`).
    """

    total_width: MM
    """The total width of the profile [mm]."""
    total_height: MM
    """The total height of the profile [mm]."""
    left_wall_thickness: MM
    """The thickness of the left wall [mm]."""
    right_wall_thickness: MM
    """The thickness of the right wall [mm]."""
    top_wall_thickness: MM
    """The thickness of the top wall [mm]."""
    bottom_wall_thickness: MM
    """The thickness of the bottom wall [mm]."""
    top_right_inner_radius: MM = 0
    """The inner radius of the top right corner [mm]."""
    top_left_inner_radius: MM = 0
    """The inner radius of the top left corner [mm]."""
    bottom_right_inner_radius: MM = 0
    """The inner radius of the bottom right corner [mm]."""
    bottom_left_inner_radius: MM = 0
    """The inner radius of the bottom left corner [mm]."""
    top_right_outer_radius: MM = 0
    """The outer radius of the top right corner [mm]."""
    top_left_outer_radius: MM = 0
    """The outer radius of the top left corner [mm]."""
    bottom_right_outer_radius: MM = 0
    """The outer radius of the bottom right corner [mm]."""
    bottom_left_outer_radius: MM = 0
    """The outer radius of the bottom left corner [mm]."""
    name: str = "RHS-Profile"
    """The name of the profile."""
    plotter: Callable[[Profile], plt.Figure] = plot_shapes
    """The plotter function to visualize the profile."""
    right_wall_outer_height: MM = field(init=False)
    """The outer height of the right wall [mm]."""
    left_wall_outer_height: MM = field(init=False)
    """The outer height of the left wall [mm]."""
    top_wall_outer_width: MM = field(init=False)
    """The outer width of the top wall [mm]."""
    bottom_wall_outer_width: MM = field(init=False)
    """The outer width of the bottom wall [mm]."""
    right_wall_inner_height: MM = field(init=False)
    """The inner height of the right wall [mm]."""
    left_wall_inner_height: MM = field(init=False)
    """The inner height of the left wall [mm]."""
    top_wall_inner_width: MM = field(init=False)
    """The inner width of the top wall [mm]."""
    bottom_wall_inner_width: MM = field(init=False)
    """The inner width of the bottom wall [mm]."""

    def __post_init__(self) -> None:
        """Initialize the RHS- or SHS-profile."""
        object.__setattr__(self, "right_wall_outer_height", self.total_height - self.top_right_outer_radius - self.bottom_right_outer_radius)
        object.__setattr__(self, "left_wall_outer_height", self.total_height - self.top_left_outer_radius - self.bottom_left_outer_radius)
        object.__setattr__(self, "top_wall_outer_width", self.total_width - self.top_right_outer_radius - self.top_left_outer_radius)
        object.__setattr__(self, "bottom_wall_outer_width", self.total_width - self.bottom_right_outer_radius - self.bottom_left_outer_radius)

        object.__setattr__(
            self,
            "right_wall_inner_height",
            self.total_height - self.top_wall_thickness - self.bottom_wall_thickness - self.top_right_inner_radius - self.bottom_right_inner_radius,
        )
        object.__setattr__(
            self,
            "left_wall_inner_height",
            self.total_height - self.top_wall_thickness - self.bottom_wall_thickness - self.top_left_inner_radius - self.bottom_left_inner_radius,
        )
        object.__setattr__(
            self,
            "top_wall_inner_width",
            self.total_width - self.left_wall_thickness - self.right_wall_thickness - self.top_right_inner_radius - self.top_left_inner_radius,
        )
        object.__setattr__(
            self,
            "bottom_wall_inner_width",
            self.total_width - self.left_wall_thickness - self.right_wall_thickness - self.bottom_right_inner_radius - self.bottom_left_inner_radius,
        )
        raise_if_negative(
            right_wall_inner_height=self.right_wall_inner_height,
            left_wall_inner_height=self.left_wall_inner_height,
            top_wall_inner_width=self.top_wall_inner_width,
            bottom_wall_inner_width=self.bottom_wall_inner_width,
        )

    @property
    def max_profile_thickness(self) -> MM:
        """Maximum element thickness of the profile [mm]."""
        return max(self.left_wall_thickness, self.right_wall_thickness, self.top_wall_thickness, self.bottom_wall_thickness)

    @property
    def _polygon(self) -> Polygon:
        """Return the polygon of the RHS profile without the offset and rotation applied."""
        outer_polygon = (
            # Start at top left corner (just to the right of the top left corner) and go clockwise
            PolygonBuilder(starting_point=(0, 0))
            .append_line(length=self.top_wall_outer_width, angle=0)
            .append_arc(sweep=-90, angle=0, radius=self.top_right_outer_radius)
            .append_line(length=self.right_wall_outer_height, angle=270)
            .append_arc(sweep=-90, angle=270, radius=self.bottom_right_outer_radius)
            .append_line(length=self.bottom_wall_outer_width, angle=180)
            .append_arc(sweep=-90, angle=180, radius=self.bottom_left_outer_radius)
            .append_line(length=self.left_wall_outer_height, angle=90)
            .append_arc(sweep=-90, angle=90, radius=self.top_left_outer_radius)
            .generate_polygon()
        )
        inner_polygon = (
            # Start at top left corner (just to the right of the top left corner) and go clockwise
            PolygonBuilder(starting_point=(0, 0))
            .append_line(length=self.top_wall_inner_width, angle=0)
            .append_arc(sweep=-90, angle=0, radius=self.top_right_inner_radius)
            .append_line(length=self.right_wall_inner_height, angle=270)
            .append_arc(sweep=-90, angle=270, radius=self.bottom_right_inner_radius)
            .append_line(length=self.bottom_wall_inner_width, angle=180)
            .append_arc(sweep=-90, angle=180, radius=self.bottom_left_inner_radius)
            .append_line(length=self.left_wall_inner_height, angle=90)
            .append_arc(sweep=-90, angle=90, radius=self.top_left_inner_radius)
            .generate_polygon()
        )
        return Polygon(shell=outer_polygon.exterior.coords, holes=(inner_polygon.exterior.coords,))

    def with_corrosion(self, corrosion_outside: MM = 0, corrosion_inside: MM = 0) -> RHSProfile:
        """Apply corrosion to the RHS- or SHS-profile and return a new RHS- or SHS-profile instance.

        The name attribute of the new instance will be updated to reflect the total corrosion applied
        including any previous corrosion indicated in the original name.

        Parameters
        ----------
        corrosion_outside : MM, optional
            Corrosion to be subtracted from the outer diameter [mm] (default: 0).
        corrosion_inside : MM, optional
            Corrosion to be added to the inner diameter [mm] (default: 0).

        Returns
        -------
        RHSProfile
            A new RHS- or SHS-profile instance with the applied corrosion.

        Raises
        ------
        ValueError
            If the profile has fully corroded.
        """
        raise_if_negative(corrosion_outside=corrosion_outside)
        raise_if_negative(corrosion_inside=corrosion_inside)

        if corrosion_inside == 0 and corrosion_outside == 0:
            return self

        total_width = self.total_width - 2 * corrosion_outside
        total_height = self.total_height - 2 * corrosion_outside

        top_wall_thickness = self.top_wall_thickness - corrosion_outside - corrosion_inside
        bottom_wall_thickness = self.bottom_wall_thickness - corrosion_outside - corrosion_inside
        left_wall_thickness = self.left_wall_thickness - corrosion_outside - corrosion_inside
        right_wall_thickness = self.right_wall_thickness - corrosion_outside - corrosion_inside

        top_right_inner_radius = self.top_right_inner_radius + corrosion_inside
        top_left_inner_radius = self.top_left_inner_radius + corrosion_inside
        bottom_right_inner_radius = self.bottom_right_inner_radius + corrosion_inside
        bottom_left_inner_radius = self.bottom_left_inner_radius + corrosion_inside
        top_right_outer_radius = max(self.top_right_outer_radius - corrosion_outside, 0)
        top_left_outer_radius = max(self.top_left_outer_radius - corrosion_outside, 0)
        bottom_right_outer_radius = max(self.bottom_right_outer_radius - corrosion_outside, 0)
        bottom_left_outer_radius = max(self.bottom_left_outer_radius - corrosion_outside, 0)

        if any(
            thickness < FULL_CORROSION_TOLERANCE
            for thickness in (
                top_wall_thickness,
                bottom_wall_thickness,
                left_wall_thickness,
                right_wall_thickness,
            )
        ):
            raise ValueError("The profile has fully corroded.")

        name = update_name_with_corrosion(self.name, corrosion_inside=corrosion_inside, corrosion_outside=corrosion_outside)

        return RHSProfile(
            total_width=total_width,
            total_height=total_height,
            left_wall_thickness=left_wall_thickness,
            right_wall_thickness=right_wall_thickness,
            top_wall_thickness=top_wall_thickness,
            bottom_wall_thickness=bottom_wall_thickness,
            top_right_inner_radius=top_right_inner_radius,
            top_left_inner_radius=top_left_inner_radius,
            bottom_right_inner_radius=bottom_right_inner_radius,
            bottom_left_inner_radius=bottom_left_inner_radius,
            top_right_outer_radius=top_right_outer_radius,
            top_left_outer_radius=top_left_outer_radius,
            bottom_right_outer_radius=bottom_right_outer_radius,
            bottom_left_outer_radius=bottom_left_outer_radius,
            name=name,
            plotter=self.plotter,
        )
