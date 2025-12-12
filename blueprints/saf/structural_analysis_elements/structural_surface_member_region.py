"""Surface member region definition for structural analysis following SAF specification.

A region within a surface member with a specific thickness and material.
"""

from dataclasses import dataclass
from enum import Enum


class SystemPlaneType(str, Enum):
    """Position of system plane relative to physical section following SAF specification.

    Defines the alignment of the analytical axis relative to the physical section.
    """

    BOTTOM = "Bottom"
    CENTRE = "Centre"
    TOP = "Top"


class EdgeType(str, Enum):
    """Edge type between consecutive nodes following SAF specification.

    Defines the curve shape between consecutive nodes.
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
class StructuralSurfaceMemberRegion:
    """Structural surface member region following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralsurfacememberregion.html.

    A region within a surface member defining a particular area with specific thickness
    and material properties.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "R1").
    material : str
        Reference to StructuralMaterial by name.
    thickness : float
        Total thickness in millimeters.
    system_plane_at : SystemPlaneType
        Position of system plane relative to physical section.
    two_d_member : str
        Reference to parent StructuralSurfaceMember by name.
    nodes : tuple[str, ...]
        Node names defining geometry. Must contain at least 3 nodes.
    edges : tuple[EdgeType, ...]
        Edge types between consecutive nodes. Length must equal len(nodes).
    eccentricity_z : float
        Offset from system plane in Z direction in millimeters.
    area : float | None, optional
        Surface area in square meters.
    parent_id : str, optional
        Parent ID for tracking segmented curved geometry (UUID format).
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name or material is empty.
        If two_d_member is empty.
        If fewer than 3 nodes are provided.
        If edges length doesn't match nodes length.
        If any node name is empty.

    Examples
    --------
    >>> from blueprints.saf import StructuralSurfaceMemberRegion, SystemPlaneType, EdgeType
    >>> # Simple rectangular region
    >>> region = StructuralSurfaceMemberRegion(
    ...     name="R1",
    ...     material="MAT1",
    ...     thickness=200.0,
    ...     system_plane_at=SystemPlaneType.CENTRE,
    ...     two_d_member="S1",
    ...     nodes=("N1", "N2", "N3", "N4"),
    ...     edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
    ...     eccentricity_z=0.0,
    ... )

    >>> # Region with curved edges and eccentricity
    >>> region_curved = StructuralSurfaceMemberRegion(
    ...     name="R2",
    ...     material="MAT2",
    ...     thickness=250.0,
    ...     system_plane_at=SystemPlaneType.TOP,
    ...     two_d_member="S2",
    ...     nodes=("N1", "N2", "N3"),
    ...     edges=(EdgeType.CIRCULAR_ARC, EdgeType.BEZIER, EdgeType.LINE),
    ...     eccentricity_z=-50.0,
    ...     area=5.5,
    ... )
    """

    name: str
    material: str
    thickness: float
    system_plane_at: SystemPlaneType
    two_d_member: str
    nodes: tuple[str, ...]
    edges: tuple[EdgeType, ...]
    eccentricity_z: float
    area: float | None = None
    parent_id: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate surface member region properties.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.material:
            raise ValueError("material cannot be empty")
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
