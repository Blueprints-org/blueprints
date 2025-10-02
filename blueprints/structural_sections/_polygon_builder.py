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

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.type_alias import CM, DEG, MM, M
from blueprints.validations import LessOrEqualToZeroError

PointLike = tuple[float, float]
Length = TypeVar("Length", M, CM, MM)

# Numerical tolerance constants
# -----------------------------
# We treat values whose absolute magnitude is below these thresholds as zero.
# Rationale: these are several orders above floating noise (~1e-16) yet far
# below any meaningful geometric dimension or angle in typical structural
# section modeling contexts.
RADIUS_ZERO_ATOL: float = 1e-9  # length units (assumed meters --> 1 nm)
"""Absolute tolerance for radius values."""
SWEEP_ZERO_ATOL_DEG: float = 1e-10  # degrees
"""Absolute tolerance for sweep angles in degrees."""
DIRECTION_VECTOR_ROUND_DECIMALS: int = 15  # Because np.float64 has ~15-17 decimal digits of precision
"""Decimal places to round direction vectors to remove floating point noise."""


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

    def __init__(self, starting_point: PointLike) -> None:
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

        Raises
        ------
        ValueError
            If `max_segment_angle` is not positive.
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
            Radius of the arc segment. Must be non-zero.
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
        if np.isclose(radius, 0.0, atol=RADIUS_ZERO_ATOL, rtol=0.0):
            raise LessOrEqualToZeroError(value_name="radius", value=radius)

        if np.isclose(sweep, 0.0, atol=SWEEP_ZERO_ATOL_DEG, rtol=0.0):
            # A zero sweep does not change the geometry; simply return the builder.
            return self

        if max_segment_angle <= 0:
            raise LessOrEqualToZeroError(value_name="max_segment_angle", value=max_segment_angle)

        # Compute the center of the arc and the vector from the center to the start point.
        center = self._compute_arc_center(angle, sweep, radius)
        start_vector = self._current_point - center

        # Determine the number of segments to approximate the arc.
        segment_count = self._segment_count_for_arc(sweep, max_segment_angle)

        # Create the rotation matrix for the arc segments. Rotation matrix will be applied repeatedly to the start_vector.
        rotation = self._rotation_matrix(sweep, segment_count)

        # Generate the intermediate points along the arc and append them to the polygon.
        arc_points = self._generate_arc_vertices(center, start_vector, rotation, segment_count)
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
    def _rotation_matrix(sweep: DEG, segment_count: int) -> NDArray[np.float64]:
        """Return a 2D rotation matrix for the per-segment sweep angle.

        This matrix can be used to rotate a vector in 2D space.

        Parameters
        ----------
        sweep : DEG
            Sweep angle of the arc segment in degrees;
            Positive values indicate counter-clockwise rotation, negative values indicate clockwise rotation.
        segment_count : int
            The number of segments to approximate the arc.

        Returns
        -------
        NDArray[np.float64]
            A 2x2 rotation matrix.
        """
        rotation_angle = np.deg2rad(sweep / segment_count)
        cosine = np.cos(rotation_angle)
        sine = np.sin(rotation_angle)
        return np.array([[cosine, -sine], [sine, cosine]], dtype=float)

    @staticmethod
    def _generate_arc_vertices(
        center: NDArray[np.float64],
        start_vector: NDArray[np.float64],
        rotation: NDArray[np.float64],
        segment_count: int,
    ) -> NDArray[np.float64]:
        """Return the coordinates tracing the arc, excluding the start point.

        Parameters
        ----------
        center : array-like of shape (2,)
            Coordinates of the circle center.
        start_vector : array-like of shape (2,)
            Vector from the center to the arc start point.
        rotation : array-like of shape (2, 2)
            Rotation matrix for the per-segment sweep angle.
        segment_count : int
            Number of chord segments tessellating the arc.

        Returns
        -------
        NDArray[np.float64]
            Array of shape (segment_count, 2) containing the coordinates of the arc points.
        """
        rotation_angle = np.arctan2(rotation[1, 0], rotation[0, 0])
        # Build the rotation series for each tessellation step without a Python loop.
        step_indices = np.arange(1, segment_count + 1, dtype=float)
        cosines = np.cos(step_indices * rotation_angle)
        sines = np.sin(step_indices * rotation_angle)

        # Broadcast the start vector so each row can be rotated via element-wise trig.
        base_vectors = np.repeat(start_vector[np.newaxis, :], segment_count, axis=0)
        x_components = base_vectors[:, 0]
        y_components = base_vectors[:, 1]

        rotated = np.empty_like(base_vectors)
        rotated[:, 0] = cosines * x_components - sines * y_components
        rotated[:, 1] = sines * x_components + cosines * y_components

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

        polygon = Polygon(self._points)
        if not polygon.is_valid:
            raise ValueError("The constructed polygon is not valid.")

        if transform_centroid:
            polygon = transform(polygon, lambda point: point - polygon.centroid.coords.__array__())

        return polygon
