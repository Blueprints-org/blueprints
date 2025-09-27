"""Module for building and editing polygons."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

import numpy as np
from numpy.typing import NDArray
from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import CM, DEG, MM, M

PointLike = tuple[float, float]
Length = TypeVar("Length", M, CM, MM)


def merge_polygons(elements: Sequence[CrossSection]) -> Polygon:
    """Return the merged polygon of the cross-section elements."""
    # check if there are any elements
    if not elements:
        raise ValueError("No elements have been added to the cross-section.")

    # return the polygon of the first element if there is only one
    if len(elements) == 1:
        return elements[0].polygon

    # Combine the polygons of all elements if there is multiple
    combined_polygon: BaseGeometry = elements[0].polygon
    for element in elements[1:]:
        combined_polygon = combined_polygon.union(element.polygon)

    # Ensure the result is a valid Polygon
    if not isinstance(combined_polygon, Polygon):
        raise TypeError("The combined geometry is not a valid Polygon.")

    # Ensure consistent orientation
    return orient(combined_polygon)


class PolygonBuilder:
    """Class for building and editing planar polygons from straight lines and circular arcs.

    Notes
    -----
    `Smoothness`:
        set `max_segment_angle` to control how finely arcs are tessellated (smaller = smoother, more vertices).
        Internally this maps to Shapely's buffer `resolution`.
    """

    def __init__(self, starting_point: PointLike, max_segment_angle: DEG = 5.0) -> None:
        """Initialize an empty PolygonBuilder.

        Parameters
        ----------
        starting_point : PointLike
            Starting point of the polygon (x, y).
        max_segment_angle : DEG, optional
            Maximum central angle (degrees) per arc chord segment when tessellating arcs.
            This is used to determine the number of segments when creating circular arcs.
            Smaller values lead to finer tessellation and more points in the resulting polygon.
            Default is 5.0 degrees.
        """
        self._points: NDArray[np.float64] = np.array([starting_point], dtype=float)
        self._max_segment_angle = max_segment_angle

    @property
    def _current_point(self) -> NDArray[np.float64]:
        """Get the current endpoint of the polygon."""
        return self._points[-1]

    def append_line(self, length: Length, angle: DEG) -> PolygonBuilder:
        """Append a straight line segment to the polygon from the current endpoint.

        Parameters
        ----------
        length : Length
            Length of the line segment.
        angle : DEG
            The tangent direction at the line start in degrees;
            Angle is measured counter-clockwise from the positive x-axis;
            0° is along the positive x-axis, 90° is along the positive y-axis.

        Returns
        -------
        PolygonBuilder
            The PolygonBuilder instance (for method chaining).
        """
        angle_in_radians = np.deg2rad(angle)
        direction = np.array([np.cos(angle_in_radians), np.sin(angle_in_radians)], dtype=float)
        new_point = self._current_point + length * direction

        self._points = np.concatenate((self._points, new_point[np.newaxis, :]), axis=0)

        return self

    def append_arc(self, sweep: DEG, angle: DEG, radius: Length) -> PolygonBuilder:
        """Append a circular arc segment to the polygon from the current endpoint.

        Parameters
        ----------
        sweep : DEG
            Sweep angle of the arc segment in degrees;
            Positive values indicate counter-clockwise rotation, negative values indicate clockwise rotation.
        angle : DEG
            The tangent direction at the arc start in degrees;
            0° is along the positive x-axis, 90° is along the positive y-axis.
        radius : Length
            Radius of the arc segment. Must be non-zero.
            The sign of the radius is ignored; only its magnitude is used.

        Returns
        -------
        PolygonBuilder
            The PolygonBuilder instance (for method chaining).
        """
        raise NotImplementedError

    def create_polygon(self) -> Polygon:
        """Create and return a Shapely Polygon from the built points.

        Returns
        -------
        Polygon
            A Shapely Polygon object representing the built polygon.

        Raises
        ------
        ValueError
            If there are fewer than 3 points to form a polygon.
            If the constructed polygon is not valid.
        """
        raise NotImplementedError
