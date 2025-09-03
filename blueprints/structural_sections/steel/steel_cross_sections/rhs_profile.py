"""RHS- and SHS-Profile steel section."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.cross_section_cornered import CircularCorneredCrossSection
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhscf import RHSCF
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shs import SHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shscf import SHSCF
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM


@dataclass(kw_only=True)
class RHSSteelProfile(CombinedSteelCrossSection):
    """Representation of an SHS or RHS steel section.

    Attributes
    ----------
    steel_material : SteelMaterial
        Steel material properties for the profile.
    total_width : MM
        The width of the profile [mm].
    total_height : MM
        The height of the profile [mm].
    left_wall_thickness : MM
        The thickness of the left wall [mm].
    right_wall_thickness : MM
        The thickness of the right wall [mm].
    top_wall_thickness : MM
        The thickness of the top wall [mm].
    bottom_wall_thickness : MM
        The thickness of the bottom wall [mm].
    top_right_inner_radius : MM | None
        The inner radius of the top right corner. Default is None, the corner radius is then taken as the thickness.
    top_left_inner_radius : MM | None
        The inner radius of the top left corner. Default is None, the corner radius is then taken as the thickness.
    bottom_right_inner_radius : MM | None
        The inner radius of the bottom right corner. Default is None, the corner radius is then taken as the thickness.
    bottom_left_inner_radius : MM | None
        The inner radius of the bottom left corner. Default is None, the corner radius is then taken as the thickness.
    top_right_outer_radius : MM | None
        The outer radius of the top right corner. Default is None, the corner radius is then taken as twice the thickness.
    top_left_outer_radius : MM | None
        The outer radius of the top left corner. Default is None, the corner radius is then taken as twice the thickness.
    bottom_right_outer_radius : MM | None
        The outer radius of the bottom right corner. Default is None, the corner radius is then taken as twice the thickness.
    bottom_left_outer_radius : MM | None
        The outer radius of the bottom left corner. Default is None, the corner radius is then taken as twice the thickness.
    name : str
        The name of the profile. Default is "RHS-Profile". If corrosion is applied, the name will include the corrosion value.
    """

    steel_material: SteelMaterial
    total_width: MM
    total_height: MM
    left_wall_thickness: MM
    right_wall_thickness: MM
    top_wall_thickness: MM
    bottom_wall_thickness: MM
    top_right_inner_radius: MM | None = None
    top_left_inner_radius: MM | None = None
    bottom_right_inner_radius: MM | None = None
    bottom_left_inner_radius: MM | None = None
    top_right_outer_radius: MM | None = None
    top_left_outer_radius: MM | None = None
    bottom_right_outer_radius: MM | None = None
    bottom_left_outer_radius: MM | None = None
    name: str = "RHS-Profile"

    def __post_init__(self) -> None:
        """Initialize the RHS- or SHS-profile steel section."""
        self.top_right_inner_radius = self.top_right_inner_radius if self.top_right_inner_radius is not None else self.top_wall_thickness
        self.top_left_inner_radius = self.top_left_inner_radius if self.top_left_inner_radius is not None else self.top_wall_thickness
        self.bottom_right_inner_radius = self.bottom_right_inner_radius if self.bottom_right_inner_radius is not None else self.bottom_wall_thickness
        self.bottom_left_inner_radius = self.bottom_left_inner_radius if self.bottom_left_inner_radius is not None else self.bottom_wall_thickness
        self.top_right_outer_radius = self.top_right_outer_radius if self.top_right_outer_radius is not None else 2 * self.top_wall_thickness
        self.top_left_outer_radius = self.top_left_outer_radius if self.top_left_outer_radius is not None else 2 * self.top_wall_thickness
        self.bottom_right_outer_radius = (
            self.bottom_right_outer_radius if self.bottom_right_outer_radius is not None else 2 * self.bottom_wall_thickness
        )
        self.bottom_left_outer_radius = self.bottom_left_outer_radius if self.bottom_left_outer_radius is not None else 2 * self.bottom_wall_thickness

        # calculate the lengths of the rectangular sections
        self.right_wall_height = (
            self.total_height - self.top_wall_thickness - self.bottom_wall_thickness - self.top_right_inner_radius - self.bottom_right_inner_radius
        )
        self.left_wall_height = (
            self.total_height - self.top_wall_thickness - self.bottom_wall_thickness - self.top_left_inner_radius - self.bottom_left_inner_radius
        )
        self.top_wall_width = (
            self.total_width - self.left_wall_thickness - self.right_wall_thickness - self.top_right_inner_radius - self.top_left_inner_radius
        )
        self.bottom_wall_width = (
            self.total_width - self.left_wall_thickness - self.right_wall_thickness - self.bottom_right_inner_radius - self.bottom_left_inner_radius
        )

        # Create the cross-sections for the flanges and web
        self.top_wall = RectangularCrossSection(
            name="Top Wall",
            width=self.top_wall_width,
            height=self.top_wall_thickness,
            x=(self.left_wall_thickness - self.right_wall_thickness + self.top_left_inner_radius - self.top_right_inner_radius) / 2,
            y=(self.total_height - self.top_wall_thickness) / 2,
        )
        self.bottom_wall = RectangularCrossSection(
            name="Bottom Wall",
            width=self.bottom_wall_width,
            height=self.bottom_wall_thickness,
            x=(self.left_wall_thickness - self.right_wall_thickness + self.bottom_left_inner_radius - self.bottom_right_inner_radius) / 2,
            y=-(self.total_height - self.bottom_wall_thickness) / 2,
        )
        self.left_wall = RectangularCrossSection(
            name="Left Wall",
            width=self.left_wall_thickness,
            height=self.left_wall_height,
            x=-(self.total_width - self.left_wall_thickness) / 2,
            y=-(self.top_wall_thickness - self.bottom_wall_thickness + self.top_left_inner_radius - self.bottom_left_inner_radius) / 2,
        )
        self.right_wall = RectangularCrossSection(
            name="Right Wall",
            width=self.right_wall_thickness,
            height=self.right_wall_height,
            x=(self.total_width - self.right_wall_thickness) / 2,
            y=-(self.top_wall_thickness - self.bottom_wall_thickness + self.top_right_inner_radius - self.bottom_right_inner_radius) / 2,
        )

        # Create the corner sections
        self.top_right_corner = CircularCorneredCrossSection(
            name="Top Right Corner",
            thickness_vertical=self.top_wall_thickness,
            thickness_horizontal=self.right_wall_thickness,
            inner_radius=self.top_right_inner_radius,
            outer_radius=self.top_right_outer_radius,
            x=self.total_width / 2 - self.right_wall_thickness - self.top_right_inner_radius,
            y=self.total_height / 2 - self.top_wall_thickness - self.top_right_inner_radius,
            corner_direction=0,
        )
        self.top_left_corner = CircularCorneredCrossSection(
            name="Top Left Corner",
            thickness_vertical=self.top_wall_thickness,
            thickness_horizontal=self.left_wall_thickness,
            inner_radius=self.top_left_inner_radius,
            outer_radius=self.top_left_outer_radius,
            x=-self.total_width / 2 + self.left_wall_thickness + self.top_left_inner_radius,
            y=self.total_height / 2 - self.top_wall_thickness - self.top_left_inner_radius,
            corner_direction=1,
        )
        self.bottom_right_corner = CircularCorneredCrossSection(
            name="Bottom Right Corner",
            thickness_vertical=self.bottom_wall_thickness,
            thickness_horizontal=self.right_wall_thickness,
            inner_radius=self.bottom_right_inner_radius,
            outer_radius=self.bottom_right_outer_radius,
            x=self.total_width / 2 - self.right_wall_thickness - self.bottom_right_inner_radius,
            y=-self.total_height / 2 + self.bottom_wall_thickness + self.bottom_right_inner_radius,
            corner_direction=3,
        )
        self.bottom_left_corner = CircularCorneredCrossSection(
            name="Bottom Left Corner",
            thickness_vertical=self.bottom_wall_thickness,
            thickness_horizontal=self.left_wall_thickness,
            inner_radius=self.bottom_left_inner_radius,
            outer_radius=self.bottom_left_outer_radius,
            x=-self.total_width / 2 + self.left_wall_thickness + self.bottom_left_inner_radius,
            y=-self.total_height / 2 + self.bottom_wall_thickness + self.bottom_left_inner_radius,
            corner_direction=2,
        )

        # Create the steel elements
        self.elements = [
            SteelElement(
                cross_section=self.top_wall,
                material=self.steel_material,
                nominal_thickness=self.top_wall_thickness,
            ),
            SteelElement(
                cross_section=self.bottom_wall,
                material=self.steel_material,
                nominal_thickness=self.bottom_wall_thickness,
            ),
            SteelElement(
                cross_section=self.left_wall,
                material=self.steel_material,
                nominal_thickness=self.left_wall_thickness,
            ),
            SteelElement(
                cross_section=self.right_wall,
                material=self.steel_material,
                nominal_thickness=self.right_wall_thickness,
            ),
            SteelElement(
                cross_section=self.top_right_corner,
                material=self.steel_material,
                nominal_thickness=self.top_wall_thickness,
            ),
            SteelElement(
                cross_section=self.top_left_corner,
                material=self.steel_material,
                nominal_thickness=self.top_wall_thickness,
            ),
            SteelElement(
                cross_section=self.bottom_right_corner,
                material=self.steel_material,
                nominal_thickness=self.bottom_wall_thickness,
            ),
            SteelElement(
                cross_section=self.bottom_left_corner,
                material=self.steel_material,
                nominal_thickness=self.bottom_wall_thickness,
            ),
        ]

    @classmethod
    def from_standard_profile(
        cls,
        profile: RHS | SHS | RHSCF | SHSCF,
        steel_material: SteelMaterial,
        corrosion_outside: MM = 0,
        corrosion_inside: MM = 0,
    ) -> Self:
        """Create an RHS- or SHS-profile from a set of standard profiles already defined in Blueprints.

        Blueprints offers standard profiles for RHS, SHS, RHSCF, and SHSCF. This method allows you to create an RHS/SHS-profile.

        Parameters
        ----------
        profile : RHS | SHS | RHSCF | SHSCF
            Any of the standard profiles defined in Blueprints.
        steel_material : SteelMaterial
            Steel material properties for the profile.
        corrosion_outside : MM, optional
            Corrosion thickness to be subtracted from the outer diameter [mm] (default: 0).
        corrosion_inside : MM, optional
            Corrosion thickness to be added to the inner diameter [mm] (default: 0).
        """
        total_width = profile.total_width - 2 * corrosion_outside
        total_height = profile.total_height - 2 * corrosion_outside

        top_wall_thickness = profile.thickness - corrosion_outside - corrosion_inside
        bottom_wall_thickness = profile.thickness - corrosion_outside - corrosion_inside
        left_wall_thickness = profile.thickness - corrosion_outside - corrosion_inside
        right_wall_thickness = profile.thickness - corrosion_outside - corrosion_inside

        top_right_inner_radius = profile.inner_radius + corrosion_inside
        top_left_inner_radius = profile.inner_radius + corrosion_inside
        bottom_right_inner_radius = profile.inner_radius + corrosion_inside
        bottom_left_inner_radius = profile.inner_radius + corrosion_inside
        top_right_outer_radius = max(profile.outer_radius - corrosion_outside, 0)
        top_left_outer_radius = max(profile.outer_radius - corrosion_outside, 0)
        bottom_right_outer_radius = max(profile.outer_radius - corrosion_outside, 0)
        bottom_left_outer_radius = max(profile.outer_radius - corrosion_outside, 0)

        if any(
            [
                top_wall_thickness < 1e-3,
                bottom_wall_thickness < 1e-3,
                left_wall_thickness < 1e-3,
                right_wall_thickness < 1e-3,
            ]
        ):
            raise ValueError("The profile has fully corroded.")

        name = profile.alias
        if corrosion_inside or corrosion_outside:
            name += (
                f" (corrosion {'' if not corrosion_inside else f'in: {corrosion_inside} mm'}"
                f"{', ' if corrosion_inside and corrosion_outside else ''}"
                f"{'' if not corrosion_outside else f'out: {corrosion_outside} mm'})"
            )

        return cls(
            steel_material=steel_material,
            total_width=total_width,
            total_height=total_height,
            left_wall_thickness=left_wall_thickness,
            right_wall_thickness=right_wall_thickness,
            top_wall_thickness=top_wall_thickness,
            bottom_wall_thickness=bottom_wall_thickness,
            top_right_inner_radius=top_right_inner_radius,
            top_left_inner_radius=top_left_inner_radius,
            bottom_right_inner_radius=bottom_right_inner_radius,
            bottom_left_inner_radius=bottom_left_inner_radius,
            top_right_outer_radius=top_right_outer_radius,
            top_left_outer_radius=top_left_outer_radius,
            bottom_right_outer_radius=bottom_right_outer_radius,
            bottom_left_outer_radius=bottom_left_outer_radius,
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
