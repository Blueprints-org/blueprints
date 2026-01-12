"""Module for building and editing polygons."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

import numpy as np
from numpy.typing import NDArray
from shapely import transform
from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient
from shapely.validation import explain_validity

from blueprints.type_alias import CM, DEG, MM, M
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError

PointLike = tuple[float, float]
Length = TypeVar("Length", M, CM, MM)

# Numerical tolerance constants
# -----------------------------
# We treat values whose absolute magnitude is below these thresholds as zero.
# Rationale: these are several orders above floating noise (~1e-16) yet far
# below any meaningful geometric dimension or angle in typical structural
# section modeling contexts.
RADIUS_ZERO_ATOL: float = 1e-9  # length units (assumed meters --> 1 nano meter)
"""Absolute tolerance for radius values."""
SWEEP_ZERO_ATOL_DEG: DEG = 1e-10  # degrees
"""Absolute tolerance for sweep angles in degrees."""
DIRECTION_VECTOR_ROUND_DECIMALS: int = 15  # Because np.float64 has ~15-17 decimal digits of precision
"""Decimal places to round direction vectors to remove floating point noise."""
POLYGON_ENDPOINTS_CLOSE_ATOL: float = 1e-12  # length units (assumed meters --> 1 pico meter)
"""Absolute tolerance to consider polygon first and last points as equal."""


def merge_polygons(polygons: Sequence[Polygon]) -> Polygon:
    """Return the merged polygon of the cross-section polygons."""
    # check if there are any polygons
    if not polygons:
        raise ValueError("No polygons have been added to the cross-section.")

    # return the polygon of the first polygon if there is only one
    if len(polygons) == 1:
        return polygons[0]

    # Combine the polygons of all polygons if there is multiple
    combined_polygon: BaseGeometry = polygons[0]
    for polygon in polygons[1:]:
        combined_polygon = combined_polygon.union(polygon)

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

    def __init__(self, starting_point: PointLike) -> None:
        """Initialize an empty PolygonBuilder.

        Parameters
        ----------
        starting_point : PointLike
            Starting point of the polygon (x, y).
        """
        self._points: NDArray[np.float64] = np.array([starting_point], dtype=float)

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
        # Direction vector rounded to remove floating point noise
        # This improves accuracy when working with (factors of) right angles
        direction = np.round(np.array([np.cos(angle_in_radians), np.sin(angle_in_radians)], dtype=float), decimals=DIRECTION_VECTOR_ROUND_DECIMALS)
        new_point = self._current_point + length * direction

        self._points = np.concatenate((self._points, new_point[np.newaxis, :]), axis=0)

        return self

    def append_arc(self, sweep: DEG, angle: DEG, radius: Length, max_segment_angle: DEG = 5.0) -> PolygonBuilder:
        """Append a circular arc segment to the polygon from the current endpoint.

        Approach
        --------
        This method tessellates the arc into multiple straight line segments to approximate the curve.

        The intermediate points along the arc are calculated and added to the polygon.
        The intermediate points are calculated by dividing the total sweep angle into smaller segments.
        Each segment spans an angle not exceeding `max_segment_angle`.
        The vector from the arc center to the current endpoint is rotated incrementally to trace the arc and generate the points.

        Parameters
        ----------
        sweep : DEG
            Sweep angle of the arc segment in degrees;
            Positive values indicate counter-clockwise rotation, negative values indicate clockwise rotation.
        angle : DEG
            The tangent direction at the arc start in degrees;
            Angle is measured counter-clockwise from the positive x-axis;
            0° is along the positive x-axis, 90° is along the positive y-axis.
        radius : Length
            Radius of the arc segment. Must be positive.
            The sign of the radius is ignored; only its magnitude is used.
        max_segment_angle : DEG, optional
            Maximum central angle (degrees) per arc chord segment when tessellating arcs.
            This is used to determine the number of segments when creating circular arcs.
            Smaller values lead to finer tessellation and more points in the resulting polygon.
            Default is 5.0 degrees.

        Raises
        ------
        LessOrEqualToZeroError
            If `radius` is zero.
        LessOrEqualToZeroError
            If `max_segment_angle` is not positive.

        Raises
        ------
        ValueError
            If `radius` is zero.

        Returns
        -------
        PolygonBuilder
            The PolygonBuilder instance (for method chaining).
        """
        if np.isclose(sweep, 0.0, atol=SWEEP_ZERO_ATOL_DEG, rtol=0.0) or np.isclose(radius, 0.0, atol=RADIUS_ZERO_ATOL, rtol=0.0):
            # A zero sweep or radius does not change the geometry; simply return the builder.
            return self

        if radius < 0:  # ty:ignore[unsupported-operator]
            raise NegativeValueError(value_name="radius", value=radius)

        if max_segment_angle <= 0:
            raise LessOrEqualToZeroError(value_name="max_segment_angle", value=max_segment_angle)

        # Compute the center of the arc and the vector from the center to the start point.
        center = self._compute_arc_center(angle, sweep, radius)
        start_vector = self._current_point - center

        # Determine the number of segments to approximate the arc.
        segment_count = self._segment_count_for_arc(sweep, max_segment_angle)

        # Create the per-step rotation (cos,sin) series for the arc segments.
        rotation_series = self._arc_rotation_series(sweep, segment_count)

        # Generate the intermediate points along the arc and append them to the polygon.
        arc_points = self._generate_arc_vertices(center, start_vector, rotation_series)
        self._points = np.concatenate((self._points, arc_points), axis=0)

        return self

    def _compute_arc_center(self, angle: DEG, sweep: DEG, radius: Length) -> NDArray[np.float64]:
        """Return the coordinates of the arc center.

        The circle center lies along the `normal left` of the tangent direction at the arc start point.
        A positive sweep turns counter-clockwise, so the center is located to the
        left of the tangent; a negative sweep turns clockwise, placing the center
        to the right.

        Parameters
        ----------
        angle : DEG
            The tangent direction at the arc start in degrees;
            Angle is measured counter-clockwise from the positive x-axis;
            0° is along the positive x-axis, 90° is along the positive y-axis.
        sweep : DEG
            Sweep angle of the arc segment in degrees;
            Positive values indicate counter-clockwise rotation, negative values indicate clockwise rotation.
        radius : Length
            Radius of the arc segment. Must be non-zero.
            The sign of the radius is ignored; only its magnitude is used.

        Returns
        -------
        NDArray[np.float64]
            Coordinates of the arc center (x, y).
        """
        tangent_angle_rad = np.deg2rad(angle)
        # Direction vector rounded to remove floating point noise
        # This improves accuracy when working with (factors of) right angles
        normal_left = np.round(
            np.array([-np.sin(tangent_angle_rad), np.cos(tangent_angle_rad)], dtype=float), decimals=DIRECTION_VECTOR_ROUND_DECIMALS
        )
        turn_direction = np.sign(sweep)  # +1 for CCW (left), -1 for CW (right)

        return self._current_point + turn_direction * abs(radius) * normal_left

    def _segment_count_for_arc(self, sweep: DEG, max_segment_angle: DEG) -> int:
        """Return the tessellation segment count for a sweep angle.

        Parameters
        ----------
        sweep : DEG
            Sweep angle of the arc segment in degrees;
            Positive values indicate counter-clockwise rotation, negative values indicate clockwise rotation.
        max_segment_angle : DEG
            Maximum central angle (degrees) per arc chord segment when tessellating arcs.
            This is used to determine the number of segments when creating circular arcs.
            Smaller values lead to finer tessellation and more points in the resulting polygon.

        Returns
        -------
        int
            The number of segments to approximate the arc with a minimum of 1.
        """
        segments = int(np.ceil(abs(sweep) / max_segment_angle))
        return max(1, segments)

    @staticmethod
    def _arc_rotation_series(sweep: DEG, segment_count: int) -> NDArray[np.float64]:
        """Return per-step rotation (cos,sin) series for the arc.

        Parameters
        ----------
        sweep : DEG
            Sweep angle of the arc segment in degrees;
            Positive values indicate counter-clockwise rotation, negative values indicate clockwise rotation.
        segment_count : int
            Number of segments approximating the arc (>=1).

        Returns
        -------
        NDArray[np.float64]
            Array of shape (segment_count, 2) with columns [cos(k*θ), sin(k*θ)] for k=1..segment_count,
            where θ = sweep/segment_count in radians.
        """
        rotation_angle = np.deg2rad(sweep / segment_count)
        step_indices = np.arange(1, segment_count + 1, dtype=float)
        cosines = np.cos(step_indices * rotation_angle)
        sines = np.sin(step_indices * rotation_angle)
        return np.round(np.column_stack((cosines, sines)), decimals=DIRECTION_VECTOR_ROUND_DECIMALS)

    @staticmethod
    def _generate_arc_vertices(
        center: NDArray[np.float64],
        start_vector: NDArray[np.float64],
        rotation_series: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        """Return the coordinates tracing the arc, excluding the start point.

        Parameters
        ----------
        center : array-like of shape (2,)
            Coordinates of the circle center.
        start_vector : array-like of shape (2,)
            Vector from the center to the arc start point.
        rotation_series : array-like of shape (segment_count, 2)
            Columns [cos(k*θ), sin(k*θ)] for k = 1 .. segment_count.

        Returns
        -------
        NDArray[np.float64]
            Array of shape (segment_count, 2) containing the coordinates of the arc points.
        """
        # Rotate the single start vector by each angle: avoid repeating the vector in memory.
        x0, y0 = start_vector
        cosines, sines = rotation_series.T  # shapes (n,), (n,)
        rotated = np.column_stack((cosines * x0 - sines * y0, sines * x0 + cosines * y0))
        return center + rotated

    def generate_polygon(self, transform_centroid: bool = True) -> Polygon:
        """Generate and return a Shapely Polygon from the built points.

        Note that the polygon is automatically closed.

        Parameters
        ----------
        transform_centroid : bool, optional
            If True, the polygon is translated so that its centroid is at the origin (0, 0).
            Default is True.

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
        if len(self._points) < 3:
            raise ValueError("A polygon requires at least 3 points.")

        # If the first and last points are are within tolerance, we set them equal to ensure properly closed polygon.
        # This has to be done in all cases, because even if this polygon is valid now, further operations (like union)
        # may fail if the endpoints are not exactly equal.
        if np.allclose(self._points[0], self._points[-1], atol=POLYGON_ENDPOINTS_CLOSE_ATOL, rtol=0.0):
            self._points[-1] = self._points[0]

        polygon = Polygon(self._points)
        if not polygon.is_valid:
            validity_issues = explain_validity(polygon)
            raise ValueError(f"The constructed polygon is not valid: {validity_issues}")

        if transform_centroid:
            polygon = transform(polygon, lambda point: point - polygon.centroid.coords.__array__())

        return polygon
