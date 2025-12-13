"""Circular Hollow Section (CHS) profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from math import pi

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

from blueprints.structural_sections._polygon_builder import PolygonBuilder
from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.profile_definitions.plotters.general_steel_plotter import plot_shapes
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


@dataclass(frozen=True, kw_only=True)
class CHSProfile(Profile):
    """Representation of a Circular Hollow Section (CHS) profile.

    Attributes
    ----------
    outer_diameter : MM
        The outer diameter of the CHS profile [mm].
    wall_thickness : MM
        The wall thickness of the CHS profile [mm].
    profile_name : str
        The name of the profile. Default is "CHS Profile".
    plotter : Callable[[Profile], plt.Figure]
        The plotter function to visualize the profile (default: `plot_shapes`).
    """

    outer_diameter: MM
    """ The outer diameter of the CHS profile [mm]. """
    wall_thickness: MM
    """ The wall thickness of the CHS profile [mm]. """
    profile_name: str = "CHS Profile"
    """ The name of the profile. """
    plotter: Callable[[Profile], plt.Figure] = plot_shapes
    """ The plotter function to visualize the profile. """
    inner_diameter: MM = field(init=False)
    """ The inner diameter of the CHS profile [mm]. """

    def __post_init__(self) -> None:
        """Post-process the CHS profile after initialization."""
        object.__setattr__(self, "inner_diameter", self.outer_diameter - 2 * self.wall_thickness)

    @property
    def name(self) -> str:
        """Name of the profile."""
        return self.profile_name

    @property
    def _polygon(self) -> Polygon:
        """Return the polygon of the CHS profile without the offset and rotation applied."""
        max_segment_angle = min(5, 360 / (pi * self.outer_diameter))  # min 1 mm per segment and not less than 5 degrees which is the default
        outer_polygon = (
            PolygonBuilder(starting_point=(0, 0))
            .append_arc(sweep=360, angle=0, radius=self.outer_diameter / 2, max_segment_angle=max_segment_angle)
            .generate_polygon()
        )
        inner_polygon = (
            PolygonBuilder(starting_point=(0, 0))
            .append_arc(sweep=360, angle=0, radius=self.inner_diameter / 2, max_segment_angle=max_segment_angle)
            .generate_polygon()
        )
        return Polygon(shell=outer_polygon.exterior.coords, holes={inner_polygon.exterior.coords})

    def with_corrosion(
        self,
        corrosion_outside: MM = 0,
        corrosion_inside: MM = 0,
    ) -> CHSProfile:
        """Return a new CHSProfile instance adjusted for corrosion.

        Parameters
        ----------
        corrosion_outside : MM, optional
            Corrosion thickness to be subtracted from the outer diameter [mm] (default: 0).
        corrosion_inside : MM, optional
            Corrosion thickness to be added to the inner diameter [mm] (default: 0).

        Returns
        -------
        CHSProfile
            The adjusted CHS profile considering corrosion effects.

        Raises
        ------
        NegativeValueError
            If any of the corrosion values are negative.
        ValueError
            If the resulting wall thickness is less than or equal to zero, indicating full corrosion.
        """
        raise_if_negative(corrosion_outside=corrosion_outside, corrosion_inside=corrosion_inside)
        if corrosion_outside == 0 and corrosion_inside == 0:
            return self

        adjusted_outer_diameter = self.outer_diameter - 2 * corrosion_outside
        adjusted_thickness = self.wall_thickness - corrosion_outside - corrosion_inside

        if adjusted_thickness <= 0:
            raise ValueError("The profile has fully corroded.")

        profile_name = self.profile_name
        profile_name += f" (corrosion inside: {corrosion_inside} mm, corrosion outside: {corrosion_outside} mm)"

        return CHSProfile(
            outer_diameter=adjusted_outer_diameter,
            wall_thickness=adjusted_thickness,
            profile_name=profile_name,
        )
