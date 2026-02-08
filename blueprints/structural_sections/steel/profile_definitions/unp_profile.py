"""UNP-Profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import Polygon

from blueprints.structural_sections._polygon_builder import PolygonBuilder
from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.profile_definitions.corrosion_utils import FULL_CORROSION_TOLERANCE, update_name_with_corrosion
from blueprints.structural_sections.steel.profile_definitions.plotters.general_steel_plotter import plot_shapes
from blueprints.type_alias import MM, PERCENTAGE
from blueprints.utils.math_helpers import slope_to_angle
from blueprints.validations import raise_if_negative


@dataclass(frozen=True, kw_only=True)
class UNPProfile(Profile):
    """Representation of U/C shaped profiles.

    For standard profiles, use the specific standard profile class like `UNP`. For example,
    ```python
    unp_profile = UNP.UNP200
    ```

    Attributes
    ----------
    top_flange_total_width : MM
        The total width of the top flange, measured halfway the total width of the element [mm].
    top_flange_thickness : MM
        The thickness of the top flange [mm].
    bottom_flange_total_width : MM
        The total width of the bottom flange, measured halfway the total width of the element [mm].
    bottom_flange_thickness : MM
        The thickness of the bottom flange [mm].
    total_height : MM
        The total height of the profile [mm].
    web_thickness : MM
        The thickness of the web [mm].
    top_root_fillet_radius : MM
        The radius of the curved corners of the top flange. Default is 0, meaning sharp corner.
    top_toe_radius : MM
        The radius of the outer corners of the top flange. Default is 0, meaning sharp corner.
    top_outer_corner_radius : MM
        The radius of the outer corners of the top flange. Default is 0, meaning sharp corner.
    bottom_root_fillet_radius : MM
        The radius of the curved corners of the bottom flange. Default is 0, meaning sharp corner.
    bottom_toe_radius : MM
        The radius of the outer corners of the bottom flange. Default is 0, meaning sharp corner.
    bottom_outer_corner_radius : MM
        The radius of the outer corners of the bottom flange. Default is 0, meaning sharp corner.
    top_slope : PERCENTAGE
        The slope of the top flange. Default is 0.
    bottom_slope : PERCENTAGE
        The slope of the bottom flange. Default is 0.
    name : str
        The name of the profile. Default is "UNP-Profile". If corrosion is applied, the name will include the corrosion value.
    plotter : Callable[[Profile], plt.Figure]
        The plotter function to visualize the profile (default: `plot_shapes`).
    """

    top_flange_total_width: MM
    """The total width of the top flange [mm]."""
    top_flange_thickness: MM
    """The thickness of the top flange [mm]."""
    bottom_flange_total_width: MM
    """The total width of the bottom flange [mm]."""
    bottom_flange_thickness: MM
    """The thickness of the bottom flange [mm]."""
    total_height: MM
    """The total height of the profile [mm]."""
    web_thickness: MM
    """The thickness of the web [mm]."""
    top_root_fillet_radius: MM = 0.0
    """The radius of the curved corners of the top flange. Default is 0, meaning sharp corner."""
    top_toe_radius: MM = 0.0
    """The radius of the outer corners of the top flange. Default is 0, meaning sharp corner."""
    top_outer_corner_radius: MM = 0.0
    """The radius of the outer corners of the top flange. Default is 0, meaning sharp corner."""
    bottom_root_fillet_radius: MM = 0.0
    """The radius of the curved corners of the bottom flange. Default is 0, meaning sharp corner."""
    bottom_toe_radius: MM = 0.0
    """The radius of the outer corners of the bottom flange. Default is 0, meaning sharp corner."""
    bottom_outer_corner_radius: MM = 0.0
    """The radius of the outer corners of the bottom flange. Default is 0, meaning sharp corner."""
    top_slope: PERCENTAGE = 0.0
    """The slope of the top flange. Default is 0."""
    bottom_slope: PERCENTAGE = 0.0
    """The slope of the bottom flange. Default is 0."""
    name: str = "UNP-Profile"
    """The name of the profile. Default is "UNP-Profile". If corrosion is applied, the name will include the corrosion value."""
    plotter: Callable[[Profile], plt.Figure] = plot_shapes
    """The plotter function to visualize the profile (default: `plot_shapes`)."""

    # Attributes set in __post_init__ (for type checkers)
    top_root_fillet_height: float = field(init=False, repr=False)
    top_root_fillet_width: float = field(init=False, repr=False)
    bottom_root_fillet_height: float = field(init=False, repr=False)
    bottom_root_fillet_width: float = field(init=False, repr=False)
    top_toe_radius_height: float = field(init=False, repr=False)
    top_toe_radius_width: float = field(init=False, repr=False)
    bottom_toe_radius_height: float = field(init=False, repr=False)
    bottom_toe_radius_width: float = field(init=False, repr=False)
    top_slope_width: float = field(init=False, repr=False)
    top_slope_height: float = field(init=False, repr=False)
    top_slope_length: float = field(init=False, repr=False)
    bottom_slope_width: float = field(init=False, repr=False)
    bottom_slope_height: float = field(init=False, repr=False)
    bottom_slope_length: float = field(init=False, repr=False)
    top_toe_total_height: float = field(init=False, repr=False)
    top_toe_flat_height: float = field(init=False, repr=False)
    bottom_toe_total_height: float = field(init=False, repr=False)
    bottom_toe_flat_height: float = field(init=False, repr=False)
    web_inner_height_top: float = field(init=False, repr=False)
    web_inner_height_bottom: float = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Post-initialization: calculate corner and slope parameters for the UNP profile."""
        object.__setattr__(self, "top_root_fillet_height", np.cos(np.deg2rad(slope_to_angle(self.top_slope))) * self.top_root_fillet_radius)
        object.__setattr__(self, "top_root_fillet_width", (1 - np.sin(np.deg2rad(slope_to_angle(self.top_slope)))) * self.top_root_fillet_radius)

        object.__setattr__(self, "bottom_root_fillet_height", np.cos(np.deg2rad(slope_to_angle(self.bottom_slope))) * self.bottom_root_fillet_radius)
        object.__setattr__(
            self, "bottom_root_fillet_width", (1 - np.sin(np.deg2rad(slope_to_angle(self.bottom_slope)))) * self.bottom_root_fillet_radius
        )

        object.__setattr__(self, "top_toe_radius_height", np.cos(np.deg2rad(slope_to_angle(self.top_slope))) * self.top_toe_radius)
        object.__setattr__(self, "top_toe_radius_width", (1 - np.sin(np.deg2rad(slope_to_angle(self.top_slope)))) * self.top_toe_radius)

        object.__setattr__(self, "bottom_toe_radius_height", np.cos(np.deg2rad(slope_to_angle(self.bottom_slope))) * self.bottom_toe_radius)
        object.__setattr__(self, "bottom_toe_radius_width", (1 - np.sin(np.deg2rad(slope_to_angle(self.bottom_slope)))) * self.bottom_toe_radius)

        object.__setattr__(
            self, "top_slope_width", self.top_flange_total_width - self.web_thickness - self.top_root_fillet_width - self.top_toe_radius_width
        )
        object.__setattr__(self, "top_slope_height", np.tan(np.deg2rad(slope_to_angle(self.top_slope))) * self.top_slope_width)
        object.__setattr__(self, "top_slope_length", np.sqrt(self.top_slope_width**2 + self.top_slope_height**2))

        object.__setattr__(
            self,
            "bottom_slope_width",
            self.bottom_flange_total_width - self.web_thickness - self.bottom_root_fillet_width - self.bottom_toe_radius_width,
        )
        object.__setattr__(self, "bottom_slope_height", np.tan(np.deg2rad(slope_to_angle(self.bottom_slope))) * self.bottom_slope_width)
        object.__setattr__(self, "bottom_slope_length", np.sqrt(self.bottom_slope_width**2 + self.bottom_slope_height**2))

        object.__setattr__(
            self,
            "top_toe_total_height",
            self.top_flange_thickness - (self.top_flange_total_width / 2 - self.top_toe_radius_width) * self.top_slope / 100,
        )
        object.__setattr__(self, "top_toe_flat_height", self.top_toe_total_height - self.top_toe_radius_height)

        object.__setattr__(
            self,
            "bottom_toe_total_height",
            self.bottom_flange_thickness - (self.bottom_flange_total_width / 2 - self.bottom_toe_radius_width) * self.bottom_slope / 100,
        )
        object.__setattr__(self, "bottom_toe_flat_height", self.bottom_toe_total_height - self.bottom_toe_radius_height)

        object.__setattr__(
            self, "web_inner_height_top", self.total_height / 2 - self.top_toe_total_height - self.top_slope_height - self.top_root_fillet_height
        )
        object.__setattr__(
            self,
            "web_inner_height_bottom",
            self.total_height / 2 - self.bottom_toe_total_height - self.bottom_slope_height - self.bottom_root_fillet_height,
        )

        raise_if_negative(
            top_slope=self.top_slope,
            bottom_slope=self.bottom_slope,
            top_root_fillet_height=self.top_root_fillet_height,
            top_root_fillet_width=self.top_root_fillet_width,
            bottom_root_fillet_height=self.bottom_root_fillet_height,
            bottom_root_fillet_width=self.bottom_root_fillet_width,
            top_toe_radius_height=self.top_toe_radius_height,
            top_toe_radius_width=self.top_toe_radius_width,
            bottom_toe_radius_height=self.bottom_toe_radius_height,
            bottom_toe_radius_width=self.bottom_toe_radius_width,
            top_slope_width=self.top_slope_width,
            top_slope_height=self.top_slope_height,
            top_slope_length=self.top_slope_length,
            bottom_slope_width=self.bottom_slope_width,
            bottom_slope_height=self.bottom_slope_height,
            bottom_slope_length=self.bottom_slope_length,
            top_toe_total_height=self.top_toe_total_height,
            top_toe_flat_height=self.top_toe_flat_height,
            bottom_toe_total_height=self.bottom_toe_total_height,
            bottom_toe_flat_height=self.bottom_toe_flat_height,
            web_inner_height_top=self.web_inner_height_top,
            web_inner_height_bottom=self.web_inner_height_bottom,
        )

    @property
    def max_profile_thickness(self) -> MM:
        """Maximum element thickness of the profile [mm]."""
        return max(self.top_flange_thickness, self.bottom_flange_thickness, self.web_thickness)

    @property
    def _polygon(self) -> Polygon:
        """Return the polygon of the UNP profile without the offset and rotation applied."""
        return (
            PolygonBuilder(starting_point=(0, 0))
            # Starting halfway along the web, going up
            .append_line(length=self.total_height / 2 - self.top_outer_corner_radius, angle=90)
            # Top flange
            .append_arc(sweep=-90, angle=90, radius=self.top_outer_corner_radius)
            .append_line(length=self.top_flange_total_width - self.top_outer_corner_radius, angle=0)
            .append_line(length=self.top_toe_flat_height, angle=270)
            .append_arc(sweep=-90 + slope_to_angle(self.top_slope), angle=270, radius=self.top_toe_radius)
            .append_line(length=self.top_slope_length, angle=180 + slope_to_angle(self.top_slope))
            .append_arc(sweep=90 - slope_to_angle(self.top_slope), angle=180 + slope_to_angle(self.top_slope), radius=self.top_root_fillet_radius)
            # Going down the web
            .append_line(length=self.web_inner_height_top, angle=270)
            .append_line(length=self.web_inner_height_bottom, angle=270)
            # Bottom flange
            .append_arc(sweep=90 - slope_to_angle(self.bottom_slope), angle=270, radius=self.bottom_root_fillet_radius)
            .append_line(length=self.bottom_slope_length, angle=-slope_to_angle(self.bottom_slope))
            .append_arc(sweep=-90 + slope_to_angle(self.bottom_slope), angle=-slope_to_angle(self.bottom_slope), radius=self.bottom_toe_radius)
            .append_line(length=self.bottom_toe_flat_height, angle=270)
            .append_line(length=self.bottom_flange_total_width - self.bottom_outer_corner_radius, angle=180)
            .append_arc(sweep=-90, angle=180, radius=self.bottom_outer_corner_radius)
            # Closing the profile
            .append_line(length=self.total_height / 2 - self.bottom_outer_corner_radius, angle=90)
            .generate_polygon()
        )

    def with_corrosion(self, corrosion: MM = 0) -> UNPProfile:
        """Apply corrosion to the UNP-profile and return a new UNP-profile instance.

        The name attribute of the new instance will be updated to reflect the total corrosion applied
        including any previous corrosion indicated in the original name.

        Parameters
        ----------
        corrosion : MM, optional
            Corrosion per side (default is 0).

        Returns
        -------
        UNPProfile
            A new UNP-profile instance with the applied corrosion.

        Raises
        ------
        ValueError
            If the profile has fully corroded.
        """
        raise_if_negative(corrosion=corrosion)

        if corrosion == 0:
            return self

        # Use a buffer dict to store updated dimensions
        buffer = {
            "top_flange_total_width": self.top_flange_total_width - 2 * corrosion,
            "top_flange_thickness": self.top_flange_thickness - 2 * corrosion,
            "bottom_flange_total_width": self.bottom_flange_total_width - 2 * corrosion,
            "bottom_flange_thickness": self.bottom_flange_thickness - 2 * corrosion,
            "total_height": self.total_height - 2 * corrosion,
            "web_thickness": self.web_thickness - 2 * corrosion,
            "top_root_fillet_radius": self.top_root_fillet_radius + corrosion,
            "top_toe_radius": max(0, self.top_toe_radius - corrosion),
            "top_outer_corner_radius": max(0, self.top_outer_corner_radius - corrosion),
            "bottom_root_fillet_radius": self.bottom_root_fillet_radius + corrosion,
            "bottom_toe_radius": max(0, self.bottom_toe_radius - corrosion),
            "bottom_outer_corner_radius": max(0, self.bottom_outer_corner_radius - corrosion),
        }

        if any(
            buffer[thickness] < FULL_CORROSION_TOLERANCE
            for thickness in (
                "top_flange_thickness",
                "bottom_flange_thickness",
                "web_thickness",
            )
        ):
            raise ValueError("The profile has fully corroded.")

        name = update_name_with_corrosion(self.name, corrosion=corrosion)

        return UNPProfile(
            top_flange_total_width=buffer["top_flange_total_width"],
            top_flange_thickness=buffer["top_flange_thickness"],
            bottom_flange_total_width=buffer["bottom_flange_total_width"],
            bottom_flange_thickness=buffer["bottom_flange_thickness"],
            total_height=buffer["total_height"],
            web_thickness=buffer["web_thickness"],
            top_root_fillet_radius=buffer["top_root_fillet_radius"],
            top_toe_radius=buffer["top_toe_radius"],
            top_outer_corner_radius=buffer["top_outer_corner_radius"],
            bottom_root_fillet_radius=buffer["bottom_root_fillet_radius"],
            bottom_toe_radius=buffer["bottom_toe_radius"],
            bottom_outer_corner_radius=buffer["bottom_outer_corner_radius"],
            top_slope=self.top_slope,
            bottom_slope=self.bottom_slope,
            name=name,
            plotter=self.plotter,
        )
