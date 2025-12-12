"""Surface member definition for structural analysis following SAF specification.

A 2D structural member representing face members such as slabs, walls, and shells.
"""

from dataclasses import dataclass
from enum import Enum


class ThicknessType(str, Enum):
    """Thickness variation type following SAF specification.

    Defines how thickness varies across the surface member.
    """

    CONSTANT = "Constant"
    VARIABLE_X = "Variable in global X"
    VARIABLE_Y = "Variable in global Y"
    VARIABLE_Z = "Variable in global Z"
    VARIABLE_LOCAL_X = "Variable in local X"
    VARIABLE_LOCAL_Y = "Variable in local Y"
    VARIABLE_XY = "Variable in direction XY"
    VARIABLE_RADIAL = "Variable radially"


class SystemPlaneType(str, Enum):
    """Position of system plane relative to physical section following SAF specification.

    Defines the alignment of the analytical axis relative to the physical section.
    """

    BOTTOM = "Bottom"
    CENTRE = "Centre"
    TOP = "Top"


class SurfaceEdgeType(str, Enum):
    """Edge type between consecutive nodes following SAF specification.

    Defines the curve shape between consecutive nodes.
    """

    LINE = "Line"
    CIRCULAR_ARC = "Circular Arc"
    CIRCLE_BY_3_POINTS = "Circle by 3 points"
    PARABOLIC_ARC = "Parabolic arc"
    BEZIER = "Bezier"
    SPLINE = "Spline"
    CIRCLE = "Circle"
    POINT = "Point"


class LCSType(str, Enum):
    """Local Coordinate System determination following SAF specification.

    Defines how the local coordinate system is oriented relative to the global system.
    """

    X_BY_VECTOR = "x by vector"
    Y_BY_VECTOR = "y by vector"
    TILT_OF_VECTOR_BY_POINT = "Tilt of vector defined by point"


class BehaviourType(str, Enum):
    """Behaviour in analysis following SAF specification.

    Defines the mechanical behaviour of the surface member.
    """

    ISOTROPIC = "Isotropic"
    ORTHOTROPIC = "Orthotropic"
    MEMBRANE = "Membrane"
    PRESS_ONLY = "Press only"


@dataclass(frozen=True)
class StructuralSurfaceMember:
    """Structural surface member (2D member) following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralsurfacemember.html.

    A 2D structural member representing face members such as slabs, walls, and shells.
    Can be planar or curved, with constant or variable thickness.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "S1", "W1").
    material : str
        Reference to StructuralMaterial by name.
    thickness_type : ThicknessType
        How thickness varies across the member.
    thickness : str
        Single value (e.g., "200") or node-based format (e.g., "N1:200; N2:250").
    system_plane_at : SystemPlaneType
        Position of system plane relative to physical section.
    nodes : tuple[str, ...]
        Semicolon-separated node names defining geometry. Must have at least 3.
    edges : tuple[SurfaceEdgeType, ...]
        Edge types between consecutive nodes. Length must be len(nodes).
    lcs_type : LCSType
        Local coordinate system determination method.
    lcs_x : float
        X coordinate for LCS definition in meters.
    lcs_y : float
        Y coordinate for LCS definition in meters.
    lcs_z : float
        Z coordinate for LCS definition in meters.
    lcs_rotation : float
        Rotation around normal axis in degrees.
    behaviour : BehaviourType
        Mechanical behaviour in analysis.
    type : str, optional
        Classification (e.g., "Plate", "Wall", "Shell").
    internal_nodes : tuple[str, ...], optional
        Non-geometry-defining nodes.
    area : float | None, optional
        Surface area in square meters.
    layer : str, optional
        Custom grouping classification.
    structural_z_eccentricity : float | None, optional
        Physical-to-analytical offset in Z direction (display only) in millimeters.
    shape : str, optional
        Shape classification ("Flat" or "Curved").
    color : str, optional
        Hex color format (#AARRGGBB).
    parent_id : str, optional
        Parent ID for segmented curved geometry tracking (UUID format).
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name or material is empty.
        If fewer than 3 nodes are provided.
        If edges length doesn't match nodes length.
        If any node name is empty.
        If any internal node name is empty.

    Examples
    --------
    >>> from blueprints.saf import StructuralSurfaceMember, ThicknessType, SystemPlaneType, SurfaceEdgeType, LCSType, BehaviourType
    >>> # Simple slab
    >>> slab = StructuralSurfaceMember(
    ...     name="S1",
    ...     material="M1",
    ...     thickness_type=ThicknessType.CONSTANT,
    ...     thickness="200",
    ...     system_plane_at=SystemPlaneType.CENTRE,
    ...     nodes=("N1", "N2", "N3", "N4"),
    ...     edges=(SurfaceEdgeType.LINE, SurfaceEdgeType.LINE, SurfaceEdgeType.LINE, SurfaceEdgeType.LINE),
    ...     lcs_type=LCSType.X_BY_VECTOR,
    ...     lcs_x=1.0,
    ...     lcs_y=0.0,
    ...     lcs_z=0.0,
    ...     lcs_rotation=0.0,
    ...     behaviour=BehaviourType.ISOTROPIC,
    ... )

    >>> # Wall with variable thickness
    >>> wall = StructuralSurfaceMember(
    ...     name="W1",
    ...     material="M2",
    ...     thickness_type=ThicknessType.VARIABLE_Y,
    ...     thickness="N1:250; N2:300",
    ...     system_plane_at=SystemPlaneType.CENTRE,
    ...     nodes=("N1", "N2", "N3", "N4"),
    ...     edges=(SurfaceEdgeType.LINE, SurfaceEdgeType.LINE, SurfaceEdgeType.LINE, SurfaceEdgeType.LINE),
    ...     lcs_type=LCSType.Y_BY_VECTOR,
    ...     lcs_x=0.0,
    ...     lcs_y=1.0,
    ...     lcs_z=0.0,
    ...     lcs_rotation=0.0,
    ...     behaviour=BehaviourType.ORTHOTROPIC,
    ...     type="Wall",
    ...     structural_z_eccentricity=0.0,
    ... )
    """

    name: str
    material: str
    thickness_type: ThicknessType
    thickness: str
    system_plane_at: SystemPlaneType
    nodes: tuple[str, ...]
    edges: tuple[SurfaceEdgeType, ...]
    lcs_type: LCSType
    lcs_x: float
    lcs_y: float
    lcs_z: float
    lcs_rotation: float
    behaviour: BehaviourType
    type: str = ""
    internal_nodes: tuple[str, ...] = ()
    area: float | None = None
    layer: str = ""
    structural_z_eccentricity: float | None = None
    shape: str = ""
    color: str = ""
    parent_id: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate surface member properties.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.material:
            raise ValueError("material cannot be empty")

        if len(self.nodes) < 3:
            raise ValueError("nodes must contain at least 3 nodes")

        if len(self.edges) != len(self.nodes):
            raise ValueError(f"edges length ({len(self.edges)}) must equal nodes length ({len(self.nodes)})")

        # Validate that all node names are non-empty
        for i, node in enumerate(self.nodes):
            if not node:
                raise ValueError(f"Node name at index {i} cannot be empty")

        # Validate internal nodes are non-empty if provided
        for i, node in enumerate(self.internal_nodes):
            if not node:
                raise ValueError(f"Internal node name at index {i} cannot be empty")
