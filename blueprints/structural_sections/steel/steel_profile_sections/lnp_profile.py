"""LNP-Profile section."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.structural_sections._polygon_builder import PolygonBuilder
from blueprints.structural_sections.steel.steel_profile_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative

if TYPE_CHECKING:
    from blueprints.structural_sections.steel.standard_profiles.lnp import LNP  # pragma: no cover


@dataclass(frozen=True, kw_only=True)
class LNPProfile(CrossSection):
    """Representation of an LNP section.

    Web is the vertical part and base is the horizontal part of the LNP-profile.

    Attributes
    ----------
    total_width : MM
        The total width of the profile [mm].
    total_height : MM
        The total height of the profile [mm].
    web_thickness : MM
        The thickness of the web [mm].
    base_thickness : MM
        The thickness of the base [mm].
    root_radius : MM
        The inner radius of the web-base corner.
    back_radius : MM
        The outer radius of the web-base corner.
    web_toe_radius : MM
        The radius of the toe in the web.
    base_toe_radius : MM
        The radius of the toe in the base.
    name : str
        The name of the profile. Default is "LNP-Profile". If corrosion is applied, the name will include the corrosion value.
    plotter : Callable[[CrossSection], plt.Figure]
        The plotter function to visualize the cross-section (default: `plot_shapes`).
    """

    total_width: MM
    """ The total width of the profile [mm]. """
    total_height: MM
    """ The total height of the profile [mm]. """
    web_thickness: MM
    """ The thickness of the web [mm]. """
    base_thickness: MM
    """ The thickness of the base [mm]. """
    root_radius: MM
    """ The inner radius of the web-base corner [mm]. """
    back_radius: MM
    """ The outer radius of the web-base corner [mm]. """
    web_toe_radius: MM
    """ The radius of the toe in the web [mm]. """
    base_toe_radius: MM
    """ The radius of the toe in the base [mm]. """
    name: str = "LNP-Profile"
    """ The name of the profile. """
    plotter: Callable[[CrossSection], plt.Figure] = plot_shapes
    """ The plotter function to visualize the cross-section. """
    web_toe_straight_part: MM = field(init=False)
    """ The straight part of the web before the toe radius [mm]. """
    base_toe_straight_part: MM = field(init=False)
    """ The straight part of the base before the toe radius [mm]. """
    web_outer_height: MM = field(init=False)
    """ The outer height of the web [mm]. """
    web_inner_height: MM = field(init=False)
    """ The inner height of the web [mm]. """
    base_outer_width: MM = field(init=False)
    """ The outer width of the base [mm]. """
    base_inner_width: MM = field(init=False)
    """ The inner width of the base [mm]. """

    def __post_init__(self) -> None:
        """Post-process the LNP-profile section after initialization."""
        object.__setattr__(self, "web_toe_straight_part", self.web_thickness - self.web_toe_radius)
        object.__setattr__(self, "base_toe_straight_part", self.base_thickness - self.base_toe_radius)

        object.__setattr__(self, "web_outer_height", self.total_height - self.back_radius)
        object.__setattr__(self, "web_inner_height", self.total_height - self.base_thickness - self.root_radius - self.web_toe_radius)

        object.__setattr__(self, "base_outer_width", self.total_width - self.back_radius)
        object.__setattr__(self, "base_inner_width", self.total_width - self.web_thickness - self.root_radius - self.base_toe_radius)

        raise_if_negative(
            web_toe_straight_part=self.web_toe_straight_part,
            base_toe_straight_part=self.base_toe_straight_part,
            web_outer_height=self.web_outer_height,
            web_inner_height=self.web_inner_height,
            base_outer_width=self.base_outer_width,
            base_inner_width=self.base_inner_width,
        )

    @property
    def polygon(self) -> Polygon:
        """Return the polygon of the LNP profile section."""
        return (
            # Start from top left corner and go clockwise
            PolygonBuilder(starting_point=(0, 0))
            # Web
            .append_line(length=self.web_toe_straight_part, angle=0)
            .append_arc(sweep=-90, angle=0, radius=self.web_toe_radius)
            .append_line(length=self.web_inner_height, angle=270)
            # Root radius
            .append_arc(sweep=90, angle=270, radius=self.root_radius)
            # Base
            .append_line(length=self.base_inner_width, angle=0)
            .append_arc(sweep=-90, angle=0, radius=self.base_toe_radius)
            .append_line(length=self.base_toe_straight_part, angle=270)
            .append_line(length=self.base_outer_width, angle=180)
            # Back radius
            .append_arc(sweep=-90, angle=180, radius=self.back_radius)
            # Web
            .append_line(length=self.web_outer_height, angle=90)
            .generate_polygon()
        )

    @classmethod
    def from_standard_profile(
        cls,
        profile: LNP,
        corrosion: MM = 0,
    ) -> Self:
        """Create an LNP-profile from a set of standard profiles already defined in Blueprints.

        Blueprints offers standard profiles for LNP. This method allows you to create an LNP-profile.

        Parameters
        ----------
        profile : LNP
            Any of the standard profiles defined in Blueprints.
        corrosion : MM, optional
            Corrosion thickness per side (default is 0).
        """
        total_width = profile.width - 2 * corrosion
        total_height = profile.height - 2 * corrosion

        web_thickness = profile.web_thickness - 2 * corrosion
        base_thickness = profile.base_thickness - 2 * corrosion

        root_radius = profile.root_radius + corrosion
        back_radius = max(profile.back_radius - corrosion, 0)
        base_toe_radius = max(profile.toe_radius - corrosion, 0)
        web_toe_radius = max(profile.toe_radius - corrosion, 0)

        if any(
            [
                web_thickness < 1e-3,
                base_thickness < 1e-3,
            ]
        ):
            raise ValueError("The profile has fully corroded.")

        name = profile.alias
        if corrosion:
            name += f" (corrosion: {corrosion} mm)"

        return cls(
            total_width=total_width,
            total_height=total_height,
            web_thickness=web_thickness,
            base_thickness=base_thickness,
            root_radius=root_radius,
            back_radius=back_radius,
            web_toe_radius=web_toe_radius,
            base_toe_radius=base_toe_radius,
            name=name,
        )
