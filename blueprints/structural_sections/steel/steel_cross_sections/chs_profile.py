"""Circular Hollow Section (CHS) steel profile."""

from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.cross_section_tube import TubeCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.base import SteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.chs import CHSStandardProfileClass
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
                name="Ring",
                outer_diameter=outer_diameter,
                inner_diameter=outer_diameter - 2 * wall_thickness,
                x=0,
                y=0,
            ),
            steel_material=SteelMaterial(steel_class=steel_class, thickness=wall_thickness),
        )
        self.elements = [SteelElement(cross_section=self.cross_section, material=self.steel_material)]

        self.diameter = outer_diameter
        self.thickness = wall_thickness

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
        return plot_shapes(self.cross_section, centroid=self.centroid, *args, **kwargs)


class CHSProfiles:
    r"""Representation of the strength and deformation characteristics for steel material.

    Parameters
    ----------
    steel_class: SteelStrengthClass
        Enumeration of steel strength classes (default: S355)
    profile: CHSStandardProfileClass
        Enumeration of standard CHS profiles (default: CHS_508x20)
    """

    def __init__(
        self,
        steel_class: SteelStrengthClass = SteelStrengthClass.EN_10025_2_S355,
        profile: CHSStandardProfileClass = CHSStandardProfileClass.CHS_508x20,
    ) -> None:
        self.steel_class = steel_class
        self.profile = profile

    def __str__(self) -> str:
        """Return the steel class and profile."""
        return f"Steel class: {self.steel_class}, Profile: {self.profile}"

    def diameter(self) -> MM:
        """Return the outer diameter of the CHS profile."""
        return float(self.profile.value.split(" ")[1].split("x")[0].replace("_", "."))

    def thickness(self) -> MM:
        """Return the wall thickness of the CHS profile."""
        return float(self.profile.value.split(" ")[1].split("x")[1].replace("_", "."))

    def get_profile(self) -> CHSSteelProfile:
        """Return the CHS profile."""
        return CHSSteelProfile(outer_diameter=self.diameter(), wall_thickness=self.thickness(), steel_class=self.steel_class)

    def get_profile_name(self) -> str:
        """Return the name of the CHS profile."""
        return self.profile.value


if __name__ == "__main__":
    # Define a sample CHS profile
    steel_class = SteelStrengthClass.EN_10025_2_S355
    profile = CHSProfiles(steel_class=steel_class, profile=CHSStandardProfileClass.CHS_508x16)
    profile.get_profile().plot(show=True)
