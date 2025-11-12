"""I-Profile steel section."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.cross_section_cornered import CircularCorneredCrossSection
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.hea import HEA
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.heb import HEB
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.hem import HEM
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.ipe import IPE
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM


@dataclass(kw_only=True)
class ISteelProfile(CombinedSteelCrossSection):
    """Representation of an I-Profile steel section.
    This can be used to create a custom I-profile or to create an I-profile from a standard profile.

    For standard profiles, use the `from_standard_profile` class method.
    For example,
    ```python
    i_profile = ISteelProfile.from_standard_profile(profile=HEA.HEA200, steel_material=SteelMaterial(SteelStrengthClass.S355))
    ```

    Attributes
    ----------
    steel_material : SteelMaterial
        Steel material properties for the profile.
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
    top_radius : MM | None
        The radius of the curved corners of the top flange. Default is None, the corner radius is then taken as the thickness.
    bottom_radius : MM | None
        The radius of the curved corners of the bottom flange. Default is None, the corner radius is then taken as the thickness.
    name : str
        The name of the profile. Default is "I-Profile". If corrosion is applied, the name will include the corrosion value.
    """

    steel_material: SteelMaterial
    top_flange_width: MM
    top_flange_thickness: MM
    bottom_flange_width: MM
    bottom_flange_thickness: MM
    total_height: MM
    web_thickness: MM
    top_radius: MM | None = None
    bottom_radius: MM | None = None
    name: str = "I-Profile"

    def __post_init__(self) -> None:
        """Initialize the I-profile steel section."""
        self.top_radius = self.top_radius if self.top_radius is not None else self.top_flange_thickness
        self.bottom_radius = self.bottom_radius if self.bottom_radius is not None else self.bottom_flange_thickness

        # Calculate web height
        self.web_height = self.total_height - self.top_flange_thickness - self.bottom_flange_thickness - self.top_radius - self.bottom_radius
        self.width_outstand_top_flange = (self.top_flange_width - self.web_thickness - 2 * self.top_radius) / 2
        self.width_outstand_bottom_flange = (self.bottom_flange_width - self.web_thickness - 2 * self.bottom_radius) / 2

        # Create the cross-sections for the flanges and web
        self.top_right_flange = RectangularCrossSection(
            name="Top Right Flange",
            width=self.width_outstand_top_flange,
            height=self.top_flange_thickness,
            x=self.top_flange_width / 2 - self.width_outstand_top_flange / 2,
            y=(self.total_height - self.top_flange_thickness) / 2,
        )

        self.top_left_flange = RectangularCrossSection(
            name="Top Left Flange",
            width=self.width_outstand_top_flange,
            height=self.top_flange_thickness,
            x=-self.top_flange_width / 2 + self.width_outstand_top_flange / 2,
            y=(self.total_height - self.top_flange_thickness) / 2,
        )

        self.bottom_right_flange = RectangularCrossSection(
            name="Bottom Right Flange",
            width=self.width_outstand_bottom_flange,
            height=self.bottom_flange_thickness,
            x=self.bottom_flange_width / 2 - self.width_outstand_bottom_flange / 2,
            y=-(self.total_height - self.bottom_flange_thickness) / 2,
        )

        self.bottom_left_flange = RectangularCrossSection(
            name="Bottom Left Flange",
            width=self.width_outstand_bottom_flange,
            height=self.bottom_flange_thickness,
            x=-self.bottom_flange_width / 2 + self.width_outstand_bottom_flange / 2,
            y=-(self.total_height - self.bottom_flange_thickness) / 2,
        )

        self.web = RectangularCrossSection(
            name="Web",
            width=self.web_thickness,
            height=self.web_height,
            x=0,
            y=(-self.top_flange_thickness - self.top_radius + self.bottom_flange_thickness + self.bottom_radius) / 2,
        )

        # Create curves for the corners of the flanges
        self.curve_top_right = CircularCorneredCrossSection(
            name="Curve top right",
            inner_radius=self.top_radius,
            outer_radius=0,
            x=self.top_radius + self.web_thickness / 2,
            y=self.total_height / 2 - self.top_flange_thickness - self.top_radius,
            corner_direction=1,
            thickness_horizontal=self.web_thickness / 2,
            thickness_vertical=self.top_flange_thickness,
        )
        self.curve_top_left = CircularCorneredCrossSection(
            name="Curve top left",
            inner_radius=self.top_radius,
            outer_radius=0,
            x=-self.top_radius - self.web_thickness / 2,
            y=self.total_height / 2 - self.top_flange_thickness - self.top_radius,
            corner_direction=0,
            thickness_horizontal=self.web_thickness / 2,
            thickness_vertical=self.top_flange_thickness,
        )
        self.curve_bottom_right = CircularCorneredCrossSection(
            name="Curve bottom right",
            inner_radius=self.bottom_radius,
            outer_radius=0,
            x=self.bottom_radius + self.web_thickness / 2,
            y=-self.total_height / 2 + self.bottom_flange_thickness + self.bottom_radius,
            corner_direction=2,
            thickness_horizontal=self.web_thickness / 2,
            thickness_vertical=self.bottom_flange_thickness,
        )
        self.curve_bottom_left = CircularCorneredCrossSection(
            name="Curve bottom left",
            inner_radius=self.bottom_radius,
            outer_radius=0,
            x=-self.bottom_radius - self.web_thickness / 2,
            y=-self.total_height / 2 + self.bottom_flange_thickness + self.bottom_radius,
            corner_direction=3,
            thickness_horizontal=self.web_thickness / 2,
            thickness_vertical=self.bottom_flange_thickness,
        )

        # Create the steel elements
        self.elements = [
            SteelElement(
                cross_section=self.top_right_flange,
                material=self.steel_material,
                nominal_thickness=self.top_flange_thickness,
            ),
            SteelElement(
                cross_section=self.top_left_flange,
                material=self.steel_material,
                nominal_thickness=self.top_flange_thickness,
            ),
            SteelElement(
                cross_section=self.bottom_right_flange,
                material=self.steel_material,
                nominal_thickness=self.bottom_flange_thickness,
            ),
            SteelElement(
                cross_section=self.bottom_left_flange,
                material=self.steel_material,
                nominal_thickness=self.bottom_flange_thickness,
            ),
            SteelElement(
                cross_section=self.web,
                material=self.steel_material,
                nominal_thickness=self.web_thickness,
            ),
            SteelElement(
                cross_section=self.curve_top_right,
                material=self.steel_material,
                nominal_thickness=self.top_flange_thickness,
            ),
            SteelElement(
                cross_section=self.curve_top_left,
                material=self.steel_material,
                nominal_thickness=self.top_flange_thickness,
            ),
            SteelElement(
                cross_section=self.curve_bottom_right,
                material=self.steel_material,
                nominal_thickness=self.bottom_flange_thickness,
            ),
            SteelElement(
                cross_section=self.curve_bottom_left,
                material=self.steel_material,
                nominal_thickness=self.bottom_flange_thickness,
            ),
        ]

    @classmethod
    def from_standard_profile(
        cls,
        profile: HEA | HEB | HEM | IPE,
        steel_material: SteelMaterial,
        corrosion: MM = 0,
    ) -> Self:
        """Create an I-profile from a set of standard profiles already defined in Blueprints.

        Blueprints offers standard profiles for HEA, HEB, HEM, and IPE. This method allows you to create an I-profile.

        Parameters
        ----------
        profile : HEA | HEB | HEM | IPE
            Any of the standard profiles defined in Blueprints.
        steel_material : SteelMaterial
            Steel material properties for the profile.
        corrosion : MM, optional
            Corrosion thickness per side (default is 0).
        """
        top_flange_width = profile.top_flange_width - corrosion * 2
        top_flange_thickness = profile.top_flange_thickness - corrosion * 2
        bottom_flange_width = profile.bottom_flange_width - corrosion * 2
        bottom_flange_thickness = profile.bottom_flange_thickness - corrosion * 2
        total_height = profile.total_height - corrosion * 2
        web_thickness = profile.web_thickness - corrosion * 2

        if any(
            [
                top_flange_thickness < 1e-3,
                bottom_flange_thickness < 1e-3,
                web_thickness < 1e-3,
            ]
        ):
            raise ValueError("The profile has fully corroded.")

        name = profile.alias
        if corrosion:
            name += f" (corrosion: {corrosion} mm)"

        return cls(
            top_flange_width=top_flange_width,
            top_flange_thickness=top_flange_thickness,
            bottom_flange_width=bottom_flange_width,
            bottom_flange_thickness=bottom_flange_thickness,
            total_height=total_height,
            web_thickness=web_thickness,
            steel_material=steel_material,
            top_radius=profile.top_radius,
            bottom_radius=profile.bottom_radius,
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
