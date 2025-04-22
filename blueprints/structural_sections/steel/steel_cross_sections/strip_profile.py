"""Steel Strip Profile."""

from matplotlib import pyplot as plt

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import SteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
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
        self.thickness = min(width, height)  # Nominal thickness is the minimum of width and height

        self.strip = RectangularCrossSection(
            name="Steel Strip",
            width=self.width,
            height=self.height,
            x=0,
            y=0,
        )

        self.steel_material = SteelMaterial(steel_class=steel_class)

        self.elements = [SteelElement(cross_section=self.strip, material=self.steel_material, nominal_thickness=self.thickness)]

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


class LoadStandardStrip:
    r"""Class to load in values for standard Strip profile.

    Parameters
    ----------
    steel_class: SteelStrengthClass
        Enumeration of steel strength classes (default: S355)
    profile: Strip
        Enumeration of standard steel strip profiles (default: STRIP160x5)
    """

    def __init__(
        self,
        steel_class: SteelStrengthClass = SteelStrengthClass.S355,
        profile: Strip = Strip.STRIP160x5,
    ) -> None:
        self.steel_class = steel_class
        self.profile = profile

    def __str__(self) -> str:
        """Return the steel class and profile."""
        return f"Steel class: {self.steel_class}, Profile: {self.profile}"

    def alias(self) -> str:
        """Return the code of the strip profile."""
        return self.profile.alias

    def width(self) -> MM:
        """Return the width of the strip profile."""
        return self.profile.width

    def height(self) -> MM:
        """Return the height (thickness) of the strip profile."""
        return self.profile.height

    def get_profile(self, corrosion: MM = 0) -> StripSteelProfile:
        """Return the strip profile.

        Parameters
        ----------
        corrosion : MM, optional
            Corrosion thickness per side (default is 0).
        """
        width = self.width() - corrosion * 2
        height = self.height() - corrosion * 2
        return StripSteelProfile(width=width, height=height, steel_class=self.steel_class)
