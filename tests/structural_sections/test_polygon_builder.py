"""Tests for the cross-section builder module."""

from itertools import pairwise

import numpy as np
import pytest
from shapely.geometry import Polygon

from blueprints.structural_sections._polygon_builder import PolygonBuilder, merge_polygons
from blueprints.structural_sections.geometric_cross_sections import RectangularCrossSection
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestMergePolygons:
    """Tests for the merge_polygons function."""

    def test_merge_polygons_empty_list(self) -> None:
        """Test that ValueError is raised when an empty list is provided."""
        with pytest.raises(ValueError, match=r"No elements have been added to the cross-section."):
            merge_polygons([])

    def test_merge_polygons_single_element(self) -> None:
        """Test that the polygon of a single element is returned unchanged."""
        rect = RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0)
        elements = [rect]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        assert result.equals(rect.polygon)

    def test_merge_polygons_two_touching_rectangles(self) -> None:
        """Test merging two rectangles that are touching (edge-to-edge)."""
        rect1 = RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0)
        rect2 = RectangularCrossSection(width=97.73, height=203.45, x=97.73, y=0.0)  # Touching at edge
        elements = [rect1, rect2]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        # The result should have an area equal to the sum of both rectangles
        expected_area = rect1.area + rect2.area
        assert result.area == pytest.approx(expected_area, rel=1e-6)

    def test_merge_polygons_two_overlapping_rectangles(self) -> None:
        """Test merging two overlapping rectangles."""
        rect1 = RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0)
        rect2 = RectangularCrossSection(width=97.73, height=203.45, x=48.87, y=0.0)  # 50% overlap
        elements = [rect1, rect2]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        # The result should have an area less than the sum due to overlap
        individual_area = rect1.area
        # Calculate overlap: rect1 center at 0, extends from -48.865 to +48.865
        # rect2 center at 48.87, extends from 0.005 to 97.735
        # Overlap is from 0.005 to 48.865 = 48.86 width
        overlap_area = 48.86 * 203.45  # more precise overlap width * height
        expected_area = 2 * individual_area - overlap_area
        assert result.area == pytest.approx(expected_area, rel=1e-3)

    def test_merge_polygons_three_rectangles_forming_t_shape(self) -> None:
        """Test merging three rectangles forming a T-shape."""
        # Horizontal bar of T
        rect1 = RectangularCrossSection(width=296.84, height=51.22, x=0.0, y=76.83)
        # Vertical bar of T (left part)
        rect2 = RectangularCrossSection(width=51.22, height=102.44, x=-73.11, y=0.0)
        # Vertical bar of T (right part)
        rect3 = RectangularCrossSection(width=51.22, height=102.44, x=73.11, y=0.0)
        elements = [rect1, rect2, rect3]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        # Total area should be sum of all three rectangles
        expected_area = rect1.area + rect2.area + rect3.area
        assert result.area == pytest.approx(expected_area, rel=1e-6)

    def test_merge_polygons_multiple_rectangles_complex_shape(self) -> None:
        """Test merging multiple rectangles creating a more complex shape."""
        # Create a plus sign shape with 5 rectangles
        center = RectangularCrossSection(width=97.73, height=102.44, x=0.0, y=0.0)
        top = RectangularCrossSection(width=48.87, height=51.22, x=0.0, y=76.83)
        bottom = RectangularCrossSection(width=48.87, height=51.22, x=0.0, y=-76.83)
        left = RectangularCrossSection(width=51.22, height=48.87, x=-74.47, y=0.0)
        right = RectangularCrossSection(width=51.22, height=48.87, x=74.47, y=0.0)
        elements = [center, top, bottom, left, right]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        # Check that the result is valid
        assert result.is_valid
        # The area should be less than sum due to overlaps but greater than the center rectangle
        total_individual_area = center.area + top.area + bottom.area + left.area + right.area
        assert result.area < total_individual_area  # Due to overlaps
        assert result.area > center.area  # Should be larger than just the center

    def test_merge_polygons_identical_rectangles(self) -> None:
        """Test merging identical rectangles (complete overlap)."""
        rect1 = RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0)
        rect2 = RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0)
        elements = [rect1, rect2]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        # Area should be the same as one rectangle since they completely overlap
        assert result.area == pytest.approx(rect1.area, rel=1e-6)

    def test_merge_polygons_rectangles_forming_l_shape(self) -> None:
        """Test merging two rectangles forming an L-shape."""
        # Horizontal part of L
        rect1 = RectangularCrossSection(width=194.67, height=51.22, x=0.0, y=0.0)
        # Vertical part of L (overlapping with horizontal part)
        rect2 = RectangularCrossSection(width=48.87, height=153.66, x=-72.90, y=25.61)
        elements = [rect1, rect2]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        # Calculate expected area: both rectangles minus the overlap
        overlap_area = 48.87 * 51.22  # overlap width x height
        expected_area = rect1.area + rect2.area - overlap_area
        assert result.area == pytest.approx(expected_area, rel=1e-6)

    def test_merge_polygons_concentric_rectangles(self) -> None:
        """Test merging concentric rectangles (one inside another)."""
        # Outer rectangle
        rect1 = RectangularCrossSection(width=194.67, height=307.22, x=0.0, y=0.0)
        # Inner rectangle (completely inside the outer one)
        rect2 = RectangularCrossSection(width=97.33, height=153.61, x=0.0, y=0.0)
        elements = [rect1, rect2]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        # Area should be the same as the larger rectangle
        assert result.area == pytest.approx(rect1.area, rel=1e-6)

    def test_merge_polygons_connected_rectangles_at_corners(self) -> None:
        """Test merging rectangles that connect at corners."""
        # Four rectangles forming a pinwheel pattern - they touch at corners
        center_x, center_y = 0.0, 0.0
        size = 48.87

        top_right = RectangularCrossSection(width=size, height=size, x=center_x + size / 2, y=center_y + size / 2)
        top_left = RectangularCrossSection(width=size, height=size, x=center_x - size / 2, y=center_y + size / 2)
        bottom_left = RectangularCrossSection(width=size, height=size, x=center_x - size / 2, y=center_y - size / 2)
        bottom_right = RectangularCrossSection(width=size, height=size, x=center_x + size / 2, y=center_y - size / 2)
        elements = [top_right, top_left, bottom_left, bottom_right]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        # Total area should be sum of all four rectangles
        expected_area = top_right.area + top_left.area + bottom_left.area + bottom_right.area
        assert result.area == pytest.approx(expected_area, rel=1e-6)

    def test_merge_polygons_result_is_oriented(self) -> None:
        """Test that the result polygon has consistent orientation."""
        rect1 = RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0)
        rect2 = RectangularCrossSection(width=97.73, height=203.45, x=97.73, y=0.0)  # Touching at edge
        elements = [rect1, rect2]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        # Check that the polygon is properly oriented (should be counter-clockwise for exterior)
        assert result.is_valid
        # The exterior ring should be counter-clockwise oriented
        coords = list(result.exterior.coords)
        # For a properly oriented polygon, the signed area should be positive
        signed_area = 0.5 * sum((x1 * y2 - x2 * y1) for (x1, y1), (x2, y2) in pairwise(coords))
        assert signed_area > 0  # Counter-clockwise orientation

    def test_merge_polygons_overlapping_rectangles_different_sizes(self) -> None:
        """Test merging rectangles of different sizes with overlaps."""
        small_rect = RectangularCrossSection(width=48.87, height=51.22, x=0.0, y=0.0)
        medium_rect = RectangularCrossSection(width=97.73, height=102.44, x=73.30, y=0.0)  # partial overlap
        large_rect = RectangularCrossSection(width=194.67, height=204.88, x=0.0, y=127.66)  # overlaps with small_rect
        elements = [small_rect, medium_rect, large_rect]

        result = merge_polygons(elements)

        assert isinstance(result, Polygon)
        assert result.is_valid
        # The area should be less than the sum of individual areas due to overlaps
        total_individual_area = small_rect.area + medium_rect.area + large_rect.area
        assert result.area <= total_individual_area
        assert result.area > 0

    def test_merge_polygons_maintains_polygon_type(self) -> None:
        """Test that merge_polygons always returns a Polygon object."""
        # Test with various configurations that result in connected shapes
        configurations = [
            # Single rectangle
            [RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0)],
            # Two touching rectangles
            [RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0), RectangularCrossSection(width=97.73, height=203.45, x=97.73, y=0.0)],
            # Three overlapping rectangles
            [
                RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0),
                RectangularCrossSection(width=97.73, height=203.45, x=78.18, y=0.0),
                RectangularCrossSection(width=97.73, height=203.45, x=156.37, y=0.0),
            ],
        ]

        for elements in configurations:
            result = merge_polygons(elements)
            assert isinstance(result, Polygon)
            assert result.is_valid

    def test_merge_polygons_disconnected_rectangles_raises_error(self) -> None:
        """Test that merging disconnected rectangles raises TypeError."""
        # Two rectangles that don't touch or overlap
        rect1 = RectangularCrossSection(width=97.73, height=203.45, x=0.0, y=0.0)
        rect2 = RectangularCrossSection(width=97.73, height=203.45, x=195.46, y=0.0)  # Gap between them
        elements = [rect1, rect2]

        with pytest.raises(TypeError, match=r"The combined geometry is not a valid Polygon."):
            merge_polygons(elements)


