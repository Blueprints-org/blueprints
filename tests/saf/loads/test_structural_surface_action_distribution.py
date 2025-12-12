"""Tests for StructuralSurfaceActionDistribution class."""

import pytest

from blueprints.saf import StructuralSurfaceActionDistribution
from blueprints.saf.loads.structural_surface_action_distribution import (
    DistributionTo,
    Edge,
    LcsType,
    Type,
)


class TestStructuralSurfaceActionDistributionValidInitialization:
    """Test valid initialization of StructuralSurfaceActionDistribution."""

    def test_basic_nodes_distribution(self) -> None:
        """Test basic distribution to nodes."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.name == "FL1"
        assert dist.type == Type.NODES
        assert dist.nodes == "N81;N263;N659;N660"

    def test_nodes_distribution_with_all_optional_fields(self) -> None:
        """Test nodes distribution with all optional fields."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
            layer="Load panel",
            load_applied_to="B1;B2;B3",
            id="uuid-1234",
        )
        assert dist.layer == "Load panel"
        assert dist.load_applied_to == "B1;B2;B3"
        assert dist.id == "uuid-1234"

    def test_edges_distribution(self) -> None:
        """Test distribution to edges only."""
        dist = StructuralSurfaceActionDistribution(
            name="FL2",
            type=Type.EDGES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.Y_BY_VECTOR,
            coordinate_x=0.0,
            coordinate_y=1.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.TWO_WAY,
        )
        assert dist.type == Type.EDGES

    def test_beams_and_edges_distribution(self) -> None:
        """Test distribution to beams and edges."""
        dist = StructuralSurfaceActionDistribution(
            name="FL3",
            type=Type.BEAMS_AND_EDGES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_Y,
            load_applied_to="B1;B2;B3;B5",
        )
        assert dist.type == Type.BEAMS_AND_EDGES

    def test_one_way_x_distribution(self) -> None:
        """Test One way - X distribution."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.distribution_to == DistributionTo.ONE_WAY_X

    def test_one_way_y_distribution(self) -> None:
        """Test One way - Y distribution."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.Y_BY_VECTOR,
            coordinate_x=0.0,
            coordinate_y=1.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_Y,
        )
        assert dist.distribution_to == DistributionTo.ONE_WAY_Y

    def test_two_way_distribution(self) -> None:
        """Test Two way distribution."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.TILT_OF_VECTOR_DEFINED_BY_POINT,
            coordinate_x=0.5,
            coordinate_y=0.5,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.TWO_WAY,
        )
        assert dist.distribution_to == DistributionTo.TWO_WAY

    def test_x_by_vector_lcs(self) -> None:
        """Test x by vector local coordinate system."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.lcs_type == LcsType.X_BY_VECTOR

    def test_y_by_vector_lcs(self) -> None:
        """Test y by vector local coordinate system."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.Y_BY_VECTOR,
            coordinate_x=0.0,
            coordinate_y=1.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_Y,
        )
        assert dist.lcs_type == LcsType.Y_BY_VECTOR

    def test_tilt_of_vector_lcs(self) -> None:
        """Test tilt of vector local coordinate system."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.TILT_OF_VECTOR_DEFINED_BY_POINT,
            coordinate_x=1.0,
            coordinate_y=1.0,
            coordinate_z=0.0,
            lcs_rotation=30.0,
            distribution_to=DistributionTo.TWO_WAY,
        )
        assert dist.lcs_type == LcsType.TILT_OF_VECTOR_DEFINED_BY_POINT

    def test_line_edges(self) -> None:
        """Test with Line edges."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert "Line" in dist.edges

    def test_circular_arc_edges(self) -> None:
        """Test with circular arc edges."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Circular arc;Line;Circular arc",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert "Circular arc" in dist.edges

    def test_parabolic_arc_edges(self) -> None:
        """Test with parabolic arc edges."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Parabolic arc;Line;Parabolic arc",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert "Parabolic arc" in dist.edges

    def test_bezier_edges(self) -> None:
        """Test with Bezier edges."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Bezier;Line;Bezier",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert "Bezier" in dist.edges

    def test_spline_edges(self) -> None:
        """Test with spline edges."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4;N5",
            edges="Line;Spline;Spline;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert "Spline" in dist.edges

    def test_zero_lcs_rotation(self) -> None:
        """Test with zero LCS rotation."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.lcs_rotation == 0.0

    def test_positive_lcs_rotation(self) -> None:
        """Test with positive LCS rotation."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.lcs_rotation == 45.0

    def test_negative_lcs_rotation(self) -> None:
        """Test with negative LCS rotation."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=-30.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.lcs_rotation == -30.0

    def test_decimal_coordinates(self) -> None:
        """Test with decimal coordinate values."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.5,
            coordinate_y=0.75,
            coordinate_z=1.2,
            lcs_rotation=22.5,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.coordinate_x == 1.5
        assert dist.coordinate_y == 0.75
        assert dist.coordinate_z == 1.2

    def test_multiple_nodes(self) -> None:
        """Test with many nodes."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4;N5;N6;N7;N8",
            edges="Line;Line;Line;Line;Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.name == "FL1"

    def test_multiple_beams(self) -> None:
        """Test with multiple beams in load_applied_to."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.BEAMS_AND_EDGES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
            load_applied_to="B1;B2;B3;B4;B5;B6",
        )
        assert dist.load_applied_to == "B1;B2;B3;B4;B5;B6"


class TestStructuralSurfaceActionDistributionValidation:
    """Test validation of StructuralSurfaceActionDistribution."""

    def test_empty_nodes_raises_error(self) -> None:
        """Test that empty nodes string raises ValueError."""
        with pytest.raises(ValueError, match="nodes cannot be empty string"):
            StructuralSurfaceActionDistribution(
                name="FL1",
                type=Type.NODES,
                nodes="",
                edges="Line;Line;Line;Line",
                lcs_type=LcsType.X_BY_VECTOR,
                coordinate_x=1.0,
                coordinate_y=0.0,
                coordinate_z=1.2,
                lcs_rotation=45.0,
                distribution_to=DistributionTo.ONE_WAY_X,
            )

    def test_empty_edges_raises_error(self) -> None:
        """Test that empty edges string raises ValueError."""
        with pytest.raises(ValueError, match="edges cannot be empty string"):
            StructuralSurfaceActionDistribution(
                name="FL1",
                type=Type.NODES,
                nodes="N81;N263;N659;N660",
                edges="",
                lcs_type=LcsType.X_BY_VECTOR,
                coordinate_x=1.0,
                coordinate_y=0.0,
                coordinate_z=1.2,
                lcs_rotation=45.0,
                distribution_to=DistributionTo.ONE_WAY_X,
            )


class TestStructuralSurfaceActionDistributionEnums:
    """Test enum values and functionality."""

    def test_type_enum_values(self) -> None:
        """Test all Type enum values."""
        assert Type.NODES.value == "Nodes"
        assert Type.EDGES.value == "Edges"
        assert Type.BEAMS_AND_EDGES.value == "Beams and edges"

    def test_lcs_type_enum_values(self) -> None:
        """Test all LcsType enum values."""
        assert LcsType.X_BY_VECTOR.value == "x by vector"
        assert LcsType.Y_BY_VECTOR.value == "y by vector"
        assert LcsType.TILT_OF_VECTOR_DEFINED_BY_POINT.value == "Tilt of vector defined by point"

    def test_distribution_to_enum_values(self) -> None:
        """Test all DistributionTo enum values."""
        assert DistributionTo.ONE_WAY_X.value == "One way - X"
        assert DistributionTo.ONE_WAY_Y.value == "One way - Y"
        assert DistributionTo.TWO_WAY.value == "Two way"

    def test_edge_enum_values(self) -> None:
        """Test all Edge enum values."""
        assert Edge.LINE.value == "Line"
        assert Edge.CIRCULAR_ARC.value == "Circular arc"
        assert Edge.CIRCLE_BY_3_POINTS.value == "Circle by 3 points"
        assert Edge.CIRCLE_AND_POINT.value == "Circle and point"
        assert Edge.PARABOLIC_ARC.value == "Parabolic arc"
        assert Edge.BEZIER.value == "Bezier"
        assert Edge.SPLINE.value == "Spline"


class TestStructuralSurfaceActionDistributionImmutability:
    """Test immutability of StructuralSurfaceActionDistribution."""

    def test_frozen_dataclass(self) -> None:
        """Test that instances are frozen and immutable."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        with pytest.raises(AttributeError):
            dist.name = "FL2"  # type: ignore

    def test_hash_support(self) -> None:
        """Test that frozen instances are hashable."""
        dist1 = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        dist_dict = {dist1: "first"}
        assert dist_dict[dist1] == "first"


