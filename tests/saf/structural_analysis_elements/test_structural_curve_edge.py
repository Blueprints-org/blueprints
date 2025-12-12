"""Tests for StructuralCurveEdge SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_curve_edge import (
    SegmentType,
    StructuralCurveEdge,
)


class TestStructuralCurveEdgeValidInitialization:
    """Test valid initialization of StructuralCurveEdge."""

    def test_simple_line_edge(self) -> None:
        """Test simple line edge with two nodes."""
        edge = StructuralCurveEdge(
            name="IE1",
            surface_member="S2",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
        )
        assert edge.name == "IE1"
        assert edge.surface_member == "S2"
        assert len(edge.nodes) == 2
        assert len(edge.segments) == 1

    def test_edge_with_multiple_nodes_and_segments(self) -> None:
        """Test edge with multiple nodes and segments."""
        edge = StructuralCurveEdge(
            name="IE2",
            surface_member="S3",
            nodes=("N1", "N2", "N3", "N4"),
            segments=(
                SegmentType.LINE,
                SegmentType.CIRCULAR_ARC,
                SegmentType.LINE,
            ),
        )
        assert len(edge.nodes) == 4
        assert len(edge.segments) == 3

    def test_edge_with_circular_arc(self) -> None:
        """Test edge with circular arc segment."""
        edge = StructuralCurveEdge(
            name="IE3",
            surface_member="S1",
            nodes=("N1", "N2", "N3"),
            segments=(
                SegmentType.CIRCULAR_ARC,
                SegmentType.LINE,
            ),
        )
        assert edge.segments[0] == SegmentType.CIRCULAR_ARC
        assert edge.segments[1] == SegmentType.LINE

    def test_edge_with_bezier_segment(self) -> None:
        """Test edge with Bezier segment."""
        edge = StructuralCurveEdge(
            name="IE4",
            surface_member="S4",
            nodes=("N1", "N2"),
            segments=(SegmentType.BEZIER,),
        )
        assert edge.segments[0] == SegmentType.BEZIER

    def test_edge_with_parabolic_arc(self) -> None:
        """Test edge with parabolic arc."""
        edge = StructuralCurveEdge(
            name="IE5",
            surface_member="S5",
            nodes=("N1", "N2", "N3"),
            segments=(
                SegmentType.PARABOLIC_ARC,
                SegmentType.LINE,
            ),
        )
        assert edge.segments[0] == SegmentType.PARABOLIC_ARC

    def test_edge_with_spline(self) -> None:
        """Test edge with spline segment."""
        edge = StructuralCurveEdge(
            name="IE6",
            surface_member="S6",
            nodes=("N1", "N2", "N3", "N4"),
            segments=(
                SegmentType.SPLINE,
                SegmentType.SPLINE,
                SegmentType.SPLINE,
            ),
        )
        assert edge.segments[0] == SegmentType.SPLINE

    def test_edge_with_parent_id(self) -> None:
        """Test edge with parent ID."""
        edge = StructuralCurveEdge(
            name="IE7",
            surface_member="S7",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            parent_id="12345678-1234-5678-1234-567812345678",
        )
        assert edge.parent_id == "12345678-1234-5678-1234-567812345678"

    def test_edge_with_uuid(self) -> None:
        """Test edge with UUID identifier."""
        edge = StructuralCurveEdge(
            name="IE8",
            surface_member="S8",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            id="87654321-4321-8765-4321-876543218765",
        )
        assert edge.id == "87654321-4321-8765-4321-876543218765"

    def test_edge_with_many_nodes(self) -> None:
        """Test edge with many nodes."""
        nodes = tuple(f"N{i}" for i in range(1, 11))
        segments = tuple(SegmentType.LINE for _ in range(9))
        edge = StructuralCurveEdge(
            name="IE9",
            surface_member="S9",
            nodes=nodes,
            segments=segments,
        )
        assert len(edge.nodes) == 10
        assert len(edge.segments) == 9

    def test_all_segment_types(self) -> None:
        """Test edge with all segment types."""
        edge = StructuralCurveEdge(
            name="IE10",
            surface_member="S10",
            nodes=("N1", "N2", "N3", "N4", "N5", "N6"),
            segments=(
                SegmentType.LINE,
                SegmentType.CIRCULAR_ARC,
                SegmentType.BEZIER,
                SegmentType.PARABOLIC_ARC,
                SegmentType.SPLINE,
            ),
        )
        assert edge.segments[0] == SegmentType.LINE
        assert edge.segments[1] == SegmentType.CIRCULAR_ARC
        assert edge.segments[2] == SegmentType.BEZIER
        assert edge.segments[3] == SegmentType.PARABOLIC_ARC
        assert edge.segments[4] == SegmentType.SPLINE


class TestStructuralCurveEdgeValidation:
    """Test validation of StructuralCurveEdge."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralCurveEdge(
                name="",
                surface_member="S1",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
            )

    def test_empty_surface_member_raises_error(self) -> None:
        """Test that empty surface_member raises ValueError."""
        with pytest.raises(ValueError, match="surface_member cannot be empty"):
            StructuralCurveEdge(
                name="IE1",
                surface_member="",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
            )

    def test_less_than_two_nodes_raises_error(self) -> None:
        """Test that fewer than 2 nodes raises ValueError."""
        with pytest.raises(ValueError, match="at least 2 nodes"):
            StructuralCurveEdge(
                name="IE1",
                surface_member="S1",
                nodes=("N1",),
                segments=(SegmentType.LINE,),
            )

    def test_empty_nodes_raises_error(self) -> None:
        """Test that empty nodes raises ValueError."""
        with pytest.raises(ValueError, match="at least 2 nodes"):
            StructuralCurveEdge(
                name="IE1",
                surface_member="S1",
                nodes=(),
                segments=(),
            )

    def test_segment_count_mismatch_raises_error(self) -> None:
        """Test that segment count not matching nodes - 1 raises ValueError."""
        with pytest.raises(ValueError, match="segments length"):
            StructuralCurveEdge(
                name="IE1",
                surface_member="S1",
                nodes=("N1", "N2", "N3"),
                segments=(SegmentType.LINE,),  # Should have 2 segments
            )

    def test_empty_node_name_raises_error(self) -> None:
        """Test that empty node name raises ValueError."""
        with pytest.raises(ValueError, match="Node name at index"):
            StructuralCurveEdge(
                name="IE1",
                surface_member="S1",
                nodes=("N1", ""),  # Empty node name at index 1
                segments=(SegmentType.LINE,),
            )

    def test_too_many_segments_raises_error(self) -> None:
        """Test that too many segments raises ValueError."""
        with pytest.raises(ValueError, match="segments length"):
            StructuralCurveEdge(
                name="IE1",
                surface_member="S1",
                nodes=("N1", "N2"),
                segments=(
                    SegmentType.LINE,
                    SegmentType.LINE,  # Too many
                ),
            )


