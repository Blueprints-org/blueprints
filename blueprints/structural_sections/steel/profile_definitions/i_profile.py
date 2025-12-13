"""I-Profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self, overload

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

from blueprints.structural_sections._polygon_builder import PolygonBuilder
from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.profile_definitions.plotters.general_steel_plotter import plot_shapes
from blueprints.type_alias import MM

if TYPE_CHECKING:
    from blueprints.structural_sections.steel.standard_profiles.hea import HEA  # pragma: no cover
    from blueprints.structural_sections.steel.standard_profiles.heb import HEB  # pragma: no cover
    from blueprints.structural_sections.steel.standard_profiles.hem import HEM  # pragma: no cover
    from blueprints.structural_sections.steel.standard_profiles.ipe import IPE  # pragma: no cover


@dataclass(frozen=True, kw_only=True)
class IProfile(Profile):
    """Representation of I-Profile.
    This can be used to create a custom I-profile or to create an I-profile from a standard profile.

    For standard profiles, use the `from_standard_profile` class method.
    For example,
    ```python
    i_profile = IProfile.from_standard_profile(profile=HEA.HEA200)
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

    @overload
    @classmethod
    def from_standard_profile(cls, profile: HEA, corrosion: MM = 0) -> Self: ...

    @overload
    @classmethod
    def from_standard_profile(cls, profile: HEB, corrosion: MM = 0) -> Self: ...

    @overload
    @classmethod
    def from_standard_profile(cls, profile: HEM, corrosion: MM = 0) -> Self: ...

    @overload
    @classmethod
    def from_standard_profile(cls, profile: IPE, corrosion: MM = 0) -> Self: ...

    @classmethod
    def from_standard_profile(
        cls,
        profile: HEA | HEB | HEM | IPE,
        corrosion: MM = 0,
    ) -> Self:
        """Create an I-profile from a set of standard profiles already defined in Blueprints.

        Blueprints offers standard profiles for HEA, HEB, HEM, and IPE. This method allows you to create an I-profile.

        Parameters
        ----------
        profile : HEA | HEB | HEM | IPE
            Any of the standard profiles defined in Blueprints.
        corrosion : MM, optional
            Corrosion thickness per side (default is 0).
        """
        top_flange_width = profile.top_flange_width - corrosion * 2
        top_flange_thickness = profile.top_flange_thickness - corrosion * 2
        bottom_flange_width = profile.bottom_flange_width - corrosion * 2
        bottom_flange_thickness = profile.bottom_flange_thickness - corrosion * 2
        total_height = profile.total_height - corrosion * 2
        web_thickness = profile.web_thickness - corrosion * 2

        if any(
            [
                top_flange_thickness < 1e-3,
                bottom_flange_thickness < 1e-3,
                web_thickness < 1e-3,
            ]
        ):
            raise ValueError("The profile has fully corroded.")

        name = profile.alias
        if corrosion:
            name += f" (corrosion: {corrosion} mm)"

        return cls(
            top_flange_width=top_flange_width,
            top_flange_thickness=top_flange_thickness,
            bottom_flange_width=bottom_flange_width,
            bottom_flange_thickness=bottom_flange_thickness,
            total_height=total_height,
            web_thickness=web_thickness,
            top_radius=profile.top_radius,
            bottom_radius=profile.bottom_radius,
            name=name,
        )