class TestStructuralSurfaceActionDistributionEquality:
    """Test equality comparison of StructuralSurfaceActionDistribution."""

    def test_equal_instances(self) -> None:
        """Test that identical instances are equal."""
        dist1 = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        dist2 = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist1 == dist2

    def test_unequal_instances_different_name(self) -> None:
        """Test that instances with different names are not equal."""
        dist1 = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        dist2 = StructuralSurfaceActionDistribution(
            name="FL2",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist1 != dist2

    def test_unequal_instances_different_type(self) -> None:
        """Test that instances with different types are not equal."""
        dist1 = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        dist2 = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.EDGES,
            nodes="N81;N263;N659;N660",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=1.2,
            lcs_rotation=45.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist1 != dist2


class TestStructuralSurfaceActionDistributionEdgeCases:
    """Test edge cases and special scenarios."""

    def test_negative_coordinates(self) -> None:
        """Test with negative coordinate values."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=-1.0,
            coordinate_y=-0.5,
            coordinate_z=-1.2,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.coordinate_x == -1.0

    def test_zero_coordinates(self) -> None:
        """Test with zero coordinate values."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=0.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.coordinate_x == 0.0

    def test_large_rotation_angle(self) -> None:
        """Test with large rotation angle."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=360.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.lcs_rotation == 360.0

    def test_empty_optional_layer(self) -> None:
        """Test that empty layer is default."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.layer == ""

    def test_empty_optional_load_applied_to(self) -> None:
        """Test that empty load_applied_to is default."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.load_applied_to == ""

    def test_empty_optional_id(self) -> None:
        """Test that empty id is default."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1;N2;N3;N4",
            edges="Line;Line;Line;Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.id == ""

    def test_single_node(self) -> None:
        """Test with single node (edge case)."""
        dist = StructuralSurfaceActionDistribution(
            name="FL1",
            type=Type.NODES,
            nodes="N1",
            edges="Line",
            lcs_type=LcsType.X_BY_VECTOR,
            coordinate_x=1.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            lcs_rotation=0.0,
            distribution_to=DistributionTo.ONE_WAY_X,
        )
        assert dist.nodes == "N1"
