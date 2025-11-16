"""UNP-Profile steel section."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

import numpy as np
from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial
from blueprints.math_helpers import slope_to_angle
from blueprints.structural_sections.cross_section_cornered import CircularCorneredCrossSection
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.unp import UNP
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM, PERCENTAGE


@dataclass(kw_only=True)
class UNPSteelProfile(CombinedSteelCrossSection):
    """Representation of a UNP-Profile steel section.
    This can be used to create a custom UNP-profile or to create a UNP-profile from a standard profile.

    For standard profiles, use the `from_standard_profile` class method.
    For example,
    ```python
    unp_profile = UNPSteelProfile.from_standard_profile(profile=UNP.UNP200, steel_material=SteelMaterial(SteelStrengthClass.S355))
    ```

    Attributes
    ----------
    steel_material : SteelMaterial
        Steel material properties for the profile.
    top_flange_total_width : MM
        The total width of the top flange [mm].
    top_flange_thickness : MM
        The thickness of the top flange [mm].
    bottom_flange_total_width : MM
        The total width of the bottom flange [mm].
    bottom_flange_thickness : MM
        The thickness of the bottom flange [mm].
    total_height : MM
        The total height of the profile [mm].
    web_thickness : MM
        The thickness of the web [mm].
    top_root_fillet_radius : MM | None
        The radius of the curved corners of the top flange. Default is None, the corner radius is then taken as the thickness of top flange.
    top_toe_radius : MM
        The radius of the outer corners of the top flange. Default is 0, meaning sharp corner.
    bottom_root_fillet_radius : MM | None
        The radius of the curved corners of the bottom flange. Default is None, the corner radius is then taken as the thickness of bottom flange.
    bottom_toe_radius : MM
        The radius of the outer corners of the bottom flange. Default is 0, meaning sharp corner.
    top_slope : PERCENTAGE
        The slope of the top flange. Default is 0.
    bottom_slope : PERCENTAGE
        The slope of the bottom flange. Default is 0.
    name : str
        The name of the profile. Default is "UNP-Profile". If corrosion is applied, the name will include the corrosion value.
    """

    steel_material: SteelMaterial
    top_flange_total_width: MM
    top_flange_thickness: MM
    bottom_flange_total_width: MM
    bottom_flange_thickness: MM
    total_height: MM
    web_thickness: MM
    top_root_fillet_radius: MM | None = None
    top_toe_radius: MM = 0
    bottom_root_fillet_radius: MM | None = None
    bottom_toe_radius: MM = 0
    top_slope: PERCENTAGE = 0.0
    bottom_slope: PERCENTAGE = 0.0
    name: str = "UNP-Profile"

    def __post_init__(self) -> None:
        """Initialize the UNP-profile steel section."""
        self.top_root_fillet_radius = self.top_root_fillet_radius if self.top_root_fillet_radius is not None else self.top_flange_thickness
        self.bottom_root_fillet_radius = (
            self.bottom_root_fillet_radius if self.bottom_root_fillet_radius is not None else self.bottom_flange_thickness
        )

        # Create curves for the corners of the flanges
        # It is used that the thickness is measured vertically halfway the total width of the flange
        # The results of this allign with standard UNP profiles databases
        top_angle = np.deg2rad(slope_to_angle(self.top_slope))
        bottom_angle = np.deg2rad(slope_to_angle(self.bottom_slope))

        top_thickness_at_web = (
            self.top_flange_thickness
            + (self.top_flange_total_width / 2 - self.web_thickness - self.top_root_fillet_radius * np.cos(top_angle)) * self.top_slope / 100
        )
        bottom_thickness_at_web = (
            self.bottom_flange_thickness
            + (self.bottom_flange_total_width / 2 - self.web_thickness - self.bottom_root_fillet_radius * np.cos(bottom_angle))
            * self.bottom_slope
            / 100
        )

        top_thickness_at_toe = max(0, self.top_flange_thickness - (self.top_flange_total_width / 2) * self.top_slope / 100)
        bottom_thickness_at_toe = max(0, self.bottom_flange_thickness - (self.bottom_flange_total_width / 2) * self.bottom_slope / 100)

        self.corner_top = CircularCorneredCrossSection(
            name="Corner top",
            inner_radius=self.top_root_fillet_radius,
            outer_radius=0,
            x=0,
            y=self.total_height / 2,
            corner_direction=1,
            thickness_horizontal=self.web_thickness,
            thickness_vertical=top_thickness_at_web,
            inner_slope_at_vertical=self.top_slope,
            reference_point="outer",
        )
        self.corner_bottom = CircularCorneredCrossSection(
            name="Corner bottom",
            inner_radius=self.bottom_root_fillet_radius,
            outer_radius=0,
            x=0,
            y=-self.total_height / 2,
            corner_direction=2,
            thickness_horizontal=self.web_thickness,
            thickness_vertical=bottom_thickness_at_web,
            inner_slope_at_vertical=self.bottom_slope,
            reference_point="outer",
        )

        self.web = RectangularCrossSection(
            name="Web",
            width=self.web_thickness,
            height=self.total_height - self.corner_bottom.total_height - self.corner_top.total_height,
            x=self.web_thickness / 2,
            y=0,
        )

        # using modelled toe radius to avoid impossible geometry with small mesh
        modelled_top_toe_radius = (
            min(self.top_toe_radius, 0.95 * top_thickness_at_toe) if min(self.top_toe_radius, 0.95 * top_thickness_at_toe) >= 1.0 else 0
        )
        self.top_flange = CircularCorneredCrossSection(
            name="Top flange",
            inner_radius=0,
            outer_radius=modelled_top_toe_radius,
            x=self.corner_top.total_width,
            y=self.total_height / 2,
            corner_direction=3,
            thickness_horizontal=self.top_flange_total_width - self.corner_top.total_width,
            thickness_vertical=top_thickness_at_web,
            outer_slope_at_vertical=self.top_slope,
        )

        # using modelled toe radius to avoid impossible geometry with small mesh
        modelled_bottom_toe_radius = (
            min(self.bottom_toe_radius, 0.95 * bottom_thickness_at_toe) if min(self.bottom_toe_radius, 0.95 * bottom_thickness_at_toe) >= 1.0 else 0
        )
        self.bottom_flange = CircularCorneredCrossSection(
            name="Bottom flange",
            inner_radius=0,
            outer_radius=modelled_bottom_toe_radius,
            x=self.corner_bottom.total_width,
            y=-self.total_height / 2,
            corner_direction=0,
            thickness_horizontal=self.bottom_flange_total_width - self.corner_bottom.total_width,
            thickness_vertical=bottom_thickness_at_web,
            outer_slope_at_vertical=self.bottom_slope,
        )

        # Create the steel elements
        self.elements = [
            SteelElement(
                cross_section=self.corner_top,
                material=self.steel_material,
                nominal_thickness=self.bottom_flange_thickness,
            ),
            SteelElement(
                cross_section=self.corner_bottom,
                material=self.steel_material,
                nominal_thickness=self.bottom_flange_thickness,
            ),
            SteelElement(
                cross_section=self.web,
                material=self.steel_material,
                nominal_thickness=self.web_thickness,
            ),
            SteelElement(
                cross_section=self.top_flange,
                material=self.steel_material,
                nominal_thickness=self.top_flange_thickness,
            ),
            SteelElement(
                cross_section=self.bottom_flange,
                material=self.steel_material,
                nominal_thickness=self.bottom_flange_thickness,
            ),
        ]

    @classmethod
    def from_standard_profile(
        cls,
        profile: UNP,
        steel_material: SteelMaterial,
        corrosion: MM = 0,
    ) -> Self:
        """Create a UNP-profile from a set of standard profiles already defined in Blueprints.

        Blueprints offers standard profiles for UNP. This method allows you to create a UNP-profile.

        Parameters
        ----------
        profile : UNP
            Any of the standard UNP profiles defined in Blueprints.
        steel_material : SteelMaterial
            Steel material properties for the profile.
        corrosion : MM, optional
            Corrosion thickness per side (default is 0).
        """
        top_flange_total_width = profile.top_flange_total_width - corrosion * 2
        top_flange_thickness = profile.top_flange_thickness - corrosion * 2
        bottom_flange_total_width = profile.bottom_flange_total_width - corrosion * 2
        bottom_flange_thickness = profile.bottom_flange_thickness - corrosion * 2
        total_height = profile.total_height - corrosion * 2
        web_thickness = profile.web_thickness - corrosion * 2
        top_root_fillet_radius = profile.root_fillet_radius + corrosion
        bottom_root_fillet_radius = profile.root_fillet_radius + corrosion
        top_toe_radius = max(profile.toe_radius - corrosion, 0)
        bottom_toe_radius = max(profile.toe_radius - corrosion, 0)

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
            top_flange_total_width=top_flange_total_width,
            top_flange_thickness=top_flange_thickness,
            bottom_flange_total_width=bottom_flange_total_width,
            bottom_flange_thickness=bottom_flange_thickness,
            total_height=total_height,
            web_thickness=web_thickness,
            steel_material=steel_material,
            top_root_fillet_radius=top_root_fillet_radius,
            top_toe_radius=top_toe_radius,
            bottom_root_fillet_radius=bottom_root_fillet_radius,
            bottom_toe_radius=bottom_toe_radius,
            top_slope=profile.slope,
            bottom_slope=profile.slope,
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
