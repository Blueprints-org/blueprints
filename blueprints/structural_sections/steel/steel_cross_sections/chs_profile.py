"""Circular Hollow Section (CHS) steel profile."""

from matplotlib import pyplot as plt

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.cross_section_tube import TubeCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import SteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHS
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM


class CHSSteelProfile(SteelCrossSection):
    """Representation of a Circular Hollow Section (CHS) steel profile.

    Parameters
    ----------
    outer_diameter : MM
        The outer diameter of the CHS profile [mm].
    wall_thickness : MM
        The wall thickness of the CHS profile [mm].
    steel_class : SteelStrengthClass
        The steel strength class of the profile.
    """

    def __init__(
        self,
        outer_diameter: MM,
        wall_thickness: MM,
        steel_class: SteelStrengthClass,
    ) -> None:
        """Initialize the CHS steel profile."""
        self.thickness = wall_thickness
        self.outer_diameter = outer_diameter
        self.inner_diameter = outer_diameter - 2 * wall_thickness

        self.chs = TubeCrossSection(
            name="Ring",
            outer_diameter=self.outer_diameter,
            inner_diameter=self.inner_diameter,
            x=0,
            y=0,
        )
        self.steel_material = SteelMaterial(steel_class=steel_class)
        self.elements = [SteelElement(cross_section=self.chs, material=self.steel_material, nominal_thickness=self.thickness)]

    def plot(self, *args, **kwargs) -> plt.Figure:
        """Plot the cross-section. Making use of the standard plotter.

        Parameters
        ----------
        *args
            Additional arguments passed to the plotter.
        **kwargs
            Additional keyword arguments passed to the plotter.
        """
        return plot_shapes(
            self,
            *args,
            **kwargs,
        )


class LoadStandardCHS:
    r"""Class to load in values for standard CHS profile.

    Parameters
    ----------
    steel_class: SteelStrengthClass
        Enumeration of steel strength classes (default: S355)
    profile: CHS
        Enumeration of standard CHS profiles (default: CHS508x20)
    """

    def __init__(
        self,
        steel_class: SteelStrengthClass = SteelStrengthClass.S355,
        profile: CHS = CHS.CHS508x20,
    ) -> None:
        self.steel_class = steel_class
        self.profile = profile

    def __str__(self) -> str:
        """Return the steel class and profile."""
        return f"Steel class: {self.steel_class}, Profile: {self.profile}"

    def alias(self) -> str:
        """Return the alias of the CHS profile."""
        return self.profile.alias

    def diameter(self) -> MM:
        """Return the outer diameter of the CHS profile."""
        return self.profile.diameter

    def thickness(self) -> MM:
        """Return the wall thickness of the CHS profile."""
        return self.profile.thickness

    def get_profile(self, corrosion_outside: MM = 0, corrosion_inside: MM = 0) -> CHSSteelProfile:
        """Return the CHS profile with optional corrosion adjustments.

        Parameters
        ----------
        corrosion_outside : MM, optional
            Corrosion thickness to be subtracted from the outer diameter [mm] (default: 0).
        corrosion_inside : MM, optional
            Corrosion thickness to be added to the inner diameter [mm] (default: 0).

        Returns
        -------
        CHSSteelProfile
            The adjusted CHS steel profile considering corrosion effects.
        """
        adjusted_outer_diameter = self.diameter() - 2 * corrosion_outside
        adjusted_thickness = self.thickness() - corrosion_outside - corrosion_inside

        if adjusted_thickness <= 0:
            raise ValueError("Adjusted wall thickness must be greater than zero.")

        return CHSSteelProfile(
            outer_diameter=adjusted_outer_diameter,
            wall_thickness=adjusted_thickness,
            steel_class=self.steel_class,
        )
