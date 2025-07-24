"""Circular Hollow Section (CHS) steel profile."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.cross_section_tube import TubeCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM


@dataclass(kw_only=True)
class CHSSteelProfile(CombinedSteelCrossSection):
    """Representation of a Circular Hollow Section (CHS) steel profile.

    Attributes
    ----------
    steel_material : SteelMaterial
        The material properties of the steel.
    outer_diameter : MM
        The outer diameter of the CHS profile [mm].
    wall_thickness : MM
        The wall thickness of the CHS profile [mm].
    """

    steel_material: SteelMaterial
    outer_diameter: MM
    wall_thickness: MM

    def __post_init__(self) -> None:
        """Initialize the CHS profile."""
        self.inner_diameter = self.outer_diameter - 2 * self.wall_thickness

        self.chs = TubeCrossSection(
            name="Ring",
            outer_diameter=self.outer_diameter,
            inner_diameter=self.inner_diameter,
            x=0,
            y=0,
        )
        self.elements = [
            SteelElement(
                cross_section=self.chs,
                material=self.steel_material,
                nominal_thickness=self.wall_thickness,
            )
        ]

    @classmethod
    def from_standard_profile(
        cls,
        profile: CHS,
        steel_material: SteelMaterial,
        corrosion_outside: MM = 0,
        corrosion_inside: MM = 0,
    ) -> Self:
        """Create a CHS profile from a set of standard profiles already defined in Blueprints.

        Parameters
        ----------
        profile : CHS
            Any of the standard CHS profiles defined in Blueprints.
        steel_material : SteelMaterial
            Steel material properties for the profile.
        corrosion_outside : MM, optional
            Corrosion thickness to be subtracted from the outer diameter [mm] (default: 0).
        corrosion_inside : MM, optional
            Corrosion thickness to be added to the inner diameter [mm] (default: 0).

        Returns
        -------
        CHSSteelProfile
            The adjusted CHS steel profile considering corrosion effects.
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
            steel_material=steel_material,
            name=name,
        )

    def plot(self, plotter: Callable[[CombinedSteelCrossSection], plt.Figure] | None = None, *args, **kwargs) -> plt.Figure:
        """Plot the cross-section. Making use of the standard plotter.

        Parameters
        ----------
        plotter : Callable[CombinedSteelCrossSection, plt.Figure] | None
            The plotter function to use. If None, the default Blueprints plotter for steel sections is used.
        *args
            Additional arguments passed to the plotter.
        **kwargs
            Additional keyword arguments passed to the plotter.
        """
        if plotter is None:
            plotter = plot_shapes
        return plotter(
            self,
            *args,
            **kwargs,
        )
