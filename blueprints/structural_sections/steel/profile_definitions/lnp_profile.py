"""LNP-Profile."""

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
class LNPProfile(Profile):
    """Representation of an LNP profile.

    Web is the vertical part and base is the horizontal part of the LNP-profile.

    Attributes
    ----------
    total_height : MM
        The total height of the profile [mm].
    total_width : MM
        The total width of the profile [mm].
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
    plotter : Callable[[Profile], plt.Figure]
        The plotter function to visualize the profile (default: `plot_shapes`).
    """

    total_height: MM
    """ The total height of the profile [mm]. """
    total_width: MM
    """ The total width of the profile [mm]. """
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
    plotter: Callable[[Profile], plt.Figure] = plot_shapes
    """ The plotter function to visualize the profile. """
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
        """Post-process the LNP-profile after initialization."""
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
    def max_thickness(self) -> MM:
        """Maximum element thickness of the profile [mm]."""
        return max(self.web_thickness, self.base_thickness)

    @property
    def _polygon(self) -> Polygon:
        """Return the polygon of the LNP profile without the offset and rotation applied."""
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

    def with_corrosion(self, corrosion: MM = 0) -> LNPProfile:
        """Return a new LNP profile with corrosion applied.

        The name attribute of the new instance will be updated to reflect the total corrosion applied
        including any previous corrosion indicated in the original name.

        Parameters
        ----------
        corrosion : MM, optional
            Corrosion per side (default is 0).

        Returns
        -------
        LNPProfile
            A new LNPProfile instance with the specified corrosion applied.

        Raises
        ------
        ValueError
            If the resulting profile is fully corroded.
        """
        raise_if_negative(corrosion=corrosion)

        if corrosion == 0:
            return self

        total_width = self.total_width - 2 * corrosion
        total_height = self.total_height - 2 * corrosion

        web_thickness = self.web_thickness - 2 * corrosion
        base_thickness = self.base_thickness - 2 * corrosion
        root_radius = self.root_radius + corrosion
        back_radius = max(self.back_radius - corrosion, 0)
        base_toe_radius = max(self.base_toe_radius - corrosion, 0)
        web_toe_radius = max(self.web_toe_radius - corrosion, 0)

        if any(
            thickness < FULL_CORROSION_TOLERANCE
            for thickness in (
                web_thickness,
                base_thickness,
            )
        ):
            raise ValueError("The profile has fully corroded.")

        name = update_name_with_corrosion(self.name, corrosion=corrosion)

        return LNPProfile(
            total_width=total_width,
            total_height=total_height,
            web_thickness=web_thickness,
            base_thickness=base_thickness,
            root_radius=root_radius,
            back_radius=back_radius,
            web_toe_radius=web_toe_radius,
            base_toe_radius=base_toe_radius,
            name=name,
            plotter=self.plotter,
        )
