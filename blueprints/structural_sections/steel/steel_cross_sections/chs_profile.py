"""Circular Hollow Section (CHS) steel profile."""

from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.cross_section_tube import TubeCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.base import SteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
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
        super().__init__(
            cross_section=TubeCrossSection(
                outer_diameter=outer_diameter,
                inner_diameter=outer_diameter - 2 * wall_thickness,
                x=0,
                y=0,
            ),
            steel_material=SteelMaterial(steel_class=steel_class, thickness=wall_thickness),
        )
        self.chs = SteelElement(cross_section=self.cross_section, material=self.steel_material, name="CHS")

        self.diameter = outer_diameter
        self.thickness = wall_thickness
        self.plotter = plot_shapes(self.chs)

    def plot(self, *args, **kwargs) -> plt.Figure:
        """Plot the cross-section. Making use of the standard plotter.

        If you want to use a custom plotter, use the .plotter attribute to plot the cross-section.

        Parameters
        ----------
        *args
            Additional arguments passed to the plotter.
        **kwargs
            Additional keyword arguments passed to the plotter.
        """
        return self.plotter.plot(*args, **kwargs, title="CHS Profile Cross Section", show=False)


if __name__ == "__main__":
    # Define a sample CHS profile
    steel_class = SteelStrengthClass.EN_10025_2_S355
    profile = CHSSteelProfile(outer_diameter=1000, wall_thickness=41, steel_class=steel_class)
