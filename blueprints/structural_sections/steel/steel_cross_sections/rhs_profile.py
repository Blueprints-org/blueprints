"""RHS- and SHS-Profile section."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.structural_sections._polygon_builder import PolygonBuilder
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhscf import RHSCF
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shs import SHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shscf import SHSCF
from blueprints.type_alias import MM


@dataclass(kw_only=True)
class RHSProfile(CrossSection):
    """Representation of an SHS or RHS section.

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
    plotter : Callable[[CrossSection], plt.Figure]
        The plotter function to visualize the cross-section (default: `plot_shapes`).
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
    plotter: Callable[[CrossSection], plt.Figure] = plot_shapes
    """The plotter function to visualize the cross-section."""

    def __post_init__(self) -> None:
        """Initialize the RHS- or SHS-profile section."""
        self.right_wall_outer_height = self.total_height - self.top_right_outer_radius - self.bottom_right_outer_radius
        self.left_wall_outer_height = self.total_height - self.top_left_outer_radius - self.bottom_left_outer_radius
        self.top_wall_outer_width = self.total_width - self.top_right_outer_radius - self.top_left_outer_radius
        self.bottom_wall_outer_width = self.total_width - self.bottom_right_outer_radius - self.bottom_left_outer_radius

        self.right_wall_inner_height = (
            self.total_height - self.top_wall_thickness - self.bottom_wall_thickness - self.top_right_inner_radius - self.bottom_right_inner_radius
        )
        self.left_wall_inner_height = (
            self.total_height - self.top_wall_thickness - self.bottom_wall_thickness - self.top_left_inner_radius - self.bottom_left_inner_radius
        )
        self.top_wall_inner_width = (
            self.total_width - self.left_wall_thickness - self.right_wall_thickness - self.top_right_inner_radius - self.top_left_inner_radius
        )
        self.bottom_wall_inner_width = (
            self.total_width - self.left_wall_thickness - self.right_wall_thickness - self.bottom_right_inner_radius - self.bottom_left_inner_radius
        )

    @property
    def polygon(self) -> Polygon:
        """Return the polygon of the RHS profile section."""
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
        return Polygon(shell=outer_polygon.exterior.coords, holes={inner_polygon.exterior.coords})

    @classmethod
    def from_standard_profile(
        cls,
        profile: RHS | SHS | RHSCF | SHSCF,
        corrosion_outside: MM = 0,
        corrosion_inside: MM = 0,
    ) -> Self:
        """Create an RHS- or SHS-profile from a set of standard profiles already defined in Blueprints.

        Blueprints offers standard profiles for RHS, SHS, RHSCF, and SHSCF. This method allows you to create an RHS/SHS-profile.

        Parameters
        ----------
        profile : RHS | SHS | RHSCF | SHSCF
            Any of the standard profiles defined in Blueprints.
        corrosion_outside : MM, optional
            Corrosion thickness to be subtracted from the outer diameter [mm] (default: 0).
        corrosion_inside : MM, optional
            Corrosion thickness to be added to the inner diameter [mm] (default: 0).
        """
        total_width = profile.total_width - 2 * corrosion_outside
        total_height = profile.total_height - 2 * corrosion_outside

        top_wall_thickness = profile.thickness - corrosion_outside - corrosion_inside
        bottom_wall_thickness = profile.thickness - corrosion_outside - corrosion_inside
        left_wall_thickness = profile.thickness - corrosion_outside - corrosion_inside
        right_wall_thickness = profile.thickness - corrosion_outside - corrosion_inside

        top_right_inner_radius = profile.inner_radius + corrosion_inside
        top_left_inner_radius = profile.inner_radius + corrosion_inside
        bottom_right_inner_radius = profile.inner_radius + corrosion_inside
        bottom_left_inner_radius = profile.inner_radius + corrosion_inside
        top_right_outer_radius = max(profile.outer_radius - corrosion_outside, 0)
        top_left_outer_radius = max(profile.outer_radius - corrosion_outside, 0)
        bottom_right_outer_radius = max(profile.outer_radius - corrosion_outside, 0)
        bottom_left_outer_radius = max(profile.outer_radius - corrosion_outside, 0)

        if any(
            [
                top_wall_thickness < 1e-3,
                bottom_wall_thickness < 1e-3,
                left_wall_thickness < 1e-3,
                right_wall_thickness < 1e-3,
            ]
        ):
            raise ValueError("The profile has fully corroded.")

        name = profile.alias
        if corrosion_inside or corrosion_outside:
            name += (
                f" (corrosion {'' if not corrosion_inside else f'in: {corrosion_inside} mm'}"
                f"{', ' if corrosion_inside and corrosion_outside else ''}"
                f"{'' if not corrosion_outside else f'out: {corrosion_outside} mm'})"
            )

        return cls(
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
        )
