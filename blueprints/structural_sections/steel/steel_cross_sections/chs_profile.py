"""Circular Hollow Section (CHS) profile."""

from collections.abc import Callable
from dataclasses import dataclass
from math import pi
from typing import Self

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.structural_sections._polygon_builder import PolygonBuilder
from blueprints.structural_sections.cross_section_tube import TubeCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.type_alias import MM


@dataclass(kw_only=True)
class CHSProfile(CrossSection):
    """Representation of a Circular Hollow Section (CHS) profile.

    Attributes
    ----------
    outer_diameter : MM
        The outer diameter of the CHS profile [mm].
    wall_thickness : MM
        The wall thickness of the CHS profile [mm].
    name : str
        The name of the profile. Default is "CHS Profile".
    plotter : Callable[[CrossSection], plt.Figure]
        The plotter function to visualize the cross-section (default: `plot_shapes`).
    """

    outer_diameter: MM
    """ The outer diameter of the CHS profile [mm]. """
    wall_thickness: MM
    """ The wall thickness of the CHS profile [mm]. """
    name: str = "CHS Profile"
    """ The name of the profile. """
    plotter: Callable[[CrossSection], plt.Figure] = plot_shapes
    """ The plotter function to visualize the cross-section. """

    def __post_init__(self) -> None:
        """Post-process the CHS profile after initialization."""
        self.inner_diameter = self.outer_diameter - 2 * self.wall_thickness

        self.chs = TubeCrossSection(
            name="Ring",
            outer_diameter=self.outer_diameter,
            inner_diameter=self.inner_diameter,
            x=0,
            y=0,
        )
        self.elements = [self.chs]

    @property
    def polygon(self) -> Polygon:
        """Return the polygon of the CHS profile section."""
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

    @classmethod
    def from_standard_profile(
        cls,
        profile: CHS,
        corrosion_outside: MM = 0,
        corrosion_inside: MM = 0,
    ) -> Self:
        """Create a CHS profile from a set of standard profiles already defined in Blueprints.

        Parameters
        ----------
        profile : CHS
            Any of the standard CHS profiles defined in Blueprints.
        corrosion_outside : MM, optional
            Corrosion thickness to be subtracted from the outer diameter [mm] (default: 0).
        corrosion_inside : MM, optional
            Corrosion thickness to be added to the inner diameter [mm] (default: 0).

        Returns
        -------
        CHSSteelProfile
            The adjusted CHS profile considering corrosion effects.
        """
        adjusted_outer_diameter = profile.diameter - 2 * corrosion_outside
        adjusted_thickness = profile.thickness - corrosion_outside - corrosion_inside

        if adjusted_thickness <= 0:
            raise ValueError("The profile has fully corroded.")

        name = profile.alias
        if corrosion_inside or corrosion_outside:
            name += (
                f" (corrosion {'' if not corrosion_inside else f'in: {corrosion_inside} mm'}"
                f"{', ' if corrosion_inside and corrosion_outside else ''}"
                f"{'' if not corrosion_outside else f'out: {corrosion_outside} mm'})"
            )

        return cls(
            outer_diameter=adjusted_outer_diameter,
            wall_thickness=adjusted_thickness,
            name=name,
        )
