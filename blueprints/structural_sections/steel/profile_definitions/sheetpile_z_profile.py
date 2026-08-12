"""Z-Shaped Sheet Pile Profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

import numpy as np
from matplotlib import pyplot as plt
from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

from blueprints.structural_sections._profile import Profile
from blueprints.structural_sections.steel.profile_definitions.corrosion_utils import (
    FULL_CORROSION_TOLERANCE,
    update_name_with_corrosion,
)
from blueprints.structural_sections.steel.profile_definitions.plotters.general_steel_plotter import (
    plot_shapes,
)
from blueprints.type_alias import DEG, MM


@dataclass(frozen=True, kw_only=True)
class SheetpileZProfile(Profile):
    """Representation of a Z-shaped sheet pile profile constructed from coordinates.

    Z-shaped sheet piles are interlocking structural elements used in retaining walls
    and cofferdams. AZ and PAZ profiles are standardized examples of Z-shaped sheet piles.

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
    name: str = "Z-Shaped Sheet Pile Profile"
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
        """Shapely Polygon representing the single sheet of the Z-shaped sheet pile profile from coordinates."""
        return Polygon(self.coordinates)

    @property
    def flange_to_web_angle(self) -> DEG:
        """Angle between the web and the (horizontal) flanges of the Z-shaped sheet pile profile [degrees].

        The angle is calculated by finding the edge of the web that intersects a horizontal line
        through the middle of the profile's bounding box.
        The angle is then computed using the arctangent of the rise over run of that edge.
        """
        # Get the bounding box of the profile
        xs = [x for x, _ in self.coordinates]
        ys = [y for _, y in self.coordinates]
        x_mid = (min(xs) + max(xs)) / 2
        y_mid = (min(ys) + max(ys)) / 2
        horizontal_line = LineString([(min(xs) - 1, y_mid), (max(xs) + 1, y_mid)])

        # Find the intersection points of the horizontal line with the profile boundary
        n = len(self.coordinates)
        candidate_edges = []
        for i in range(n):
            p1 = self.coordinates[i]
            p2 = self.coordinates[(i + 1) % n]
            point = LineString([p1, p2]).intersection(horizontal_line)
            if isinstance(point, Point):
                candidate_edges.append((point, p1, p2))

        if not candidate_edges:
            raise ValueError("Horizontal line through the middle of the bounding box does not intersect the profile boundary.")  # pragma: no cover

        # Find the edge whose intersection point is closest to the horizontal middle of the bounding box and compute the angle
        point, (x1, y1), (x2, y2) = min(candidate_edges, key=lambda edge: abs(edge[0].x - x_mid))
        return np.degrees(np.arctan2(abs(y2 - y1), abs(x2 - x1)))

    @property
    def width_of_flat_portion(self) -> MM:
        """Width of the flange of the Z-shaped sheet pile profile [mm].

        The flange width is calculated based on the height of the profile, the angle between the web and flange,
        the web thickness, and the interlocking center-to-center distance. The formula accounts for the geometry
        of the Z-shaped profile and the positioning of the flanges relative to the web.

        Based on the classification in table 5-1 in EN 1993-5.
        """
        height_of_profile = self._polygon_single_sheet.bounds[3] - self._polygon_single_sheet.bounds[1]
        width_of_web = height_of_profile / np.tan(np.radians(self.flange_to_web_angle))
        horizontal_thickness_web = self.web_thickness / np.sin(np.radians(self.flange_to_web_angle))
        return self.interlocking_ctc - width_of_web - horizontal_thickness_web

    @property
    def _polygon(self) -> Polygon:
        """Shapely Polygon representing the Z-shaped sheet pile profile from coordinates."""
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

    def multiple_sheets(self, number_of_sheets: int) -> SheetpileZProfile:
        """Return a new Z-shaped sheet pile profile instance with a different number of sheets.

        Parameters
        ----------
        number_of_sheets : int
            Number of sheets to use in the profile.

        Returns
        -------
        SheetpileZProfile
            A new profile instance with the specified number of sheets.

        Notes
        -----
        Multiple sheet functionality is implemented for coordinate-based Z-shaped sheet pile profiles.
        The `_polygon` property handles multi-sheet geometry by translating, mirroring (for odd-indexed sheets),
        and generating connectors between sheets. This method validates that `number_of_sheets >= 1`
        and returns a new instance with the updated sheet count.
        """
        if number_of_sheets < 1:
            raise ValueError("Number of sheets must be at least 1")
        return SheetpileZProfile(
            coordinates=self.coordinates,
            web_thickness=self.web_thickness,
            flange_thickness=self.flange_thickness,
            interlocking_ctc=self.interlocking_ctc,
            name=self.name,
            plotter=self.plotter,
            number_of_sheets=number_of_sheets,
        )

    def with_corrosion(self, corrosion: MM = 0) -> SheetpileZProfile:
        """Return a new Z-shaped sheet pile profile instance with corrosion applied.

        Parameters
        ----------
        corrosion : MM
            The amount of corrosion to apply to the profile [mm].

        Returns
        -------
        SheetpileZProfile
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

        coordinates: list[tuple[float, float]] = [(x, y) for x, y in corroded_polygon.exterior.coords]
        name = update_name_with_corrosion(self.name, corrosion=corrosion)

        return SheetpileZProfile(
            coordinates=coordinates,
            web_thickness=new_web_thickness,
            flange_thickness=new_flange_thickness,
            interlocking_ctc=self.interlocking_ctc,
            name=name,
            plotter=self.plotter,
            number_of_sheets=self.number_of_sheets,
        )
