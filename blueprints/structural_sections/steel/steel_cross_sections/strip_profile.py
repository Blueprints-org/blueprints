"""Strip Profile."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.structural_sections._polygon_builder import PolygonBuilder
from blueprints.structural_sections.steel.steel_cross_sections.plotters.general_steel_plotter import plot_shapes
from blueprints.structural_sections.steel.steel_cross_sections.standard_profiles.strip import Strip
from blueprints.type_alias import MM


@dataclass(frozen=True, kw_only=True)
class StripProfile(CrossSection):
    """Representation of a Strip profile.

    This class is used to create a custom strip profile or to create a strip profile from a standard profile.
    For standard profiles, use the `from_standard_profile` class method.
    For example,
    ```python
    strip_profile = StripProfile.from_standard_profile(profile=Strip.STRIP160x5)
    ```

    Attributes
    ----------
    width : MM
        The width of the strip profile [mm].
    height : MM
        The height (thickness) of the strip profile [mm].
    name : str
        The name of the profile. Default is "Strip Profile".
    plotter : Callable[[CrossSection], plt.Figure]
        The plotter function to visualize the cross-section (default: `plot_shapes`).
    """

    width: MM
    """The width of the strip profile [mm]."""
    height: MM
    """The height (thickness) of the strip profile [mm]."""
    name: str = "Strip Profile"
    """The name of the profile."""
    plotter: Callable[[CrossSection], plt.Figure] = plot_shapes
    """The plotter function to visualize the cross-section."""

    @property
    def polygon(self) -> Polygon:
        """Return the polygon of the strip profile cross-section."""
        return (
            # Start at top-left corner and go clockwise
            PolygonBuilder((0, 0))
            .append_line(length=self.width, angle=0)
            .append_line(length=self.height, angle=270)
            .append_line(length=self.width, angle=180)
            .append_line(length=self.height, angle=90)
            .generate_polygon()
        )

    @classmethod
    def from_standard_profile(
        cls,
        profile: Strip,
        corrosion: MM = 0,
    ) -> Self:
        """Create a strip profile from a set of standard profiles already defined in Blueprints.

        Parameters
        ----------
        profile : Strip
            Any of the standard strip profiles defined in Blueprints.
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
            width=width,
            height=height,
            name=name,
        )
