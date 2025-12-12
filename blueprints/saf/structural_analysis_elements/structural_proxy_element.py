"""Proxy element definition for structural analysis following SAF specification.

Solid objects defined by boundary representation that serve as geometric references.
"""

from dataclasses import dataclass
from typing import NamedTuple


class Vertex(NamedTuple):
    """A 3D vertex of a proxy element.

    Attributes
    ----------
    index : int
        Zero-based vertex index (0 to n).
    x : float
        X coordinate in meters.
    y : float
        Y coordinate in meters.
    z : float
        Z coordinate in meters.
    """

    index: int  # type: ignore[assignment]
    x: float
    y: float
    z: float


class Face(NamedTuple):
    """A face of a proxy element defined by vertex indices.

    Attributes
    ----------
    index : int
        Zero-based face index (0 to n).
    vertex_indices : tuple[int, ...]
        Ordered vertex indices defining the face polygon.
        Must contain at least 3 vertices.
    """

    index: int  # type: ignore[assignment]
    vertex_indices: tuple[int, ...]


@dataclass(frozen=True)
class StructuralProxyElement:
    """Structural proxy element following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralproxyelement.html.

    A solid object defined by boundary representation (faces and vertices) that serves
    as a geometric reference for complex structural parts. Proxy elements are not
    considered in structural analysis calculations.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "SPE1").
    material : str
        Reference to StructuralMaterial by name.
    vertices : tuple[Vertex, ...]
        3D vertices defining the geometry. Must contain at least 4 vertices.
    faces : tuple[Face, ...]
        Faces defined by vertex indices. Must contain at least 4 faces.
        Each face must reference at least 3 vertices.
    color : str, optional
        Hex color format (#AARRGGBB with alpha transparency).
    layer : str, optional
        Custom grouping classification.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name or material is empty.
        If fewer than 4 vertices are provided.
        If fewer than 4 faces are provided.
        If any face has fewer than 3 vertices.
        If any vertex index in a face is out of range.

    Examples
    --------
    >>> from blueprints.saf import StructuralProxyElement, Vertex, Face
    >>> # Simple tetrahedron (4 vertices, 4 faces)
    >>> vertices = (
    ...     Vertex(0, 0.0, 0.0, 0.0),
    ...     Vertex(1, 1.0, 0.0, 0.0),
    ...     Vertex(2, 0.5, 1.0, 0.0),
    ...     Vertex(3, 0.5, 0.5, 1.0),
    ... )
    >>> faces = (
    ...     Face(0, (0, 1, 2)),
    ...     Face(1, (0, 1, 3)),
    ...     Face(2, (1, 2, 3)),
    ...     Face(3, (0, 2, 3)),
    ... )
    >>> element = StructuralProxyElement(
    ...     name="SPE1",
    ...     material="MAT1",
    ...     vertices=vertices,
    ...     faces=faces,
    ... )

    >>> # Cube (8 vertices, 6 faces)
    >>> cube_vertices = (
    ...     Vertex(0, 0.0, 0.0, 0.0),
    ...     Vertex(1, 1.0, 0.0, 0.0),
    ...     Vertex(2, 1.0, 1.0, 0.0),
    ...     Vertex(3, 0.0, 1.0, 0.0),
    ...     Vertex(4, 0.0, 0.0, 1.0),
    ...     Vertex(5, 1.0, 0.0, 1.0),
    ...     Vertex(6, 1.0, 1.0, 1.0),
    ...     Vertex(7, 0.0, 1.0, 1.0),
    ... )
    >>> cube_faces = (
    ...     Face(0, (0, 1, 2, 3)),
    ...     Face(1, (4, 5, 6, 7)),
    ...     Face(2, (0, 1, 5, 4)),
    ...     Face(3, (2, 3, 7, 6)),
    ...     Face(4, (0, 3, 7, 4)),
    ...     Face(5, (1, 2, 6, 5)),
    ... )
    >>> cube = StructuralProxyElement(
    ...     name="SPE2",
    ...     material="MAT1",
    ...     vertices=cube_vertices,
    ...     faces=cube_faces,
    ...     color="#FF0000FF",
    ...     layer="Proxy Elements",
    ... )
    """

    name: str
    material: str
    vertices: tuple[Vertex, ...]
    faces: tuple[Face, ...]
    color: str = ""
    layer: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate proxy element properties.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.material:
            raise ValueError("material cannot be empty")

        if len(self.vertices) < 4:
            raise ValueError("vertices must contain at least 4 vertices")

        if len(self.faces) < 4:
            raise ValueError("faces must contain at least 4 faces")

        # Validate all faces have at least 3 vertices
        for i, face in enumerate(self.faces):
            if len(face.vertex_indices) < 3:
                raise ValueError(f"face at index {i} must have at least 3 vertices, got {len(face.vertex_indices)}")

        # Validate all vertex indices are in range
        max_vertex_index = len(self.vertices) - 1
        for face_idx, face in enumerate(self.faces):
            for vertex_index in face.vertex_indices:
                if vertex_index < 0 or vertex_index > max_vertex_index:
                    raise ValueError(f"face at index {face_idx} references invalid vertex index {vertex_index} (valid range: 0-{max_vertex_index})")