class TestPolygonBuilder:
    """Tests for the PolygonBuilder class."""

    def test_init_starts_with_starting_point(self) -> None:
        """The builder initializes with the given starting point."""
        starting_point = (1.5, -2.0)

        builder = PolygonBuilder(starting_point)

        assert builder._points.shape == (1, 2)  # noqa: SLF001
        np.testing.assert_allclose(builder._points[0], starting_point)  # noqa: SLF001
        np.testing.assert_allclose(builder._current_point, starting_point)  # noqa: SLF001

    def test_append_line_appends_point(self) -> None:
        """Appending a line adds a new point and updates the current endpoint."""
        builder = PolygonBuilder((0.0, 0.0))

        result = builder.append_line(5.0, 0.0)

        assert result is builder
        assert builder._points.shape == (2, 2)  # noqa: SLF001
        np.testing.assert_allclose(builder._points[-1], (5.0, 0.0))  # noqa: SLF001
        np.testing.assert_allclose(builder._current_point, (5.0, 0.0))  # noqa: SLF001

    def test_append_line_respects_angle(self) -> None:
        """The endpoint reflects the given heading angle."""
        builder = PolygonBuilder((1.5, -2.0))

        builder.append_line(2.0 * np.sqrt(2), 45.0)

        np.testing.assert_allclose(builder._points[-1], (3.5, 0.0), atol=1e-10)  # noqa: SLF001
        np.testing.assert_allclose(builder._current_point, (3.5, 0.0), atol=1e-10)  # noqa: SLF001

    def test_append_line_supports_chaining(self) -> None:
        """Multiple calls extend the path while keeping the current point updated."""
        builder = PolygonBuilder((0.0, 0.0))

        builder.append_line(2.0, 0.0).append_line(2.0, 90.0)

        assert builder._points.shape == (3, 2)  # noqa: SLF001
        np.testing.assert_allclose(builder._points[-1], (2.0, 2.0))  # noqa: SLF001

    def test_append_line_negative_length(self) -> None:
        """Appending a line with negative length moves backwards."""
        builder = PolygonBuilder((0.0, 1.0))

        builder.append_line(-3.0, 180.0)

        assert builder._points.shape == (2, 2)  # noqa: SLF001
        np.testing.assert_allclose(builder._points[-1], (3.0, 1.0))  # noqa: SLF001
        np.testing.assert_allclose(builder._current_point, (3.0, 1.0))  # noqa: SLF001

    def test_append_line_non_standard_angle(self) -> None:
        """Appending a line at a non-standard angle places the endpoint correctly."""
        builder = PolygonBuilder((0.0, 0.0))

        builder.append_line(10.0, 30.0)

        expected_x = 10.0 * np.cos(np.deg2rad(30.0))
        expected_y = 10.0 * np.sin(np.deg2rad(30.0))
        assert builder._points.shape == (2, 2)  # noqa: SLF001
        np.testing.assert_allclose(builder._points[-1], (expected_x, expected_y))  # noqa: SLF001
        np.testing.assert_allclose(builder._current_point, (expected_x, expected_y))  # noqa: SLF001

    def test_append_arc_with_invalid_max_segment_angle_raises(self) -> None:
        """A non-positive maximum segment angle raises a LessOrEqualToZeroError."""
        builder = PolygonBuilder((0.0, 0.0))
        with pytest.raises(LessOrEqualToZeroError, match=r"(?i)'max_segment_angle' must be greater than zero\.?$"):
            builder.append_arc(45.0, 0.0, 5.0, max_segment_angle=0.0)

        with pytest.raises(LessOrEqualToZeroError, match=r"(?i)'max_segment_angle' must be greater than zero\.?$"):
            builder.append_arc(45.0, 0.0, 5.0, max_segment_angle=-10.0)

    def test_append_arc_with_changing_max_segment_angle(self) -> None:
        """Changing the maximum segment angle affects the number of segments created."""
        builder = PolygonBuilder((0.0, 0.0))

        builder.append_arc(90.0, 0.0, 5.0, max_segment_angle=30.0)
        expected_segments_30 = int(np.ceil(90.0 / 30.0))
        assert builder._points.shape == (expected_segments_30 + 1, 2)  # noqa: SLF001

        builder.append_arc(90.0, 90.0, 5.0, max_segment_angle=10.0)
        expected_segments_10 = int(np.ceil(90.0 / 10.0))
        assert builder._points.shape == (expected_segments_30 + expected_segments_10 + 1, 2)  # noqa: SLF001

    def test_append_arc_ccw_quarter_circle(self) -> None:
        """A positive sweep generates a counter-clockwise arc with expected end point."""
        builder = PolygonBuilder((0.0, 0.0))

        builder.append_arc(90.0, 0.0, 5.0, max_segment_angle := 10.0)

        expected_segments = int(np.ceil(90.0 / max_segment_angle))
        assert builder._points.shape == (expected_segments + 1, 2)  # noqa: SLF001
        np.testing.assert_allclose(builder._points[-1], (5.0, 5.0), atol=1e-10)  # noqa: SLF001

        # All generated points remain on the circle centred at (0, 5) with radius 5.
        center = np.array((0.0, 5.0))
        distances = np.linalg.norm(builder._points - center, axis=1)  # noqa: SLF001
        np.testing.assert_allclose(distances, 5.0, atol=1e-9)

    def test_append_arc_cw_quarter_circle(self) -> None:
        """A negative sweep turns clockwise and reaches the expected end point."""
        builder = PolygonBuilder((0.0, 0.0))

        builder.append_arc(-90.0, 0.0, 5.0, max_segment_angle := 10.0)

        expected_segments = int(np.ceil(90.0 / max_segment_angle))
        assert builder._points.shape == (expected_segments + 1, 2)  # noqa: SLF001
        np.testing.assert_allclose(builder._points[-1], (5.0, -5.0), atol=1e-10)  # noqa: SLF001

        center = np.array((0.0, -5.0))
        distances = np.linalg.norm(builder._points - center, axis=1)  # noqa: SLF001
        np.testing.assert_allclose(distances, 5.0, atol=1e-9)

    def test_append_arc_zero_sweep_no_op(self) -> None:
        """Zero sweep leaves the point list unchanged and returns the builder."""
        builder = PolygonBuilder((1.0, 2.0))
        points_before = builder._points.copy()  # noqa: SLF001

        result = builder.append_arc(0.0, 0.0, 5.0)

        assert result is builder
        np.testing.assert_array_equal(builder._points, points_before)  # noqa: SLF001

    def test_append_arc_zero_radius_no_op(self) -> None:
        """Zero radius leaves the point list unchanged and returns the builder."""
        builder = PolygonBuilder((1.0, 2.0))
        points_before = builder._points.copy()  # noqa: SLF001

        result = builder.append_arc(45.0, 0.0, 0.0)

        assert result is builder
        np.testing.assert_array_equal(builder._points, points_before)  # noqa: SLF001

    def test_append_arc_negative_radius_raises(self) -> None:
        """Negative radius is invalid and raises a ValueError."""
        builder = PolygonBuilder((0.0, 0.0))

        with pytest.raises(
            NegativeValueError,
            match=r"(?i)values for 'radius' cannot be negative\.?$",
        ):
            builder.append_arc(45.0, 0.0, -5.0)

    def test_append_arc_appends_point(self) -> None:
        """Appending an arc adds tessellated points following the circular path."""
        builder = PolygonBuilder((0.0, 0.0))

        result = builder.append_arc(45.0, 0.0, 10.0, max_segment_angle := 10.0)

        assert result is builder
        expected_segments = int(np.ceil(45.0 / max_segment_angle))
        assert builder._points.shape == (expected_segments + 1, 2)  # noqa: SLF001

        start = builder._points[0]  # noqa: SLF001
        center = start + 10.0 * np.array((-np.sin(0.0), np.cos(0.0)))
        distances = np.linalg.norm(builder._points - center, axis=1)  # noqa: SLF001
        np.testing.assert_allclose(distances, 10.0, atol=1e-9)

    def test_append_arc_respects_angle(self) -> None:
        """The total sweep honours the supplied start tangent direction."""
        builder = PolygonBuilder((0.0, 0.0))

        builder.append_arc(90.0, 90.0, 5.0, max_segment_angle := 10.0)

        expected_segments = int(np.ceil(90.0 / max_segment_angle))
        assert builder._points.shape == (expected_segments + 1, 2)  # noqa: SLF001
        np.testing.assert_allclose(builder._points[-1], (-5.0, 5.0), atol=1e-10)  # noqa: SLF001

        start = builder._points[0]  # noqa: SLF001
        center = start + 5.0 * np.array((-np.sin(np.deg2rad(90.0)), np.cos(np.deg2rad(90.0))))
        distances = np.linalg.norm(builder._points - center, axis=1)  # noqa: SLF001
        np.testing.assert_allclose(distances, 5.0, atol=1e-9)

    def test_append_arc_supports_chaining(self) -> None:
        """Arc calls can be chained just like line segments."""
        builder = PolygonBuilder((0.0, 0.0))

        builder.append_arc(90.0, 0.0, 2.0, max_segment_angle := 5).append_arc(-90.0, 90.0, 2.0, max_segment_angle=max_segment_angle)

        first_segments = int(np.ceil(90.0 / max_segment_angle))
        second_segments = int(np.ceil(90.0 / max_segment_angle))
        expected_points = 1 + first_segments + second_segments
        assert builder._points.shape == (expected_points, 2)  # noqa: SLF001
        np.testing.assert_allclose(builder._points[-1], (4.0, 4.0), atol=1e-10)  # noqa: SLF001

    def test_append_arc_non_standard_angle(self) -> None:
        """Arcs starting from arbitrary tangents terminate at the correct location."""
        builder = PolygonBuilder((1.5, -0.75))

        sweep = 60.0
        angle = 37.0
        radius = 12.0

        builder.append_arc(sweep, angle, radius)

        tangent_rad = np.deg2rad(angle)
        start = builder._points[0]  # noqa: SLF001
        center = start + radius * np.array((-np.sin(tangent_rad), np.cos(tangent_rad)))
        start_vector = builder._points[0] - center  # noqa: SLF001
        rotation = np.array(
            [
                [np.cos(np.deg2rad(sweep)), -np.sin(np.deg2rad(sweep))],
                [np.sin(np.deg2rad(sweep)), np.cos(np.deg2rad(sweep))],
            ]
        )
        expected_endpoint = center + rotation @ start_vector

        np.testing.assert_allclose(builder._points[-1], expected_endpoint, atol=1e-10)  # noqa: SLF001

    def test_append_arc_full_circle(self) -> None:
        """A 360° sweep returns to the start point while populating the circle."""
        builder = PolygonBuilder((3.0, 0.0))

        sweep = 360.0
        radius = 3.0
        builder.append_arc(sweep, 0.0, radius, max_segment_angle := 5.0)

        segment_count = int(np.ceil(sweep / max_segment_angle))
        assert builder._points.shape == (segment_count + 1, 2)  # noqa: SLF001

        start = builder._points[0]  # noqa: SLF001
        center = start + radius * np.array((-np.sin(0.0), np.cos(0.0)))
        distances = np.linalg.norm(builder._points - center, axis=1)  # noqa: SLF001
        np.testing.assert_allclose(distances, radius, atol=1e-9)
        np.testing.assert_allclose(builder._points[-1], builder._points[0], atol=1e-9)  # noqa: SLF001

    def test_compute_arc_center_respects_sweep_sign(self) -> None:
        """Arc center is offset to left for CCW sweeps and to right for CW sweeps."""
        builder = PolygonBuilder((0.0, 0.0))

        tangent_angle = 0.0
        ccw_center = builder._compute_arc_center(tangent_angle, 30.0, 5.0)  # noqa: SLF001
        cw_center = builder._compute_arc_center(tangent_angle, -30.0, 5.0)  # noqa: SLF001

        np.testing.assert_allclose(ccw_center, (0.0, 5.0), atol=1e-12)
        np.testing.assert_allclose(cw_center, (0.0, -5.0), atol=1e-12)

    def test_segment_count_for_arc_uses_max_segment_angle(self) -> None:
        """Segment count is derived from the configured maximum segment angle."""
        builder = PolygonBuilder((0.0, 0.0))

        segments = builder._segment_count_for_arc(95.0, max_segment_angle=10.0)  # noqa: SLF001
        reverse_segments = builder._segment_count_for_arc(-95.0, max_segment_angle=10.0)  # noqa: SLF001

        assert segments == 10
        assert reverse_segments == 10

    def test_rotation_matrix_returns_expected_transform(self) -> None:
        """Rotation helper produces the standard planar rotation matrix."""
        sweep = 90.0
        segment_count = 2

        rotation = PolygonBuilder._arc_rotation_series(sweep, segment_count)  # noqa: SLF001

        # Each column is the unit vector rotated by 45° increments.
        expected = np.array([[np.sqrt(2) / 2, np.sqrt(2) / 2], [0.0, 1.0]])
        np.testing.assert_allclose(rotation, expected, atol=1e-12)

    def test_generate_arc_vertices_tracks_rotated_vectors(self) -> None:
        """Vertex generation rotates the radius vector incrementally."""
        builder = PolygonBuilder((0.0, 0.0))

        center = np.array((0.0, 0.0))
        start_vector = np.array((1.0, 0.0))
        rotation = builder._arc_rotation_series(90, 3)  # noqa: SLF001

        points = builder._generate_arc_vertices(center, start_vector, rotation)  # noqa: SLF001

        # The points should be at 30°, 60°, and 90° on the unit circle.
        expected = np.array(
            [
                (np.sqrt(3) / 2, 1.0 / 2),
                (1.0 / 2, np.sqrt(3) / 2),
                (0.0, 1.0),
            ]
        )
        np.testing.assert_allclose(points, expected, atol=1e-12)

    def test_generate_polygon_requires_three_points(self) -> None:
        """Generating a polygon with fewer than three points raises a ValueError."""
        builder = PolygonBuilder((0.0, 0.0))
        builder.append_line(1.0, 0.0)

        with pytest.raises(ValueError, match="A polygon requires at least 3 points"):
            builder.generate_polygon()

    def test_generate_polygon_invalid_geometry(self) -> None:
        """Self-intersecting point sets are rejected as invalid polygons."""
        builder = PolygonBuilder((0.0, 0.0))
        builder._points = np.array(  # noqa: SLF001
            [
                (0.0, 0.0),
                (1.0, 1.0),
                (0.0, 1.0),
                (1.0, 0.0),
            ],
            dtype=float,
        )

        with pytest.raises(ValueError, match="The constructed polygon is not valid"):
            builder.generate_polygon()

    def test_generate_polygon_returns_valid_polygon(self) -> None:
        """A closed path of segments produces a valid Shapely polygon."""
        builder = PolygonBuilder((0.0, 0.0))
        builder.append_line(1.0, 0.0)
        builder.append_line(1.0, 90.0)
        builder.append_line(1.0, 180.0)
        builder.append_line(1.0, -90.0)

        polygon = builder.generate_polygon()

        assert isinstance(polygon, Polygon)
        assert polygon.is_valid
        assert polygon.area == pytest.approx(1.0, rel=0.0, abs=1e-12)
        assert polygon.length == pytest.approx(4.0, rel=0.0, abs=1e-12)
        np.testing.assert_allclose(polygon.centroid.coords[0], (0.0, 0.0), atol=1e-12)

    def test_generate_polygon_with_arc_segments(self) -> None:
        """Polygons built from tessellated arcs remain valid and match expected area."""
        radius = 1.0
        sweep = 360.0
        builder = PolygonBuilder((radius, 0.0))

        builder.append_arc(sweep, angle=0.0, radius=radius, max_segment_angle=30.0)

        polygon = builder.generate_polygon()

        assert polygon.is_valid
        segment_count = builder._segment_count_for_arc(sweep, max_segment_angle=30.0)  # noqa: SLF001
        # Arc tessellation produces segment_count additional vertices plus the start point.
        assert len(builder._points) == segment_count + 1  # noqa: SLF001

        per_segment_angle = np.deg2rad(sweep / segment_count)
        expected_area = 0.5 * segment_count * radius**2 * np.sin(per_segment_angle)
        assert polygon.area == pytest.approx(expected_area, rel=1e-12, abs=1e-12)
        np.testing.assert_allclose(polygon.centroid.coords[0], (0.0, 0.0), atol=1e-12)

    def test_generate_polygon_with_circles(self) -> None:
        """Polygons built from full circles remain valid and match expected area."""
        radius = 2.5
        builder = PolygonBuilder((0.0, 0.0))

        builder.append_arc(360.0, 0.0, radius, max_segment_angle := 1.0)

        polygon = builder.generate_polygon()

        assert polygon.is_valid
        segment_count = 360 / max_segment_angle
        # Arc tessellation produces segment_count additional vertices plus the start point.
        assert len(builder._points) == segment_count + 1  # noqa: SLF001

        expected_area = np.pi * radius**2
        assert polygon.area == pytest.approx(expected_area, rel=1e-3)
        np.testing.assert_allclose(polygon.centroid.coords[0], (0.0, 0.0), atol=1e-9)

    def test_generate_polygon_when_polygon_does_not_close(self) -> None:
        """The builder automatically closes the polygon if needed."""
        builder = PolygonBuilder((0.0, 0.0))
        builder.append_line(1.0, 0.0)
        builder.append_line(1.0, 90.0)
        builder.append_line(1.0, 180.0)
        # Note: The final line back to the start is omitted.
        assert not np.isclose(builder._current_point, builder._points[0]).all()  # noqa: SLF001

        polygon = builder.generate_polygon()

        assert isinstance(polygon, Polygon)
        assert polygon.is_valid
        assert polygon.area == pytest.approx(1.0, rel=0.0, abs=1e-12)
        assert polygon.length == pytest.approx(4.0, rel=0.0, abs=1e-12)
        np.testing.assert_allclose(polygon.centroid.coords[0], (0.0, 0.0), atol=1e-12)

    def test_generate_polygon_no_centroid_transform(self) -> None:
        """The centroid is computed in the local coordinate system if no transform is given."""
        builder = PolygonBuilder((1.0, 1.0))
        builder.append_line(2.0, 0.0)
        builder.append_line(2.0, 90.0)
        builder.append_line(2.0, 180.0)
        builder.append_line(2.0, -90.0)

        polygon = builder.generate_polygon(transform_centroid=False)

        assert isinstance(polygon, Polygon)
        assert polygon.is_valid
        assert polygon.area == pytest.approx(4.0, rel=0.0, abs=1e-12)
        assert polygon.length == pytest.approx(8.0, rel=0.0, abs=1e-12)
        np.testing.assert_allclose(polygon.centroid.coords[0], (2.0, 2.0), atol=1e-12)
