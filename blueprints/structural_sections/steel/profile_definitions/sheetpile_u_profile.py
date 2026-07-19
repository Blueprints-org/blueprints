"""U-Shaped Sheet Pile Profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import cast

from matplotlib import pyplot as plt
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.profile_definitions.corrosion_utils import (
    FULL_CORROSION_TOLERANCE,
    update_name_with_corrosion,
)
from blueprints.structural_sections.steel.profile_definitions.plotters.general_steel_plotter import (
    plot_shapes,
)
from blueprints.type_alias import MM


@dataclass(frozen=True, kw_only=True)
class SheetpileUProfile(Profile):
    """Representation of a U-shaped sheet pile profile constructed from coordinates.

    U-shaped sheet piles are interlocking structural elements used in retaining walls
    and cofferdams. AU and PU profiles are standardized examples of U-shaped sheet piles.

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
    name: str = "U-Shaped Sheet Pile Profile"
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
        """Shapely Polygon representing the single sheet of the U-shaped sheet pile profile from coordinates."""
        return Polygon(self.coordinates)

    @property
    def _polygon(self) -> Polygon:
        """Shapely Polygon representing the U-shaped sheet pile profile from coordinates."""
        single_sheet_polygon = self._polygon_single_sheet
        if self.number_of_sheets == 1:
            return single_sheet_polygon

        # Get ymax and ymin of the single sheet
        bounds = single_sheet_polygon.bounds
        xmin = bounds[0]
        xmax = bounds[2]

        # Create list to hold all sheet polygons and connectors
        polygons = []

        for i in range(self.number_of_sheets):
            # Every second polygon (odd indices) should be mirrored vertically
            if i % 2 == 1:
                # Mirror along horizontal line: reflect across y=0 (negate y values)
                mirrored_polygon = affinity.scale(single_sheet_polygon, xfact=-1, yfact=-1, origin=((xmin + xmax) / 2, 0))
                # Then translate the mirrored polygon horizontally
                translated_polygon = affinity.translate(mirrored_polygon, xoff=i * self.interlocking_ctc)
                polygons.append(translated_polygon)
            else:
                # Translate the polygon horizontally
                translated_polygon = affinity.translate(single_sheet_polygon, xoff=i * self.interlocking_ctc)
                polygons.append(translated_polygon)

            # Add connector rectangle between sheets (except after the last sheet)
            if i < self.number_of_sheets - 1:
                # Find the point where x is maximum in the single sheet polygon
                coords = list(single_sheet_polygon.exterior.coords)
                max_x_point = max(coords, key=lambda pt: pt[0])
                max_x = max_x_point[0]
                max_x_y = max_x_point[1]

                # Find the point where x is minimum in the single sheet polygon
                coords = list(single_sheet_polygon.exterior.coords)
                min_x_point = min(coords, key=lambda pt: (pt[0], pt[1]))
                min_x = min_x_point[0]
                min_x_y = min_x_point[1]

                # Connector position at halfway between sheets
                connector_height = 1
                connector = box(
                    max_x + self.interlocking_ctc * i,
                    (min_x_y + max_x_y) / 2 - connector_height / 2,
                    min_x + self.interlocking_ctc * (i + 1),
                    (min_x_y + max_x_y) / 2 + connector_height / 2,
                )
                polygons.append(connector)

        # Union all polygons into a single polygon
        return cast(Polygon, unary_union(polygons))

    def multiple_sheets(self, number_of_sheets: int) -> SheetpileUProfile:
        """Return a new U-shaped sheet pile profile instance with a different number of sheets.

        Parameters
        ----------
        number_of_sheets : int
            Number of sheets to use in the profile.

        Returns
        -------
        SheetpileUProfile
            A new profile instance with the specified number of sheets.

        Notes
        -----
        Multiple sheet functionality is implemented for coordinate-based U-shaped sheet pile profiles.
        The `_polygon` property handles multi-sheet geometry by translating each sheet horizontally
        and generating connectors between sheets. This method validates that `number_of_sheets >= 1`
        and returns a new instance with the updated sheet count.
        """
        if number_of_sheets < 1:
            raise ValueError("Number of sheets must be at least 1")
        return replace(self, number_of_sheets=number_of_sheets)

    def with_corrosion(self, corrosion: MM = 0) -> SheetpileUProfile:
        """Return a new U-shaped sheet pile profile instance with corrosion applied.

        Parameters
        ----------
        corrosion : MM
            The amount of corrosion to apply to the profile [mm].

        Returns
        -------
        SheetpileUProfile
            A new profile instance with the specified corrosion applied.

        Notes
        -----
        Corrosion is applied on both sides of the profile, reducing the thickness of the web and flanges by 2 times the corrosion value.
        If corrosion from one side is different than the other, it is suggested to apply the average corrosion value.
        """
        if corrosion < 0:
            raise ValueError("Corrosion value must be non-negative")

        # Corrosion reduces the thickness of the web and flanges by 2 times the corrosion value (corrosion on both sides)
        new_web_thickness = self.web_thickness - 2 * corrosion
        new_flange_thickness = self.flange_thickness - 2 * corrosion

        # Check if profile has fully corroded
        if new_web_thickness <= FULL_CORROSION_TOLERANCE or new_flange_thickness <= FULL_CORROSION_TOLERANCE:
            raise ValueError("The profile has fully corroded.")

        # Apply corrosion by buffering the polygon inward by the corrosion amount
        corroded_polygon = self._polygon_single_sheet.buffer(-corrosion)

        coordinates = list(corroded_polygon.exterior.coords)
        name = update_name_with_corrosion(self.name, corrosion=corrosion)

        return replace(
            self,
            coordinates=coordinates,
            web_thickness=new_web_thickness,
            flange_thickness=new_flange_thickness,
            name=name,
        )
