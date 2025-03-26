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
    total_height : MM
        The total height of the profile [mm].
    web_thickness : MM
        The thickness of the web [mm].
    steel_class : SteelStrengthClass
        The steel strength class of the profile.
    radius_top : MM | None
        The radius of the curved corners of the top flange. Default is None, the corner radius is then taken as the thickness.
    radius_bottom : MM | None
        The radius of the curved corners of the bottom flange. Default is None, the corner radius is then taken as the thickness.
    """

    def __init__(
        self,
        top_flange_width: MM,
        top_flange_thickness: MM,
        bottom_flange_width: MM,
        bottom_flange_thickness: MM,
        total_height: MM,
        web_thickness: MM,
        steel_class: SteelStrengthClass,
        radius_top: MM | None = None,
        radius_bottom: MM | None = None,
    ) -> None:
        """Initialize the I-profile steel section."""
        self.top_flange_width = top_flange_width
        self.top_flange_thickness = top_flange_thickness
        self.bottom_flange_width = bottom_flange_width
        self.bottom_flange_thickness = bottom_flange_thickness
        self.total_height = total_height
        self.web_thickness = web_thickness
        self.radius_top = radius_top if radius_top is not None else top_flange_thickness
        self.radius_bottom = radius_bottom if radius_bottom is not None else bottom_flange_thickness

        # Calculate web height
        self.web_height = total_height - top_flange_thickness - bottom_flange_thickness

        # Create the cross-sections for the flanges and web
        self.top_flange = RectangularCrossSection(
            name="Top Flange",
            width=top_flange_width,
            height=top_flange_thickness,
            x=0,
            y=(self.web_height + top_flange_thickness) / 2,
        )
        self.bottom_flange = RectangularCrossSection(
            name="Bottom Flange",
            width=bottom_flange_width,
            height=bottom_flange_thickness,
            x=0,
            y=-(self.web_height + bottom_flange_thickness) / 2,
        )
        self.web = RectangularCrossSection(
            name="Web",
            width=web_thickness,
            height=self.web_height,
            x=0,
            y=0,
        )

        # Create curves for the corners of the flanges
        self.curve_top_right = RightAngleCurvedCrossSection(
            name="Curve top right",
            radius=self.radius_top,
            x=web_thickness / 2,
            y=self.web_height / 2,
            flipped_horizontally=False,
            flipped_vertically=True,
        )
        self.curve_top_left = RightAngleCurvedCrossSection(
            name="Curve top left",
            radius=self.radius_top,
            x=-web_thickness / 2,
            y=self.web_height / 2,
            flipped_horizontally=True,
            flipped_vertically=True,
        )
        self.curve_bottom_right = RightAngleCurvedCrossSection(
            name="Curve bottom right",
            radius=self.radius_bottom,
            x=web_thickness / 2,
            y=-self.web_height / 2,
            flipped_horizontally=False,
            flipped_vertically=False,
        )
        self.curve_bottom_left = RightAngleCurvedCrossSection(
            name="Curve bottom left",
            radius=self.radius_bottom,
            x=-web_thickness / 2,
            y=-self.web_height / 2,
            flipped_horizontally=True,
            flipped_vertically=False,
        )

        # Combine the cross-sections into a single geometry
        self.cross_section = Polygon(
            self.top_flange.geometry.exterior.coords[:]
            + self.web.geometry.exterior.coords[:]
            + self.bottom_flange.geometry.exterior.coords[:]
            + self.curve_top_right.geometry.exterior.coords[:]
            + self.curve_top_left.geometry.exterior.coords[:]
            + self.curve_bottom_right.geometry.exterior.coords[:]
            + self.curve_bottom_left.geometry.exterior.coords[:]
        )

        # material properties
        material_top_flange = SteelMaterial(steel_class=steel_class, thickness=self.top_flange_thickness)
        material_bottom_flange = SteelMaterial(steel_class=steel_class, thickness=self.bottom_flange_thickness)
        material_web = SteelMaterial(steel_class=steel_class, thickness=self.web_thickness)

        # Create the steel elements
        self.elements = [
            SteelElement(cross_section=self.top_flange, material=material_top_flange),
            SteelElement(cross_section=self.bottom_flange, material=material_bottom_flange),
            SteelElement(cross_section=self.web, material=material_web),
            SteelElement(cross_section=self.curve_top_right, material=material_web),
            SteelElement(cross_section=self.curve_top_left, material=material_web),
            SteelElement(cross_section=self.curve_bottom_right, material=material_web),
            SteelElement(cross_section=self.curve_bottom_left, material=material_web),
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
        return plot_shapes(
            self.top_flange,
            self.bottom_flange,
            self.web,
            self.curve_top_right,
            self.curve_top_left,
            self.curve_bottom_right,
            self.curve_bottom_left,
            centroid=self.centroid,
            *args,
            **kwargs,
        )

if __name__ == "__main__":
    profile = ISteelProfile(
        top_flange_width=300,
        top_flange_thickness=36,
        bottom_flange_width=300,
        bottom_flange_thickness=36,
        total_height=1000,
        web_thickness=19,
        radius_bottom=30,
        radius_top=30,
        steel_class=SteelStrengthClass.EN_10025_2_S355,
    )
    profile.plot()
    plt.show()