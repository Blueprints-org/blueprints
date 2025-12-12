"""Tests for StructuralPointConnection SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_point_connection import (
    StructuralPointConnection,
)


class TestStructuralPointConnectionValidInitialization:
    """Test valid initialization of StructuralPointConnection."""

    def test_node_at_origin(self) -> None:
        """Test node at origin."""
        node = StructuralPointConnection(
            name="N1",
            x=0.0,
            y=0.0,
            z=0.0,
        )
        assert node.name == "N1"
        assert node.x == 0.0
        assert node.y == 0.0
        assert node.z == 0.0

    def test_node_above_origin(self) -> None:
        """Test node above origin."""
        node = StructuralPointConnection(
            name="N2",
            x=5.0,
            y=0.0,
            z=3.5,
        )
        assert node.x == 5.0
        assert node.z == 3.5

    def test_node_with_negative_coordinates(self) -> None:
        """Test node with negative coordinates."""
        node = StructuralPointConnection(
            name="N3",
            x=-10.0,
            y=-5.0,
            z=-2.5,
        )
        assert node.x == -10.0
        assert node.y == -5.0
        assert node.z == -2.5

    def test_node_with_uuid(self) -> None:
        """Test node with UUID identifier."""
        node = StructuralPointConnection(
            name="N4",
            x=1.0,
            y=2.0,
            z=3.0,
            id="39f238a5-01d0-45cf-a2eb-958170fd4f39",
        )
        assert node.id == "39f238a5-01d0-45cf-a2eb-958170fd4f39"

    def test_node_with_large_coordinates(self) -> None:
        """Test node with large coordinates."""
        node = StructuralPointConnection(
            name="N5",
            x=1000.0,
            y=2000.0,
            z=3000.0,
        )
        assert node.x == 1000.0
        assert node.y == 2000.0
        assert node.z == 3000.0

    def test_node_with_fractional_coordinates(self) -> None:
        """Test node with fractional coordinates."""
        node = StructuralPointConnection(
            name="N6",
            x=1.2345,
            y=2.5678,
            z=3.9012,
        )
        assert node.x == 1.2345
        assert node.y == 2.5678
        assert node.z == 3.9012

    def test_multiple_nodes(self) -> None:
        """Test creating multiple nodes."""
        nodes = [
            StructuralPointConnection(name="N1", x=0.0, y=0.0, z=0.0),
            StructuralPointConnection(name="N2", x=5.0, y=0.0, z=0.0),
            StructuralPointConnection(name="N3", x=5.0, y=5.0, z=0.0),
        ]
        assert len(nodes) == 3
        assert nodes[0].name == "N1"
        assert nodes[1].name == "N2"
        assert nodes[2].name == "N3"


class TestStructuralPointConnectionValidation:
    """Test validation of StructuralPointConnection."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralPointConnection(
                name="",
                x=0.0,
                y=0.0,
                z=0.0,
            )


