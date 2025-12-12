"""Surface member opening definition for structural analysis following SAF specification.

Openings in face members that define cutouts within surface members.
"""

from dataclasses import dataclass
from enum import Enum


class EdgeType(str, Enum):
    """Edge type between consecutive nodes following SAF specification.

    Defines the curve shape between consecutive nodes of an opening.
    """

    LINE = "Line"
    BEZIER = "Bezier"
    CIRCULAR_ARC = "Circular Arc"
    PARABOLIC_ARC = "Parabolic arc"
    SPLINE = "Spline"
    CIRCLE = "Circle"
    CIRCLE_BY_3_POINTS = "Circle by 3 points"
    POINT = "Point"


@dataclass(frozen=True)
class StructuralSurfaceMemberOpening:
    """Structural surface member opening following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralsurfacememberopening.html.

    An opening (cutout) within a surface member with geometry that can be planar or curved.
    Opening boundaries cannot touch or cross each other.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "O1", "Opening1").
    two_d_member : str
        Reference to parent StructuralSurfaceMember by name.
    nodes : tuple[str, ...]
        Semicolon-separated node names defining opening boundary geometry.
        Must contain at least 3 nodes to form a closed polygon.
    edges : tuple[EdgeType, ...]
        Edge types between consecutive nodes. Length must equal len(nodes).
    area : float | None, optional
        Surface area of the opening in square meters.
    parent_id : str, optional
        Parent ID for tracking segmented curved geometry (UUID format).
    id : str, optional
        Unique universal identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name or two_d_member is empty.
        If fewer than 3 nodes are provided.
        If edges length doesn't match nodes length.
        If any node name is empty.

    Notes
    -----
    The edges of one opening cannot touch nor cross each other. When necessary,
    create two or more openings instead.

    Examples
    --------
    >>> from blueprints.saf import StructuralSurfaceMemberOpening, EdgeType
    >>> # Simple rectangular opening
    >>> opening = StructuralSurfaceMemberOpening(
    ...     name="O1",
    ...     two_d_member="S1",
    ...     nodes=("O1_N1", "O1_N2", "O1_N3", "O1_N4"),
    ...     edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
    ... )

    >>> # Circular opening with area
    >>> opening_circular = StructuralSurfaceMemberOpening(
    ...     name="O2",
    ...     two_d_member="S2",
    ...     nodes=("O2_N1", "O2_N2", "O2_N3"),
    ...     edges=(EdgeType.CIRCLE_BY_3_POINTS, EdgeType.CIRCLE_BY_3_POINTS, EdgeType.CIRCLE_BY_3_POINTS),
    ...     area=0.5,
    ... )

    >>> # Curved opening with Bezier edges
    >>> opening_curved = StructuralSurfaceMemberOpening(
    ...     name="O3",
    ...     two_d_member="S3",
    ...     nodes=("O3_N1", "O3_N2", "O3_N3", "O3_N4"),
    ...     edges=(EdgeType.BEZIER, EdgeType.BEZIER, EdgeType.BEZIER, EdgeType.BEZIER),
    ...     area=1.2,
    ... )
    """

    name: str
    two_d_member: str
    nodes: tuple[str, ...]
    edges: tuple[EdgeType, ...]
    area: float | None = None
    parent_id: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate surface member opening properties.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.two_d_member:
            raise ValueError("two_d_member cannot be empty")

        if len(self.nodes) < 3:
            raise ValueError("nodes must contain at least 3 nodes")

        if len(self.edges) != len(self.nodes):
            raise ValueError(f"edges length ({len(self.edges)}) must equal nodes length ({len(self.nodes)})")

        # Validate that all node names are non-empty
        for i, node in enumerate(self.nodes):
            if not node:
                raise ValueError(f"Node name at index {i} cannot be empty")
