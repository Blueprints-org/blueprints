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
    top_flange_width : MM
        The width of the top flange [mm].
    top_flange_thickness : MM
        The thickness of the top flange [mm].
    bottom_flange_width : MM
        The width of the bottom flange [mm].
    bottom_flange_thickness : MM
        The thickness of the bottom flange [mm].
    web_height : MM
        The height of the web [mm].
    web_thickness : MM
        The thickness of the web [mm].
    steel_class : SteelStrengthClass
        The steel strength class of the profile.
    radius : MM | None
        The radius of the curved corners of the flanges. Default is None, the corner radius is then taken as the thickness.
    """

    def __init__(
        self,
        top_flange_width: MM,
        top_flange_thickness: MM,
        bottom_flange_width: MM,
        bottom_flange_thickness: MM,
        web_height: MM,
        web_thickness: MM,
        steel_class: SteelStrengthClass,
        radius: MM | None = None,
    ) -> None:
        """Initialize the I-profile steel section."""
        self.top_flange_width = top_flange_width
        self.top_flange_thickness = top_flange_thickness
        self.bottom_flange_width = bottom_flange_width
        self.bottom_flange_thickness = bottom_flange_thickness
        self.web_height = web_height
        self.web_thickness = web_thickness
        self.radius = radius if radius is not None else web_thickness

        # Create the cross-sections for the flanges and web
        self.top_flange = RectangularCrossSection(
            width=top_flange_width,
            height=top_flange_thickness,
            x=0,
            y=(web_height + top_flange_thickness) / 2,
        )
        self.bottom_flange = RectangularCrossSection(
            width=bottom_flange_width,
            height=bottom_flange_thickness,
            x=0,
            y=-(web_height + bottom_flange_thickness) / 2,
        )
        self.web = RectangularCrossSection(
            width=web_thickness,
            height=web_height,
            x=0,
            y=0,
        )

        # Create curves for the corners of the flanges
        self.curve_1 = RightAngleCurvedCrossSection(
            radius=self.radius,
            x=web_thickness / 2,
            y=web_height / 2,
            flipped_horizontally=False,
            flipped_vertically=True,
        )
        self.curve_2 = RightAngleCurvedCrossSection(
            radius=self.radius,
            x=-web_thickness / 2,
            y=web_height / 2,
            flipped_horizontally=True,
            flipped_vertically=True,
        )
        self.curve_3 = RightAngleCurvedCrossSection(
            radius=self.radius,
            x=web_thickness / 2,
            y=-web_height / 2,
            flipped_horizontally=False,
            flipped_vertically=False,
        )
        self.curve_4 = RightAngleCurvedCrossSection(
            radius=self.radius,
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

        # material properties
        material_top_flange = SteelMaterial(steel_class=steel_class, thickness=self.top_flange_thickness)
        material_bottom_flange = SteelMaterial(steel_class=steel_class, thickness=self.bottom_flange_thickness)
        material_web = SteelMaterial(steel_class=steel_class, thickness=self.web_thickness)

        # Create the steel elements
        self.elements = [
            SteelElement(cross_section=self.top_flange, material=material_top_flange, name="Top Flange"),
            SteelElement(cross_section=self.bottom_flange, material=material_bottom_flange, name="Bottom Flange"),
            SteelElement(cross_section=self.web, material=material_web, name="Web"),
            SteelElement(cross_section=self.curve_1, material=material_web, name="Curve 1"),
            SteelElement(cross_section=self.curve_2, material=material_web, name="Curve 2"),
            SteelElement(cross_section=self.curve_3, material=material_web, name="Curve 3"),
            SteelElement(cross_section=self.curve_4, material=material_web, name="Curve 4"),
        ]

        self.steel_material = SteelMaterial(steel_class=steel_class, thickness=max(top_flange_thickness, bottom_flange_thickness, web_thickness))

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
        return plot_shapes(self.top_flange, self.bottom_flange, self.web, self.curve_1, self.curve_2, self.curve_3, self.curve_4, *args, **kwargs)


if __name__ == "__main__":
    # Define a sample I-profile
    steel_class = SteelStrengthClass.EN_10025_2_S355
    profile = ISteelProfile(
        top_flange_width=300,
        top_flange_thickness=36,
        bottom_flange_width=300,
        bottom_flange_thickness=36,
        web_height=1000 - 36 * 2,
        web_thickness=19,
        radius=30,
        steel_class=steel_class,
    )
