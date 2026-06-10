"""AZ Profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import cast

from matplotlib import pyplot as plt
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.profile_definitions.plotters.general_steel_plotter import (
    plot_shapes,
)
from blueprints.type_alias import MM


@dataclass(frozen=True, kw_only=True)
class AZProfile(Profile):
    """Representation of an AZ sheet pile profile constructed from coordinates.

    Attributes
    ----------
    coordinates : list[tuple[float, float]]
        List of (x, y) coordinate tuples defining the profile geometry.
    web_thickness : MM
        Thickness of the web [mm].
    flange_thickness : MM
        Thickness of the flanges [mm].
    interlocking_ctc : MM
        Center to center distance of the sheets (interlocking distance) [mm].
    name : str
        Name of the profile.
    plotter : Callable[[Profile], plt.Figure]
        The plotter function to visualize the profile.
    number_of_sheets : int
        Number of sheets in the profile.

    Notes
    -----
    The `perimeter` property is inherited from the Profile base class.
    """

    coordinates: list[tuple[float, float]]
    """List of (x, y) coordinate tuples defining the profile geometry."""
    web_thickness: MM
    """Thickness of the web [mm]."""
    flange_thickness: MM
    """Thickness of the flanges [mm]."""
    interlocking_ctc: MM
    """Center to center distance of the sheets (interlocking distance) [mm]."""
    name: str = "AZ Profile"
    """Name of the profile."""
    plotter: Callable[[Profile], plt.Figure] = plot_shapes
    """The plotter function to visualize the profile."""
    number_of_sheets: int = 1
    """Number of sheets in the profile."""

    @property
    def max_thickness(self) -> MM:
        """Maximum element thickness of the profile [mm]."""
        return max(self.web_thickness, self.flange_thickness)

    @property
    def _polygon_single_sheet(self) -> Polygon:
        """Shapely Polygon representing the single sheet of the AZ profile from coordinates."""
        return Polygon(self.coordinates)

    @property
    def _polygon(self) -> Polygon:
        """Shapely Polygon representing the AZ profile from coordinates."""
        single_sheet_polygon = self._polygon_single_sheet
        if self.number_of_sheets == 1:
            return single_sheet_polygon

        # Get ymax and ymin of the single sheet
        bounds = single_sheet_polygon.bounds
        ymin = bounds[1]
        ymax = bounds[3]

        # Create list to hold all sheet polygons and connectors
        polygons = []

        for i in range(self.number_of_sheets):
            # Translate the polygon horizontally
            translated_polygon = affinity.translate(single_sheet_polygon, xoff=i * self.interlocking_ctc)

            # Every second polygon (odd indices) should be mirrored along horizontal line at ymax
            if i % 2 == 1:
                # Mirror along horizontal line: reflect across y=ymax
                # This means new_y = 2*ymax - old_y
                mirrored_polygon = affinity.scale(translated_polygon, xfact=1, yfact=-1)
                polygons.append(mirrored_polygon)
            else:
                polygons.append(translated_polygon)

            # Add connector rectangle between sheets (except after the last sheet)
            if i < self.number_of_sheets - 1:
                # Connector position at halfway between sheets
                connector_x = (i + 1) * self.interlocking_ctc
                connector_width = self.interlocking_ctc / 4
                connector_height = 1
                connector_y = ymax - connector_height / 2 if i % 2 == 0 else ymin + connector_height / 2  # Alternate y position for connectors
                connector = box(
                    connector_x - connector_width / 2,
                    connector_y - connector_height / 2,
                    connector_x + connector_width / 2,
                    connector_y + connector_height / 2,
                )
                polygons.append(connector)

        # Union all polygons into a single polygon
        return cast(Polygon, unary_union(polygons))

    def multiple_sheets(self, number_of_sheets: int) -> AZProfile:
        """Return a new AZ profile instance with a different number of sheets.

        Parameters
        ----------
        number_of_sheets : int
            Number of sheets to use in the profile.

        Returns
        -------
        AZProfile
            A new profile instance with the specified number of sheets.

        Notes
        -----
        Multiple sheet functionality is not yet implemented for coordinate-based AZ profiles.
        This method is provided for API compatibility but currently only supports single sheets.
        """
        if number_of_sheets < 1:
            raise ValueError("Number of sheets must be at least 1")
        return replace(self, number_of_sheets=number_of_sheets)

    def with_corrosion(self, corrosion: MM = 0) -> AZProfile:
        """Return a new AZ profile instance with corrosion applied.

        Parameters
        ----------
        corrosion : MM
            The amount of corrosion to apply to the profile [mm].

        Returns
        -------
        AZProfile
            A new profile instance with the specified corrosion applied.

        Notes
        -----
        Corrosion is applied on both sides of the profile, reducing the thickness of the web and flanges by 2 times the corrosion value.
        If corrosion from one side is different than the other, it is suggested to apply the average corrosion value.
        """
        if corrosion < 0:
            raise ValueError("Corrosion value must be non-negative")

        # Corrosion reduces the thickness of the web and flanges by 2 times the corrosion value (corrosion on both sides)
        new_web_thickness = max(self.web_thickness - 2 * corrosion, 0)
        new_flange_thickness = max(self.flange_thickness - 2 * corrosion, 0)

        # Apply corrosion by buffering the polygon inward by the corrosion amount
        corroded_polygon = self._polygon_single_sheet.buffer(-corrosion)
        if corroded_polygon.is_empty:
            raise ValueError("Corrosion amount is too large, resulting in an empty profile")

        coordinates = list(corroded_polygon.exterior.coords)

        return replace(
            self,
            coordinates=coordinates,
            web_thickness=new_web_thickness,
            flange_thickness=new_flange_thickness,
            name=f"{self.name} with {corrosion} mm corrosion",
        )
