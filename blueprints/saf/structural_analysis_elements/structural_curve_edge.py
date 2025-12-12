"""Curve edge definition for structural analysis following SAF specification.

An internal edge (StructuralCurveEdge) is a line on which loads can act on a 2D member.
"""

from dataclasses import dataclass
from enum import Enum


class SegmentType(str, Enum):
    """Segment type for curve edges following SAF specification.

    Defines the shape between consecutive nodes on a curve edge.
    """

    LINE = "Line"
    CIRCULAR_ARC = "Circular Arc"
    BEZIER = "Bezier"
    PARABOLIC_ARC = "Parabolic arc"
    SPLINE = "Spline"


@dataclass(frozen=True)
class StructuralCurveEdge:
    """Structural curve edge definition following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralcurveedge.html.

    An internal edge (StructuralCurveEdge) is an object within a 2D member on which
    line forces can act. It defines a curve path on the surface using a sequence of nodes
    and segment types between them.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "IE1").
    surface_member : str
        Reference to the parent StructuralSurfaceMember by name (e.g., "S2").
    nodes : tuple[str, ...]
        Sequence of node names defining the edge geometry, ordered from beginning to end.
        Must contain at least 2 nodes.
    segments : tuple[SegmentType, ...]
        Segment types between consecutive nodes. Length must be len(nodes) - 1.
        Supported types: Line, Circular Arc, Bezier, Parabolic arc, Spline.
    parent_id : str, optional
        Parent ID for tracking curved geometry divided into straight segments (UUID format).
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name or surface_member is empty.
        If fewer than 2 nodes are provided.
        If number of segments doesn't match nodes - 1.

    Examples
    --------
    >>> from blueprints.saf import StructuralCurveEdge, SegmentType
    >>> # Simple line edge
    >>> edge1 = StructuralCurveEdge(
    ...     name="IE1",
    ...     surface_member="S2",
    ...     nodes=("N1", "N2"),
    ...     segments=(SegmentType.LINE,),
    ... )

    >>> # Edge with multiple segments
    >>> edge2 = StructuralCurveEdge(
    ...     name="IE2",
    ...     surface_member="S3",
    ...     nodes=("N1", "N2", "N3", "N4"),
    ...     segments=(
    ...         SegmentType.LINE,
    ...         SegmentType.CIRCULAR_ARC,
    ...         SegmentType.LINE,
    ...     ),
    ... )

    >>> # Edge with parent ID for curved geometry
    >>> edge3 = StructuralCurveEdge(
    ...     name="IE3",
    ...     surface_member="S1",
    ...     nodes=("N5", "N6"),
    ...     segments=(SegmentType.BEZIER,),
    ...     parent_id="12345678-1234-5678-1234-567812345678",
    ... )
    """

    name: str
    surface_member: str
    nodes: tuple[str, ...]
    segments: tuple[SegmentType, ...]
    parent_id: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate curve edge properties.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.surface_member:
            raise ValueError("surface_member cannot be empty")

        if len(self.nodes) < 2:
            raise ValueError("nodes must contain at least 2 nodes")

        if len(self.segments) != len(self.nodes) - 1:
            raise ValueError(f"segments length ({len(self.segments)}) must equal nodes length minus 1 ({len(self.nodes) - 1})")

        # Validate that all node names are non-empty
        for i, node in enumerate(self.nodes):
            if not node:
                raise ValueError(f"Node name at index {i} cannot be empty")
