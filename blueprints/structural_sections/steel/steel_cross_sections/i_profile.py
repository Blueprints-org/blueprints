"""I-Profile steel section."""

from matplotlib import pyplot as plt

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.cross_section_quarter_circular_spandrel import QuarterCircularSpandrelCrossSection
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import SteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.hea import HEA
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.hem import HEM
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.ipe import IPE
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
    top_radius : MM | None
        The radius of the curved corners of the top flange. Default is None, the corner radius is then taken as the thickness.
    bottom_radius : MM | None
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
        top_radius: MM | None = None,
        bottom_radius: MM | None = None,
    ) -> None:
        """Initialize the I-profile steel section."""
        self.top_flange_width = top_flange_width
        self.top_flange_thickness = top_flange_thickness
        self.bottom_flange_width = bottom_flange_width
        self.bottom_flange_thickness = bottom_flange_thickness
        self.total_height = total_height
        self.web_thickness = web_thickness
        self.top_radius = top_radius if top_radius is not None else top_flange_thickness
        self.bottom_radius = bottom_radius if bottom_radius is not None else bottom_flange_thickness

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
        self.curve_top_right = QuarterCircularSpandrelCrossSection(
            name="Curve top right",
            radius=self.top_radius,
            x=web_thickness / 2,
            y=self.web_height / 2,
            mirrored_horizontally=False,
            mirrored_vertically=True,
        )
        self.curve_top_left = QuarterCircularSpandrelCrossSection(
            name="Curve top left",
            radius=self.top_radius,
            x=-web_thickness / 2,
            y=self.web_height / 2,
            mirrored_horizontally=True,
            mirrored_vertically=True,
        )
        self.curve_bottom_right = QuarterCircularSpandrelCrossSection(
            name="Curve bottom right",
            radius=self.bottom_radius,
            x=web_thickness / 2,
            y=-self.web_height / 2,
            mirrored_horizontally=False,
            mirrored_vertically=False,
        )
        self.curve_bottom_left = QuarterCircularSpandrelCrossSection(
            name="Curve bottom left",
            radius=self.bottom_radius,
            x=-web_thickness / 2,
            y=-self.web_height / 2,
            mirrored_horizontally=True,
            mirrored_vertically=False,
        )

        # material properties
        self.steel_material = SteelMaterial(steel_class=steel_class)

        # Create the steel elements
        self.elements = [
            SteelElement(cross_section=self.top_flange, material=self.steel_material, nominal_thickness=top_flange_thickness),
            SteelElement(cross_section=self.bottom_flange, material=self.steel_material, nominal_thickness=bottom_flange_thickness),
            SteelElement(cross_section=self.web, material=self.steel_material, nominal_thickness=web_thickness),
            SteelElement(cross_section=self.curve_top_right, material=self.steel_material, nominal_thickness=top_flange_thickness),
            SteelElement(cross_section=self.curve_top_left, material=self.steel_material, nominal_thickness=top_flange_thickness),
            SteelElement(cross_section=self.curve_bottom_right, material=self.steel_material, nominal_thickness=bottom_flange_thickness),
            SteelElement(cross_section=self.curve_bottom_left, material=self.steel_material, nominal_thickness=bottom_flange_thickness),
        ]

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


class LoadStandardIProfile:
    r"""Class to load in values for standard I profile.

    Parameters
    ----------
    profile: ISteelProfile
        Representation of an I-Profile steel section
    steel_class: SteelStrengthClass
        Enumeration of steel strength classes (default: S355)
    """

    def __init__(
        self,
        profile: HEA | HEB | HEM | IPE,
        steel_class: SteelStrengthClass = SteelStrengthClass.S355,
    ) -> None:
        self.profile = profile
        self.steel_class = steel_class

    def __str__(self) -> str:
        """Return the steel class and profile."""
        return f"Steel class: {self.steel_class}, Profile: {self.profile}"

    def top_flange_width(self) -> MM:
        """Return the top flange width of the I-profile."""
        return self.profile.top_flange_width

    def top_flange_thickness(self) -> MM:
        """Return the top flange thickness of the I-profile."""
        return self.profile.top_flange_thickness

    def bottom_flange_width(self) -> MM:
        """Return the bottom flange width of the I-profile."""
        return self.profile.bottom_flange_width

    def bottom_flange_thickness(self) -> MM:
        """Return the bottom flange thickness of the I-profile."""
        return self.profile.bottom_flange_thickness

    def total_height(self) -> MM:
        """Return the total height of the I-profile."""
        return self.profile.total_height

    def web_thickness(self) -> MM:
        """Return the web thickness of the I-profile."""
        return self.profile.web_thickness

    def top_radius(self) -> MM:
        """Return the top radius of the I-profile."""
        return self.profile.top_radius

    def bottom_radius(self) -> MM:
        """Return the bottom radius of the I-profile."""
        return self.profile.bottom_radius

    def get_profile(self, corrosion: MM = 0) -> ISteelProfile:
        """Return the CHS profile.

        Parameters
        ----------
        corrosion : MM, optional
            Corrosion thickness per side (default is 0).
        """
        top_flange_width = self.top_flange_width() - corrosion * 2
        top_flange_thickness = self.top_flange_thickness() - corrosion * 2
        bottom_flange_width = self.bottom_flange_width() - corrosion * 2
        bottom_flange_thickness = self.bottom_flange_thickness() - corrosion * 2
        total_height = self.total_height() - corrosion * 2
        web_thickness = self.web_thickness() - corrosion * 2

        if top_flange_thickness <= 0 or bottom_flange_thickness <= 0 or web_thickness <= 0:
            raise ValueError("The profile has fully corroded.")

        return ISteelProfile(
            top_flange_width=top_flange_width,
            top_flange_thickness=top_flange_thickness,
            bottom_flange_width=bottom_flange_width,
            bottom_flange_thickness=bottom_flange_thickness,
            total_height=total_height,
            web_thickness=web_thickness,
            steel_class=self.steel_class,
            top_radius=self.top_radius(),
            bottom_radius=self.bottom_radius(),
        )
