"""Strip Profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from matplotlib import pyplot as plt
from shapely.geometry import Polygon

from blueprints.structural_sections._polygon_builder import PolygonBuilder
from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.profile_definitions.corrosion_utils import FULL_CORROSION_TOLERANCE, update_name_with_corrosion
from blueprints.structural_sections.steel.profile_definitions.plotters.general_steel_plotter import plot_shapes
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


@dataclass(frozen=True, kw_only=True)
class StripProfile(Profile):
    """Representation of a Strip profile.

    For standard profiles, use the specific standard profile class `Strip`.
    For example,
    ```python
    strip_profile = Strip.STRIP160x5
    ```

    Attributes
    ----------
    width : MM
        The width of the strip profile [mm].
    height : MM
        The height (thickness) of the strip profile [mm].
    name : str
        The name of the profile. Default is "Strip Profile".
    plotter : Callable[[Profile], plt.Figure]
        The plotter function to visualize the profile (default: `plot_shapes`).
    """

    width: MM
    """The width of the strip profile [mm]."""
    height: MM
    """The height (thickness) of the strip profile [mm]."""
    name: str = "Strip Profile"
    """The name of the profile."""
    plotter: Callable[[Profile], plt.Figure] = plot_shapes
    """The plotter function to visualize the profile."""

    @property
    def max_profile_thickness(self) -> MM:
        """Maximum element thickness of the profile [mm]."""
        return min(self.width, self.height)

    @property
    def _polygon(self) -> Polygon:
        """Return the polygon of the strip profile."""
        return (
            # Start at top-left corner and go clockwise
            PolygonBuilder((0, 0))
            .append_line(length=self.width, angle=0)
            .append_line(length=self.height, angle=270)
            .append_line(length=self.width, angle=180)
            .append_line(length=self.height, angle=90)
            .generate_polygon()
        )

    def with_corrosion(self, corrosion: MM = 0) -> StripProfile:
        """Apply corrosion to the strip profile and return a new strip profile instance.

        The name attribute of the new instance will be updated to reflect the total corrosion applied
        including any previous corrosion indicated in the original name.

        Parameters
        ----------
        corrosion : MM, optional
            Corrosion per side (default is 0).
        """
        raise_if_negative(corrosion=corrosion)

        if corrosion == 0:
            return self

        width = self.width - corrosion * 2
        height = self.height - corrosion * 2

        if any(dimension <= FULL_CORROSION_TOLERANCE for dimension in (width, height)):
            raise ValueError("The profile has fully corroded.")

        name = update_name_with_corrosion(self.name, corrosion=corrosion)

        return StripProfile(
            width=width,
            height=height,
            name=name,
            plotter=self.plotter,
        )
