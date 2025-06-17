"""Steel Strip Profile."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from matplotlib import pyplot as plt

from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import MM


@dataclass(kw_only=True)
class StripSteelProfile(CombinedSteelCrossSection):
    """Representation of a Steel Strip profile.

    This class is used to create a custom steel strip profile or to create a steel strip profile from a standard profile.
    For standard profiles, use the `from_standard_profile` class method.
    For example,
    ```python
    strip_profile = StripSteelProfile.from_standard_profile(profile=Strip.STRIP160x5, steel_material=SteelMaterial(SteelStrengthClass.S355))
    ```

    Attributes
    ----------
    steel_material : SteelMaterial
        Steel material properties for the profile.
    width : MM
        The width of the strip profile [mm].
    height : MM
        The height (thickness) of the strip profile [mm].
    """

    steel_material: SteelMaterial
    strip_width: MM
    strip_height: MM

    def __post_init__(self) -> None:
        """Initialize the Steel Strip profile."""
        # Nominal thickness is the minimum of width and height
        self.thickness = min(self.strip_width, self.strip_height)

        self.strip = RectangularCrossSection(
            name="Steel Strip",
            width=self.strip_width,
            height=self.strip_height,
            x=0,
            y=0,
        )
        self.elements = [
            SteelElement(
                cross_section=self.strip,
                material=self.steel_material,
                nominal_thickness=self.thickness,
            )
        ]

    @classmethod
    def from_standard_profile(
        cls,
        profile: Strip,
        steel_material: SteelMaterial,
        corrosion: MM = 0,
    ) -> Self:
        """Create a strip profile from a set of standard profiles already defined in Blueprints.

        Parameters
        ----------
        profile : Strip
            Any of the standard strip profiles defined in Blueprints.
        steel_material : SteelMaterial
            Steel material properties for the profile.
        corrosion : MM, optional
            Corrosion thickness per side (default is 0).
        """
        width = profile.width - corrosion * 2
        height = profile.height - corrosion * 2

        if width <= 0 or height <= 0:
            raise ValueError("The profile has fully corroded.")

        name = profile.alias
        if corrosion:
            name += f" (corrosion: {corrosion} mm)"

        return cls(
            steel_material=steel_material,
            strip_width=width,
            strip_height=height,
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