class TestStructuralPointConnectionDistance:
    """Test distance calculation between nodes."""

    def test_distance_zero(self) -> None:
        """Test distance to same point."""
        node1 = StructuralPointConnection(name="N1", x=0.0, y=0.0, z=0.0)
        node2 = StructuralPointConnection(name="N2", x=0.0, y=0.0, z=0.0)
        assert node1.distance_to(node2) == pytest.approx(0.0)

    def test_distance_horizontal(self) -> None:
        """Test distance along x-axis."""
        node1 = StructuralPointConnection(name="N1", x=0.0, y=0.0, z=0.0)
        node2 = StructuralPointConnection(name="N2", x=5.0, y=0.0, z=0.0)
        assert node1.distance_to(node2) == pytest.approx(5.0)

    def test_distance_vertical(self) -> None:
        """Test distance along z-axis."""
        node1 = StructuralPointConnection(name="N1", x=0.0, y=0.0, z=0.0)
        node2 = StructuralPointConnection(name="N2", x=0.0, y=0.0, z=3.0)
        assert node1.distance_to(node2) == pytest.approx(3.0)

    def test_distance_3d(self) -> None:
        """Test distance in 3D space."""
        node1 = StructuralPointConnection(name="N1", x=0.0, y=0.0, z=0.0)
        node2 = StructuralPointConnection(name="N2", x=3.0, y=4.0, z=0.0)
        assert node1.distance_to(node2) == pytest.approx(5.0)

    def test_distance_pythagorean(self) -> None:
        """Test distance with Pythagorean triple."""
        node1 = StructuralPointConnection(name="N1", x=0.0, y=0.0, z=0.0)
        node2 = StructuralPointConnection(name="N2", x=3.0, y=4.0, z=12.0)
        # sqrt(3^2 + 4^2 + 12^2) = sqrt(9 + 16 + 144) = sqrt(169) = 13
        assert node1.distance_to(node2) == pytest.approx(13.0)

    def test_distance_symmetric(self) -> None:
        """Test that distance is symmetric."""
        node1 = StructuralPointConnection(name="N1", x=1.0, y=2.0, z=3.0)
        node2 = StructuralPointConnection(name="N2", x=4.0, y=6.0, z=8.0)
        assert node1.distance_to(node2) == pytest.approx(node2.distance_to(node1))

    def test_distance_with_negative_coordinates(self) -> None:
        """Test distance with negative coordinates."""
        node1 = StructuralPointConnection(name="N1", x=-3.0, y=-4.0, z=0.0)
        node2 = StructuralPointConnection(name="N2", x=3.0, y=4.0, z=0.0)
        assert node1.distance_to(node2) == pytest.approx(10.0)

    def test_distance_type_error(self) -> None:
        """Test distance with wrong type raises TypeError."""
        node = StructuralPointConnection(name="N1", x=0.0, y=0.0, z=0.0)
        with pytest.raises(TypeError, match="must be a StructuralPointConnection"):
            node.distance_to("N2")  # type: ignore[arg-type]

    def test_distance_with_other_type(self) -> None:
        """Test distance with other types raises TypeError."""
        node = StructuralPointConnection(name="N1", x=0.0, y=0.0, z=0.0)
        with pytest.raises(TypeError):
            node.distance_to(None)  # type: ignore[arg-type]


class TestStructuralPointConnectionImmutability:
    """Test immutability of StructuralPointConnection."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        node = StructuralPointConnection(
            name="N1",
            x=0.0,
            y=0.0,
            z=0.0,
        )
        with pytest.raises(Exception):
            node.name = "N2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that node can be used in sets."""
        node = StructuralPointConnection(
            name="N1",
            x=0.0,
            y=0.0,
            z=0.0,
        )
        node_set = {node}
        assert node in node_set


class TestStructuralPointConnectionEquality:
    """Test equality of StructuralPointConnection."""

    def test_equal_nodes(self) -> None:
        """Test that identical nodes are equal."""
        node1 = StructuralPointConnection(
            name="N1",
            x=0.0,
            y=0.0,
            z=0.0,
        )
        node2 = StructuralPointConnection(
            name="N1",
            x=0.0,
            y=0.0,
            z=0.0,
        )
        assert node1 == node2

    def test_unequal_nodes_different_names(self) -> None:
        """Test that nodes with different names are not equal."""
        node1 = StructuralPointConnection(
            name="N1",
            x=0.0,
            y=0.0,
            z=0.0,
        )
        node2 = StructuralPointConnection(
            name="N2",
            x=0.0,
            y=0.0,
            z=0.0,
        )
        assert node1 != node2

    def test_unequal_nodes_different_coordinates(self) -> None:
        """Test that nodes with different coordinates are not equal."""
        node1 = StructuralPointConnection(
            name="N1",
            x=0.0,
            y=0.0,
            z=0.0,
        )
        node2 = StructuralPointConnection(
            name="N1",
            x=1.0,
            y=0.0,
            z=0.0,
        )
        assert node1 != node2
