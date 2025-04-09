"""RHS-Profile steel section."""

from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial, SteelStrengthClass
from blueprints.structural_sections.cross_section_annular_sector import AnnularSectorCrossSection
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.base import SteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhs import RHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.rhscf import RHSCF
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shs import SHS
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.shscf import SHSCF
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM


class RHSSteelProfile(SteelCrossSection):
    """Representation of an C-Profile steel section.

    Parameters
    ----------
    total_width : MM
        The total width of the profile [mm].
    total_height : MM
        The total height of the profile [mm].
    thickness : MM
        The thickness of the walls [mm].
    steel_class : SteelStrengthClass
        The steel strength class of the profile.
    center_radius : MM | None
        The center_radius of the curved corners. Default is None, the radius is then taken as the 1.5*thickness.
    """

    def __init__(
        self,
        total_width: MM,
        total_height: MM,
        thickness: MM,
        steel_class: SteelStrengthClass,
        center_radius: MM | None = None,
    ) -> None:
        """Initialize the C-profile steel section."""
        self.total_width = total_width
        self.total_height = total_height
        self.thickness = thickness
        self.center_radius = center_radius if center_radius is not None else 1.5 * thickness
        self.inner_radius = self.center_radius - thickness / 2
        self.outer_radius = self.center_radius + thickness / 2

        # Calculate element parameters
        self.flange_width = total_width - self.outer_radius * 2
        self.web_height = total_height - self.outer_radius * 2

        # Create the cross-sections for the flanges and web
        self.top_flange = RectangularCrossSection(
            name="Top Flange",
            width=self.flange_width,
            height=self.thickness,
            x=0,
            y=(total_height - self.thickness) / 2,
        )
        self.bottom_flange = RectangularCrossSection(
            name="Bottom Flange",
            width=self.flange_width,
            height=thickness,
            x=0,
            y=-(total_height - thickness) / 2,
        )
        self.left_web = RectangularCrossSection(
            name="Left Web",
            width=thickness,
            height=self.web_height,
            x=-(total_width - thickness) / 2,
            y=0,
        )
        self.right_web = RectangularCrossSection(
            name="Right Web",
            width=thickness,
            height=self.web_height,
            x=(total_width - thickness) / 2,
            y=0,
        )

        self.curve_top_left = AnnularSectorCrossSection(
            name="Curve top left",
            inner_radius=self.inner_radius,
            thickness=self.thickness,
            x=-(self.flange_width) / 2,
            y=(self.web_height) / 2,
            start_angle=-90,
            end_angle=0,
        )

        self.curve_bottom_left = AnnularSectorCrossSection(
            name="Curve bottom left",
            inner_radius=self.inner_radius,
            thickness=self.thickness,
            x=-(self.flange_width) / 2,
            y=-(self.web_height) / 2,
            start_angle=180,
            end_angle=270,
        )

        self.curve_top_right = AnnularSectorCrossSection(
            name="Curve top right",
            inner_radius=self.inner_radius,
            thickness=self.thickness,
            x=(self.flange_width) / 2,
            y=(self.web_height) / 2,
            start_angle=0,
            end_angle=90,
        )

        self.curve_bottom_right = AnnularSectorCrossSection(
            name="Curve bottom right",
            inner_radius=self.inner_radius,
            thickness=self.thickness,
            x=(self.flange_width) / 2,
            y=-(self.web_height) / 2,
            start_angle=90,
            end_angle=180,
        )

        # material properties
        material_top_flange = SteelMaterial(steel_class=steel_class, thickness=self.flange_width)
        material_bottom_flange = SteelMaterial(steel_class=steel_class, thickness=self.thickness)
        material_web = SteelMaterial(steel_class=steel_class, thickness=self.thickness)

        # Create the steel elements
        self.elements = [
            SteelElement(cross_section=self.top_flange, material=material_top_flange),
            SteelElement(cross_section=self.bottom_flange, material=material_bottom_flange),
            SteelElement(cross_section=self.left_web, material=material_web),
            SteelElement(cross_section=self.right_web, material=material_web),
            SteelElement(cross_section=self.curve_top_left, material=material_web),
            SteelElement(cross_section=self.curve_bottom_left, material=material_web),
            SteelElement(cross_section=self.curve_top_right, material=material_web),
            SteelElement(cross_section=self.curve_bottom_right, material=material_web),
        ]

        self.steel_material = SteelMaterial(steel_class=steel_class, thickness=thickness)

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


class RHSProfiles:
    r"""Representation of the strength and deformation characteristics for RHS steel material.

    Parameters
    ----------
    steel_class: SteelStrengthClass
        Enumeration of steel strength classes (default: S355)
    profile: RHSSteelProfile
        Representation of an RHS-Profile steel section (default: RHSCF120x80_5)
    """

    def __init__(
        self,
        steel_class: SteelStrengthClass = SteelStrengthClass.EN_10025_2_S355,
        profile: RHSCF | RHS | SHSCF | SHS = RHSCF.RHSCF120x80_5,
    ) -> None:
        self.steel_class = steel_class
        self.profile = profile

    def __str__(self) -> str:
        """Return the steel class and profile dimensions."""
        return (
            f"Steel class: {self.steel_class}, "
            f"Width: {self.profile.total_width} mm, "
            f"Height: {self.profile.total_height} mm, "
            f"Thickness: {self.profile.thickness} mm"
        )

    def total_width(self) -> MM:
        """Return the total width of the RHS profile."""
        return self.profile.total_width

    def total_height(self) -> MM:
        """Return the total height of the RHS profile."""
        return self.profile.total_height

    def thickness(self) -> MM:
        """Return the wall thickness of the RHS profile."""
        return self.profile.thickness

    def center_radius(self) -> MM:
        """Return the corner radius of the RHS profile."""
        return self.profile.center_radius

    def get_profile(self) -> RHSSteelProfile:
        """Return the RHS steel profile."""
        return RHSSteelProfile(
            total_width=self.profile.total_width,
            total_height=self.profile.total_height,
            thickness=self.profile.thickness,
            steel_class=self.steel_class,
            center_radius=self.profile.center_radius,
        )