class TestEnums:
    """Test enum values."""

    def test_segment_type_values(self) -> None:
        """Test SegmentType enum values."""
        assert SegmentType.LINE.value == "Line"
        assert SegmentType.CIRCULAR_ARC.value == "Circular Arc"
        assert SegmentType.BEZIER.value == "Bezier"
        assert SegmentType.PARABOLIC_ARC.value == "Parabolic arc"
        assert SegmentType.SPLINE.value == "Spline"


class TestStructuralCurveEdgeImmutability:
    """Test immutability of StructuralCurveEdge."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        edge = StructuralCurveEdge(
            name="IE1",
            surface_member="S1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
        )
        with pytest.raises(Exception):
            edge.name = "IE2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that edge can be used in sets."""
        edge = StructuralCurveEdge(
            name="IE1",
            surface_member="S1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
        )
        edge_set = {edge}
        assert edge in edge_set


class TestStructuralCurveEdgeEquality:
    """Test equality of StructuralCurveEdge."""

    def test_equal_edges(self) -> None:
        """Test that identical edges are equal."""
        edge1 = StructuralCurveEdge(
            name="IE1",
            surface_member="S1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
        )
        edge2 = StructuralCurveEdge(
            name="IE1",
            surface_member="S1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
        )
        assert edge1 == edge2

    def test_unequal_edges_different_names(self) -> None:
        """Test that edges with different names are not equal."""
        edge1 = StructuralCurveEdge(
            name="IE1",
            surface_member="S1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
        )
        edge2 = StructuralCurveEdge(
            name="IE2",
            surface_member="S1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
        )
        assert edge1 != edge2

    def test_unequal_edges_different_nodes(self) -> None:
        """Test that edges with different nodes are not equal."""
        edge1 = StructuralCurveEdge(
            name="IE1",
            surface_member="S1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
        )
        edge2 = StructuralCurveEdge(
            name="IE1",
            surface_member="S1",
            nodes=("N1", "N3"),
            segments=(SegmentType.LINE,),
        )
        assert edge1 != edge2
