"""Steel Strip Profile."""

from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.base import SteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import StripStandardProfileClass
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM


class StripSteelProfile(SteelCrossSection):
    """Representation of a Steel Strip profile.

    Parameters
    ----------
    width : MM
        The width of the strip profile [mm].
    height : MM
        The height (thickness) of the strip profile [mm].
    steel_class : SteelStrengthClass
        The steel strength class of the profile.
    """

    def __init__(
        self,
        width: MM,
        height: MM,
        steel_class: SteelStrengthClass,
    ) -> None:
        """Initialize the Steel Strip profile."""
        self.width = width
        self.height = height

        self.strip = RectangularCrossSection(
            name="Steel Strip",
            width=self.width,
            height=self.height,
            x=0,
            y=0,
        )

        self.steel_material = SteelMaterial(steel_class=steel_class)
        self.elements = [SteelElement(cross_section=self.strip, material=self.steel_material)]

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
        return plot_shapes(self.strip, centroid=self.centroid, *args, **kwargs)


class StripProfiles:
    r"""Representation of the strength and deformation characteristics for steel material.

    Parameters
    ----------
    steel_class: SteelStrengthClass
        Enumeration of steel strength classes (default: S355)
    profile: StripStandardProfileClass
        Enumeration of standard steel strip profiles (default: STRIP_160x5)
    """

    def __init__(
        self,
        steel_class: SteelStrengthClass = SteelStrengthClass.EN_10025_2_S355,
        profile: StripStandardProfileClass = StripStandardProfileClass.STRIP_160x5,
    ) -> None:
        self.steel_class = steel_class
        self.profile = profile

    def __str__(self) -> str:
        """Return the steel class and profile."""
        return f"Steel class: {self.steel_class}, Profile: {self.profile}"

    def code(self) -> str:
        """Return the code of the strip profile."""
        return self.profile.code

    def width(self) -> MM:
        """Return the width of the strip profile."""
        return self.profile.width

    def height(self) -> MM:
        """Return the height (thickness) of the strip profile."""
        return self.profile.height

    def get_profile(self) -> StripSteelProfile:
        """Return the strip profile."""
        return StripSteelProfile(width=self.width(), height=self.height(), steel_class=self.steel_class)


if __name__ == "__main__":
    steel_class = SteelStrengthClass.EN_10025_2_S355
    profile = StripProfiles(steel_class=steel_class, profile=StripStandardProfileClass.STRIP_160x5)
    profile.get_profile().plot(show=True)
