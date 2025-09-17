"""Module for building and editing cross-sections."""

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
        set `MAX_SEGMENT_ANGLE_DEGREES` to control how finely arcs are tessellated (smaller = smoother, more vertices).
        Internally this maps to Shapely's buffer `resolution`.
    """

    MAX_SEGMENT_ANGLE_DEGREES = 5.0
    """Maximum central angle (degrees) per arc chord segment when tessellating arcs.
    This is used to determine the number of segments when creating circular arcs.
    Smaller values lead to finer tessellation and more points in the resulting polygon."""

    def __init__(self) -> None:
        """Initialize an empty PolygonBuilder."""
        self._points: NDArray[np.float64] = np.empty((0, 2), dtype=float)
        self._current: NDArray[np.float64] | None = None

    def set_starting_point(self, start: PointLike) -> PolygonBuilder:
        """Set the starting vertex for the polygon being constructed.

        Parameters
        ----------
        start : PointLike
            Starting point of the polygon (x, y).

        Returns
        -------
        PolygonBuilder
            The PolygonBuilder instance (for method chaining).
        """
        raise NotImplementedError

    def append_line(self, length: Length, angle: DEG) -> PolygonBuilder:
        """Append a straight line segment to the polygon from the current endpoint.

        Parameters
        ----------
        length : Length
            Length of the line segment.
        angle : DEG
            The tangent direction at the line start in degrees;
            0° is along the positive x-axis, 90° is along the positive y-axis.

        Returns
        -------
        PolygonBuilder
            The PolygonBuilder instance (for method chaining).
        """
        raise NotImplementedError

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

    def coordinates(self, as_array: bool = True) -> np.ndarray | tuple[tuple[float, float], ...]:
        """Get the coordinates of the points.

        Parameters
        ----------
        as_array : bool, optional
            If True, return as a NumPy array; otherwise, return as a tuple of PointLike tuples.
            Default is True.

        Returns
        -------
        np.ndarray or tuple[tuple[float, float], ...]
            The coordinates of the built polygon points.
        """
        raise NotImplementedError
