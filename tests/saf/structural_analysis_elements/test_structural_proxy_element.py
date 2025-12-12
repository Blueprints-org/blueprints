"""Tests for StructuralProxyElement SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_proxy_element import (
    Face,
    StructuralProxyElement,
    Vertex,
)


class TestValidInitialization:
    """Test valid initialization of StructuralProxyElement."""

    def test_simple_tetrahedron(self) -> None:
        """Test simple tetrahedron (4 vertices, 4 faces)."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        element = StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)
        assert element.name == "SPE1"
        assert len(element.vertices) == 4
        assert len(element.faces) == 4

    def test_cube(self) -> None:
        """Test cube (8 vertices, 6 faces)."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 1.0, 1.0, 0.0),
            Vertex(3, 0.0, 1.0, 0.0),
            Vertex(4, 0.0, 0.0, 1.0),
            Vertex(5, 1.0, 0.0, 1.0),
            Vertex(6, 1.0, 1.0, 1.0),
            Vertex(7, 0.0, 1.0, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2, 3)),
            Face(1, (4, 5, 6, 7)),
            Face(2, (0, 1, 5, 4)),
            Face(3, (2, 3, 7, 6)),
            Face(4, (0, 3, 7, 4)),
            Face(5, (1, 2, 6, 5)),
        )
        element = StructuralProxyElement(name="SPE2", material="M2", vertices=vertices, faces=faces)
        assert len(element.vertices) == 8
        assert len(element.faces) == 6

    def test_pyramid(self) -> None:
        """Test pyramid (5 vertices, 5 faces)."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 1.0, 1.0, 0.0),
            Vertex(3, 0.0, 1.0, 0.0),
            Vertex(4, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2, 3)),
            Face(1, (0, 1, 4)),
            Face(2, (1, 2, 4)),
            Face(3, (2, 3, 4)),
            Face(4, (3, 0, 4)),
        )
        element = StructuralProxyElement(name="SPE3", material="M3", vertices=vertices, faces=faces)
        assert len(element.vertices) == 5
        assert len(element.faces) == 5

    def test_with_optional_properties(self) -> None:
        """Test element with optional properties."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        element = StructuralProxyElement(
            name="SPE4",
            material="M4",
            vertices=vertices,
            faces=faces,
            color="#FF0000FF",
            layer="Proxy Elements",
            id="39f238a5-01d0-45cf-a2eb-958170fd4f39",
        )
        assert element.color == "#FF0000FF"
        assert element.layer == "Proxy Elements"
        assert element.id == "39f238a5-01d0-45cf-a2eb-958170fd4f39"

    def test_element_with_many_vertices_and_faces(self) -> None:
        """Test element with many vertices and faces."""
        num_vertices = 10
        vertices = tuple(Vertex(i, float(i), float(i % 3), float(i % 2)) for i in range(num_vertices))
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (1, 2, 3)),
            Face(2, (2, 3, 4)),
            Face(3, (3, 4, 5)),
        )
        element = StructuralProxyElement(name="SPE5", material="M5", vertices=vertices, faces=faces)
        assert len(element.vertices) == num_vertices
        assert len(element.faces) == 4


class TestValidation:
    """Test validation of StructuralProxyElement."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralProxyElement(name="", material="M1", vertices=vertices, faces=faces)

    def test_empty_material_raises_error(self) -> None:
        """Test that empty material raises ValueError."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        with pytest.raises(ValueError, match="material cannot be empty"):
            StructuralProxyElement(name="SPE1", material="", vertices=vertices, faces=faces)

    def test_fewer_than_four_vertices_raises_error(self) -> None:
        """Test that fewer than 4 vertices raises ValueError."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 2)),
            Face(2, (0, 1, 2)),
            Face(3, (0, 1, 2)),
        )
        with pytest.raises(ValueError, match="at least 4 vertices"):
            StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)

    def test_fewer_than_four_faces_raises_error(self) -> None:
        """Test that fewer than 4 faces raises ValueError."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
        )
        with pytest.raises(ValueError, match="at least 4 faces"):
            StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)

    def test_face_with_less_than_three_vertices_raises_error(self) -> None:
        """Test that face with < 3 vertices raises ValueError."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        with pytest.raises(ValueError, match="must have at least 3 vertices"):
            StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)

    def test_invalid_vertex_index_raises_error(self) -> None:
        """Test that invalid vertex index in face raises ValueError."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 5)),  # Index 5 is out of range
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        with pytest.raises(ValueError, match="invalid vertex index"):
            StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)

    def test_negative_vertex_index_raises_error(self) -> None:
        """Test that negative vertex index raises ValueError."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, -1)),  # Negative index
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        with pytest.raises(ValueError, match="invalid vertex index"):
            StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)


class TestImmutability:
    """Test immutability of StructuralProxyElement."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        element = StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)
        with pytest.raises(Exception):
            element.name = "SPE2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that element can be used in sets."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        element = StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)
        element_set = {element}
        assert element in element_set


class TestEquality:
    """Test equality of StructuralProxyElement."""

    def test_equal_elements(self) -> None:
        """Test that identical elements are equal."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        element1 = StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)
        element2 = StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)
        assert element1 == element2

    def test_unequal_elements_different_names(self) -> None:
        """Test that elements with different names are not equal."""
        vertices = (
            Vertex(0, 0.0, 0.0, 0.0),
            Vertex(1, 1.0, 0.0, 0.0),
            Vertex(2, 0.5, 1.0, 0.0),
            Vertex(3, 0.5, 0.5, 1.0),
        )
        faces = (
            Face(0, (0, 1, 2)),
            Face(1, (0, 1, 3)),
            Face(2, (1, 2, 3)),
            Face(3, (0, 2, 3)),
        )
        element1 = StructuralProxyElement(name="SPE1", material="M1", vertices=vertices, faces=faces)
        element2 = StructuralProxyElement(name="SPE2", material="M1", vertices=vertices, faces=faces)
        assert element1 != element2


class TestVertexAndFace:
    """Test Vertex and Face NamedTuples."""

    def test_vertex_creation(self) -> None:
        """Test vertex creation with all parameters."""
        vertex = Vertex(0, 1.5, 2.5, 3.5)
        assert vertex.index == 0
        assert vertex.x == 1.5
        assert vertex.y == 2.5
        assert vertex.z == 3.5

    def test_face_creation(self) -> None:
        """Test face creation with vertex indices."""
        face = Face(0, (0, 1, 2, 3))
        assert face.index == 0
        assert face.vertex_indices == (0, 1, 2, 3)

    def test_vertex_immutability(self) -> None:
        """Test that vertex is immutable."""
        vertex = Vertex(0, 1.0, 2.0, 3.0)
        with pytest.raises(AttributeError):
            vertex.x = 5.0  # type: ignore[misc]

    def test_face_immutability(self) -> None:
        """Test that face is immutable."""
        face = Face(0, (0, 1, 2))
        with pytest.raises(AttributeError):
            face.index = 1  # type: ignore[misc]
