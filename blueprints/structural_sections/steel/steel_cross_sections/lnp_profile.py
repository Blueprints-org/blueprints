"""LNP-Profile steel section."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.cross_section_cornered import CircularCorneredCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.lnp import LNP
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM


@dataclass(kw_only=True)
class LNPProfile(CombinedSteelCrossSection):
    """Representation of an LNP steel section.

    Attributes
    ----------
    steel_material : SteelMaterial
        Steel material properties for the profile.
    total_width : MM
        The width of the profile [mm].
    total_height : MM
        The height of the profile [mm].
    web_thickness : MM
        The thickness of the web [mm].
    base_thickness : MM
        The thickness of the base [mm].
    root_radius : MM | None
        The root radius of the top corner. Default is None, the corner radius is then taken as the web thickness.
    back_radius : MM | None
        The back radius of the top corner. Default is None, the corner radius is then taken as twice the web thickness.
    web_toe_radius : MM | None
        The radius of the toe in the web. Default is None, the corner radius is then taken as sharp angle.
    base_toe_radius : MM | None
        The radius of the toe in the base. Default is None, the corner radius is then taken as sharp angle.
    name : str
        The name of the profile. Default is "LNP-Profile". If corrosion is applied, the name will include the corrosion value.
    """

    steel_material: SteelMaterial
    total_width: MM
    total_height: MM
    web_thickness: MM
    base_thickness: MM
    root_radius: MM | None
    back_radius: MM | None
    web_toe_radius: MM | None
    base_toe_radius: MM | None
    name: str = "LNP-Profile"

    def __post_init__(self) -> None:
        """Initialize the RHS- or SHS-profile steel section."""
        if self.root_radius is None:
            self.root_radius = self.web_thickness
        if self.back_radius is None:
            self.back_radius = 2 * self.web_thickness
        if self.web_toe_radius is None:
            self.web_toe_radius = 0
        if self.base_toe_radius is None:
            self.base_toe_radius = 0

        self.web_height = self.total_height - self.base_thickness - self.root_radius
        self.base_width = self.total_width - self.web_thickness - self.root_radius

        # Create the cross-sections for the web
        self.web = CircularCorneredCrossSection(
            name="Web",
            thickness_vertical=self.web_height,
            thickness_horizontal=self.web_thickness,
            inner_radius=0,
            outer_radius=self.web_toe_radius,
            x=0,
            y=self.root_radius + self.base_thickness,
            corner_direction=0,
        )

        # Create the cross-sections for the base
        self.base = CircularCorneredCrossSection(
            name="Base",
            thickness_vertical=self.base_thickness,
            thickness_horizontal=self.base_width,
            inner_radius=0,
            outer_radius=self.base_toe_radius,
            x=self.root_radius + self.web_thickness,
            y=0,
            corner_direction=0,
        )

        # Create the cross-sections for the corner
        self.corner = CircularCorneredCrossSection(
            name="Corner",
            thickness_vertical=self.base_thickness,
            thickness_horizontal=self.web_thickness,
            inner_radius=self.root_radius,
            outer_radius=self.back_radius,
            x=self.web_thickness + self.root_radius,
            y=self.base_thickness + self.root_radius,
            corner_direction=2,
        )

        # Create the steel elements
        self.elements = [
            SteelElement(
                cross_section=self.web,
                material=self.steel_material,
                nominal_thickness=self.web_thickness,
            ),
            SteelElement(
                cross_section=self.base,
                material=self.steel_material,
                nominal_thickness=self.base_thickness,
            ),
            SteelElement(
                cross_section=self.corner,
                material=self.steel_material,
                nominal_thickness=self.back_radius - self.root_radius,
            ),
        ]

    @classmethod
    def from_standard_profile(
        cls,
        profile: LNP,
        steel_material: SteelMaterial,
        corrosion: MM = 0,
    ) -> Self:
        """Create an LNP-profile from a set of standard profiles already defined in Blueprints.

        Blueprints offers standard profiles for LNP. This method allows you to create an LNP-profile.

        Parameters
        ----------
        profile : LNP
            Any of the standard profiles defined in Blueprints.
        steel_material : SteelMaterial
            Steel material properties for the profile.
        corrosion : MM, optional
            Corrosion thickness per side (default is 0).
        """
        total_width = profile.width - 2 * corrosion
        total_height = profile.height - 2 * corrosion

        web_thickness = profile.web_thickness - 2 * corrosion
        base_thickness = profile.base_thickness - 2 * corrosion

        root_radius = profile.root_radius + corrosion
        back_radius = max(profile.back_radius - corrosion, 0)
        base_toe_radius = min(profile.toe_radius, base_thickness)
        web_toe_radius = min(profile.toe_radius, web_thickness)

        if any(
            [
                web_thickness < 1e-3,
                base_thickness < 1e-3,
            ]
        ):
            raise ValueError("The profile has fully corroded.")

        name = profile.alias
        if corrosion:
            name += f" (corrosion: {corrosion} mm)"

        return cls(
            steel_material=steel_material,
            total_width=total_width,
            total_height=total_height,
            web_thickness=web_thickness,
            base_thickness=base_thickness,
            root_radius=root_radius,
            back_radius=back_radius,
            web_toe_radius=web_toe_radius,
            base_toe_radius=base_toe_radius,
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
