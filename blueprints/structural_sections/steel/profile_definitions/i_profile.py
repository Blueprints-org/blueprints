"""I-Profile."""

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
class IProfile(Profile):
    """Representation of I shaped profiles.

    For standard profiles, use the specific standard profile class like `HEA`, `HEB`, `HEM` or `IPE`.
    For example,
    ```python
    hea_profile = HEA.HEA200
    ```

    Attributes
    ----------
    top_flange_width : MM
        The width of the top flange [mm].
    top_flange_thickness : MM
        The thickness of the top flange [mm].
    bottom_flange_width : MM
        The width of the bottom flange [mm].
    bottom_flange_thickness : MM
        The thickness of the bottom flange [mm].
    total_height : MM
        The total height of the profile [mm].
    web_thickness : MM
        The thickness of the web [mm].
    top_radius : MM
        The radius of the curved corners of the top flange.
    bottom_radius : MM
        The radius of the curved corners of the bottom flange.
    name : str
        The name of the profile. Default is "I-Profile". If corrosion is applied, the name will include the corrosion value.
    plotter : Callable[[Profile], plt.Figure]
        The plotter function to visualize the profile (default: `plot_shapes`).
    """

    top_flange_width: MM
    """ The width of the top flange [mm]. """
    top_flange_thickness: MM
    """ The thickness of the top flange [mm]. """
    bottom_flange_width: MM
    """ The width of the bottom flange [mm]. """
    bottom_flange_thickness: MM
    """ The thickness of the bottom flange [mm]. """
    total_height: MM
    """ The total height of the profile [mm]. """
    web_thickness: MM
    """ The thickness of the web [mm]. """
    top_radius: MM
    """ The radius of the curved corners of the top flange [mm]. """
    bottom_radius: MM
    """ The radius of the curved corners of the bottom flange [mm]. """
    name: str = "I-Profile"
    """ The name of the profile. Default is "I-Profile". If corrosion is applied, the name will include the corrosion value. """
    plotter: Callable[[Profile], plt.Figure] = plot_shapes
    """ The plotter function to visualize the profile (default: `plot_shapes`). """
    web_height: MM = field(init=False)
    """ The height of the web [mm]. """
    width_outstand_top_flange: MM = field(init=False)
    """ The width of the outstand of the top flange [mm]. """
    width_outstand_bottom_flange: MM = field(init=False)
    """ The width of the outstand of the bottom flange [mm]. """

    def __post_init__(self) -> None:
        """Post-process the I-profile after initialization."""
        object.__setattr__(
            self, "web_height", self.total_height - self.top_flange_thickness - self.bottom_flange_thickness - self.top_radius - self.bottom_radius
        )
        object.__setattr__(self, "width_outstand_top_flange", (self.top_flange_width - self.web_thickness - 2 * self.top_radius) / 2)
        object.__setattr__(self, "width_outstand_bottom_flange", (self.bottom_flange_width - self.web_thickness - 2 * self.bottom_radius) / 2)

    @property
    def max_profile_thickness(self) -> MM:
        """Maximum element thickness of the profile [mm]."""
        return max(self.top_flange_thickness, self.bottom_flange_thickness, self.web_thickness)

    @property
    def _polygon(self) -> Polygon:
        """Return the polygon of the I-profile without the offset and rotation applied."""
        return (
            # Start from top left corner and go clockwise
            PolygonBuilder(starting_point=(0, 0))
            # Top flange
            .append_line(length=self.top_flange_width, angle=0)
            .append_line(length=self.top_flange_thickness, angle=270)
            .append_line(length=self.width_outstand_top_flange, angle=180)
            .append_arc(sweep=90, angle=180, radius=self.top_radius)
            # Web
            .append_line(length=self.web_height, angle=270)
            # Bottom flange
            .append_arc(sweep=90, angle=270, radius=self.bottom_radius)
            .append_line(length=self.width_outstand_bottom_flange, angle=0)
            .append_line(length=self.bottom_flange_thickness, angle=270)
            .append_line(length=self.bottom_flange_width, angle=180)
            .append_line(length=self.bottom_flange_thickness, angle=90)
            .append_line(length=self.width_outstand_bottom_flange, angle=0)
            .append_arc(sweep=90, angle=0, radius=self.bottom_radius)
            # Web
            .append_line(length=self.web_height, angle=90)
            # Top flange
            .append_arc(sweep=90, angle=90, radius=self.top_radius)
            .append_line(length=self.width_outstand_top_flange, angle=180)
            .append_line(length=self.top_flange_thickness, angle=90)
            .generate_polygon()
        )

    def with_corrosion(self, corrosion: MM = 0) -> IProfile:
        """Apply corrosion to the I-profile and return a new I-profile instance.

        The name attribute of the new instance will be updated to reflect the total corrosion applied
        including any previous corrosion indicated in the original name.

        Parameters
        ----------
        corrosion : MM, optional
            Corrosion per side (default is 0).

        Returns
        -------
        IProfile
            A new I-profile instance with the applied corrosion.

        Raises
        ------
        ValueError
            If the profile has fully corroded.
        """
        raise_if_negative(corrosion=corrosion)

        if corrosion == 0:
            return self

        top_flange_width = self.top_flange_width - corrosion * 2
        top_flange_thickness = self.top_flange_thickness - corrosion * 2
        bottom_flange_width = self.bottom_flange_width - corrosion * 2
        bottom_flange_thickness = self.bottom_flange_thickness - corrosion * 2
        total_height = self.total_height - corrosion * 2
        web_thickness = self.web_thickness - corrosion * 2
        top_radius = self.top_radius + corrosion
        bottom_radius = self.bottom_radius + corrosion

        if any(
            thickness < FULL_CORROSION_TOLERANCE
            for thickness in (
                top_flange_thickness,
                bottom_flange_thickness,
                web_thickness,
            )
        ):
            raise ValueError("The profile has fully corroded.")

        name = update_name_with_corrosion(self.name, corrosion=corrosion)

        return IProfile(
            top_flange_width=top_flange_width,
            top_flange_thickness=top_flange_thickness,
            bottom_flange_width=bottom_flange_width,
            bottom_flange_thickness=bottom_flange_thickness,
            total_height=total_height,
            web_thickness=web_thickness,
            top_radius=top_radius,
            bottom_radius=bottom_radius,
            name=name,
            plotter=self.plotter,
        )
