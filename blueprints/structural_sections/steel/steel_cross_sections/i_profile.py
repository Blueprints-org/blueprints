"""I-Profile steel section."""

from matplotlib import pyplot as plt
from shapely import Polygon

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.cross_section_radius import RightAngleCurvedCrossSection
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.base import SteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM


class ISteelProfile(SteelCrossSection):
    """Representation of an I-Profile steel section.

    Parameters
    ----------
    flange_width : MM
        The width of the flanges [mm].
    flange_thickness : MM
        The thickness of the flanges [mm].
    web_height : MM
        The height of the web [mm].
    web_thickness : MM
        The thickness of the web [mm].
    steel_class : SteelStrengthClass
        The steel strength class of the profile.
    """

    def __init__(
        self,
        flange_width: MM,
        flange_thickness: MM,
        web_height: MM,
        web_thickness: MM,
        steel_class: SteelStrengthClass,
    ) -> None:
        """Initialize the I-profile steel section."""
        self.flange_width = flange_width
        self.flange_thickness = flange_thickness
        self.web_height = web_height
        self.web_thickness = web_thickness

        # Create the cross-sections for the flanges and web
        self.top_flange = RectangularCrossSection(
            width=flange_width,
            height=flange_thickness,
            x=0,
            y=(web_height + flange_thickness) / 2,
        )
        self.bottom_flange = RectangularCrossSection(
            width=flange_width,
            height=flange_thickness,
            x=0,
            y=-(web_height + flange_thickness) / 2,
        )
        self.web = RectangularCrossSection(
            width=web_thickness,
            height=web_height,
            x=0,
            y=0,
        )

        # Create curves for the corners of the flanges
        self.curve_1 = RightAngleCurvedCrossSection(
            radius=flange_thickness,
            x=web_thickness / 2,
            y=web_height / 2,
            flipped_horizontally=False,
            flipped_vertically=True,
        )
        self.curve_2 = RightAngleCurvedCrossSection(
            radius=flange_thickness,
            x=-web_thickness / 2,
            y=web_height / 2,
            flipped_horizontally=True,
            flipped_vertically=True,
        )
        self.curve_3 = RightAngleCurvedCrossSection(
            radius=flange_thickness,
            x=web_thickness / 2,
            y=-web_height / 2,
            flipped_horizontally=False,
            flipped_vertically=False,
        )
        self.curve_4 = RightAngleCurvedCrossSection(
            radius=flange_thickness,
            x=-web_thickness / 2,
            y=-web_height / 2,
            flipped_horizontally=True,
            flipped_vertically=False,
        )

        # Combine the cross-sections into a single geometry
        self.cross_section = Polygon(
            self.top_flange.geometry.exterior.coords[:]
            + self.web.geometry.exterior.coords[:]
            + self.bottom_flange.geometry.exterior.coords[:]
            + self.curve_1.geometry.exterior.coords[:]
            + self.curve_2.geometry.exterior.coords[:]
            + self.curve_3.geometry.exterior.coords[:]
            + self.curve_4.geometry.exterior.coords[:]
        )

        self.steel_material = SteelMaterial(steel_class=steel_class, thickness=max(flange_thickness, web_thickness))
        self.i_profile = SteelElement(cross_section=self.cross_section, material=self.steel_material, name="I-Profile")

        self.plotter = plot_shapes(self.top_flange, self.bottom_flange, self.web, self.curve_1, self.curve_2, self.curve_3, self.curve_4)

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
        return self.plotter.plot(*args, **kwargs)


if __name__ == "__main__":
    # Define a sample I-profile
    steel_class = SteelStrengthClass.EN_10025_2_S355
    profile = ISteelProfile(
        flange_width=200,
        flange_thickness=20,
        web_height=300,
        web_thickness=10,
        steel_class=steel_class,
    )
