"""Tests for StructuralSurfaceMemberOpening SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_surface_member_opening import (
    EdgeType,
    StructuralSurfaceMemberOpening,
)


class TestValidInitialization:
    """Test valid initialization of StructuralSurfaceMemberOpening."""

    def test_rectangular_opening(self) -> None:
        """Test simple rectangular opening."""
        opening = StructuralSurfaceMemberOpening(
            name="O1",
            two_d_member="S1",
            nodes=("O1_N1", "O1_N2", "O1_N3", "O1_N4"),
            edges=(
                EdgeType.LINE,
                EdgeType.LINE,
                EdgeType.LINE,
                EdgeType.LINE,
            ),
        )
        assert opening.name == "O1"
        assert opening.two_d_member == "S1"
        assert len(opening.nodes) == 4

    def test_triangular_opening(self) -> None:
        """Test triangular opening."""
        opening = StructuralSurfaceMemberOpening(
            name="O2",
            two_d_member="S2",
            nodes=("O2_N1", "O2_N2", "O2_N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
        )
        assert len(opening.nodes) == 3
        assert len(opening.edges) == 3

    def test_circular_opening_by_3_points(self) -> None:
        """Test circular opening defined by 3 points."""
        opening = StructuralSurfaceMemberOpening(
            name="O3",
            two_d_member="S3",
            nodes=("O3_N1", "O3_N2", "O3_N3"),
            edges=(
                EdgeType.CIRCLE_BY_3_POINTS,
                EdgeType.CIRCLE_BY_3_POINTS,
                EdgeType.CIRCLE_BY_3_POINTS,
            ),
        )
        assert opening.edges[0] == EdgeType.CIRCLE_BY_3_POINTS

    def test_opening_with_circle_edge(self) -> None:
        """Test opening with circle edge."""
        opening = StructuralSurfaceMemberOpening(
            name="O4",
            two_d_member="S4",
            nodes=("O4_N1", "O4_N2", "O4_N3"),
            edges=(EdgeType.CIRCLE, EdgeType.CIRCLE, EdgeType.CIRCLE),
        )
        assert opening.edges[0] == EdgeType.CIRCLE

    def test_opening_with_area(self) -> None:
        """Test opening with area property."""
        opening = StructuralSurfaceMemberOpening(
            name="O5",
            two_d_member="S5",
            nodes=("O5_N1", "O5_N2", "O5_N3", "O5_N4"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            area=2.5,
        )
        assert opening.area == 2.5

    def test_opening_with_curved_edges(self) -> None:
        """Test opening with curved edges."""
        opening = StructuralSurfaceMemberOpening(
            name="O6",
            two_d_member="S6",
            nodes=("O6_N1", "O6_N2", "O6_N3", "O6_N4"),
            edges=(
                EdgeType.BEZIER,
                EdgeType.CIRCULAR_ARC,
                EdgeType.PARABOLIC_ARC,
                EdgeType.SPLINE,
            ),
        )
        assert len(opening.edges) == 4

    def test_opening_with_all_edge_types(self) -> None:
        """Test opening with different edge types."""
        edges = [
            EdgeType.LINE,
            EdgeType.BEZIER,
            EdgeType.CIRCULAR_ARC,
            EdgeType.PARABOLIC_ARC,
            EdgeType.SPLINE,
            EdgeType.CIRCLE,
            EdgeType.CIRCLE_BY_3_POINTS,
        ]
        opening = StructuralSurfaceMemberOpening(
            name="O7",
            two_d_member="S7",
            nodes=tuple(f"O7_N{i}" for i in range(len(edges))),
            edges=tuple(edges),
        )
        assert len(opening.edges) == len(edges)

    def test_opening_with_uuid(self) -> None:
        """Test opening with UUID identifier."""
        opening = StructuralSurfaceMemberOpening(
            name="O8",
            two_d_member="S8",
            nodes=("O8_N1", "O8_N2", "O8_N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            id="39f238a5-01d0-45cf-a2eb-958170fd4f39",
        )
        assert opening.id == "39f238a5-01d0-45cf-a2eb-958170fd4f39"

    def test_opening_with_parent_id(self) -> None:
        """Test opening with parent ID for curved geometry tracking."""
        opening = StructuralSurfaceMemberOpening(
            name="O9",
            two_d_member="S9",
            nodes=("O9_N1", "O9_N2", "O9_N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            parent_id="12345678-1234-5678-1234-567812345678",
        )
        assert opening.parent_id == "12345678-1234-5678-1234-567812345678"

    def test_many_node_opening(self) -> None:
        """Test opening with many nodes."""
        num_nodes = 10
        opening = StructuralSurfaceMemberOpening(
            name="O10",
            two_d_member="S10",
            nodes=tuple(f"O10_N{i}" for i in range(1, num_nodes + 1)),
            edges=tuple(EdgeType.LINE for _ in range(num_nodes)),
        )
        assert len(opening.nodes) == num_nodes
        assert len(opening.edges) == num_nodes


class TestValidation:
    """Test validation of StructuralSurfaceMemberOpening."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralSurfaceMemberOpening(
                name="",
                two_d_member="S1",
                nodes=("N1", "N2", "N3"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            )

    def test_empty_two_d_member_raises_error(self) -> None:
        """Test that empty two_d_member raises ValueError."""
        with pytest.raises(ValueError, match="two_d_member cannot be empty"):
            StructuralSurfaceMemberOpening(
                name="O1",
                two_d_member="",
                nodes=("N1", "N2", "N3"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            )

    def test_fewer_than_three_nodes_raises_error(self) -> None:
        """Test that fewer than 3 nodes raises ValueError."""
        with pytest.raises(ValueError, match="at least 3 nodes"):
            StructuralSurfaceMemberOpening(
                name="O1",
                two_d_member="S1",
                nodes=("N1", "N2"),
                edges=(EdgeType.LINE, EdgeType.LINE),
            )

    def test_empty_nodes_raises_error(self) -> None:
        """Test that empty nodes raises ValueError."""
        with pytest.raises(ValueError, match="at least 3 nodes"):
            StructuralSurfaceMemberOpening(
                name="O1",
                two_d_member="S1",
                nodes=(),
                edges=(),
            )

    def test_edges_count_mismatch_raises_error(self) -> None:
        """Test that edges count not matching nodes raises ValueError."""
        with pytest.raises(ValueError, match="edges length"):
            StructuralSurfaceMemberOpening(
                name="O1",
                two_d_member="S1",
                nodes=("N1", "N2", "N3", "N4"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            )

    def test_empty_node_name_raises_error(self) -> None:
        """Test that empty node name raises ValueError."""
        with pytest.raises(ValueError, match="Node name at index"):
            StructuralSurfaceMemberOpening(
                name="O1",
                two_d_member="S1",
                nodes=("N1", "", "N3"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            )

    def test_too_many_edges_raises_error(self) -> None:
        """Test that too many edges raises ValueError."""
        with pytest.raises(ValueError, match="edges length"):
            StructuralSurfaceMemberOpening(
                name="O1",
                two_d_member="S1",
                nodes=("N1", "N2", "N3"),
                edges=(
                    EdgeType.LINE,
                    EdgeType.LINE,
                    EdgeType.LINE,
                    EdgeType.LINE,
                ),
            )


class TestEnums:
    """Test enum values."""

    def test_edge_type_values(self) -> None:
        """Test EdgeType enum values."""
        assert EdgeType.LINE.value == "Line"
        assert EdgeType.BEZIER.value == "Bezier"
        assert EdgeType.CIRCULAR_ARC.value == "Circular Arc"
        assert EdgeType.PARABOLIC_ARC.value == "Parabolic arc"
        assert EdgeType.SPLINE.value == "Spline"
        assert EdgeType.CIRCLE.value == "Circle"
        assert EdgeType.CIRCLE_BY_3_POINTS.value == "Circle by 3 points"
        assert EdgeType.POINT.value == "Point"


class TestImmutability:
    """Test immutability of StructuralSurfaceMemberOpening."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        opening = StructuralSurfaceMemberOpening(
            name="O1",
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
        )
        with pytest.raises(Exception):
            opening.name = "O2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that opening can be used in sets."""
        opening = StructuralSurfaceMemberOpening(
            name="O1",
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
        )
        opening_set = {opening}
        assert opening in opening_set


class TestEquality:
    """Test equality of StructuralSurfaceMemberOpening."""

    def test_equal_openings(self) -> None:
        """Test that identical openings are equal."""
        opening1 = StructuralSurfaceMemberOpening(
            name="O1",
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
        )
        opening2 = StructuralSurfaceMemberOpening(
            name="O1",
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
        )
        assert opening1 == opening2

    def test_unequal_openings_different_names(self) -> None:
        """Test that openings with different names are not equal."""
        opening1 = StructuralSurfaceMemberOpening(
            name="O1",
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
        )
        opening2 = StructuralSurfaceMemberOpening(
            name="O2",
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
        )
        assert opening1 != opening2

    def test_unequal_openings_different_nodes(self) -> None:
        """Test that openings with different nodes are not equal."""
        opening1 = StructuralSurfaceMemberOpening(
            name="O1",
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
        )
        opening2 = StructuralSurfaceMemberOpening(
            name="O1",
            two_d_member="S1",
            nodes=("N1", "N2", "N4"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
        )
        assert opening1 != opening2
