"""Tests for the cross-section builder module."""

from itertools import pairwise

import numpy as np
import pytest
from shapely.geometry import Polygon

from blueprints.structural_sections._polygon_builder import PolygonBuilder, merge_polygons
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection


class TestMergePolygons:
    """Tests for the merge_polygons function."""

    def test_merge_polygons_empty_list(self) -> None:
        """Test that ValueError is raised when an empty list is provided."""
        with pytest.raises(ValueError, match="No elements have been added to the cross-section."):
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

        with pytest.raises(TypeError, match="The combined geometry is not a valid Polygon."):
            merge_polygons(elements)


class TestPolygonBuilderStub:
    """Ensure the placeholder `PolygonBuilder` surface behaves as expected for now."""

    def test_placeholder_methods_raise(self) -> None:
        """Test that all placeholder methods raise NotImplementedError."""
        builder = PolygonBuilder((0.0, 0.0))

        assert isinstance(builder._points, np.ndarray)  # noqa: SLF001
        assert builder._points.shape == (1, 2)  # noqa: SLF001
        assert builder._current_point is not None  # noqa: SLF001

        with pytest.raises(NotImplementedError):
            builder.append_line(1.0, 0.0)

        with pytest.raises(NotImplementedError):
            builder.append_arc(90.0, 0.0, 1.0)

        with pytest.raises(NotImplementedError):
            builder.create_polygon()
