"""Curve member definition for structural analysis following SAF specification.

A 1D structural member (beam, column, truss) with defined local coordinate system.
"""

from dataclasses import dataclass
from enum import Enum


class GeometricalShapeType(str, Enum):
    """Geometrical shape type for curve members following SAF specification.

    Defines the overall curve type of the member.
    """

    LINE = "Line"
    CIRCULAR_ARC = "Circular Arc"
    PARABOLIC_ARC = "Parabolic Arc"
    BEZIER = "Bezier"
    SPLINE = "Spline"
    POLYLINE = "Polyline"


class LCSType(str, Enum):
    """Local Coordinate System determination following SAF specification.

    Defines how the local coordinate system is oriented relative to the global system.
    """

    Y_BY_VECTOR = "y by vector"
    Z_BY_VECTOR = "z by vector"
    Y_BY_POINT = "y by point"
    Z_BY_POINT = "z by point"


class SystemLineType(str, Enum):
    """System line position following SAF specification.

    Defines the alignment of the analytical axis relative to the physical section.
    """

    CENTRE = "Centre"
    TOP = "Top"
    BOTTOM = "Bottom"
    LEFT = "Left"
    RIGHT = "Right"
    TOP_LEFT = "Top left"
    TOP_RIGHT = "Top right"
    BOTTOM_LEFT = "Bottom left"
    BOTTOM_RIGHT = "Bottom right"


class BehaviourType(str, Enum):
    """Behaviour in analysis following SAF specification.

    Defines the force transfer capability of the member.
    """

    STANDARD = "Standard"
    AXIAL_FORCE_ONLY = "Axial force only"
    COMPRESSION_ONLY = "Compression only"
    TENSION_ONLY = "Tension only"


class SegmentType(str, Enum):
    """Segment type between consecutive nodes following SAF specification."""

    LINE = "Line"
    CIRCULAR_ARC = "Circular Arc"
    BEZIER = "Bezier"
    PARABOLIC_ARC = "Parabolic arc"
    SPLINE = "Spline"


@dataclass(frozen=True)
class StructuralCurveMember:
    """Structural curve member definition following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralcurvemember.html.

    A 1D structural member (beam, column, truss member, etc.) defined by a sequence of nodes
    with a unique local coordinate system originating at the start point.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "B1", "C1").
    cross_section : str
        Reference to StructuralCrossSection by name (e.g., "CS1").
    nodes : tuple[str, ...]
        Ordered nodes from beginning to end. First node is begin point, last is end point.
        Must contain at least 2 nodes.
    segments : tuple[SegmentType, ...]
        Shape between consecutive nodes. Length must be len(nodes) - 1.
    member_type : str, optional
        Classification within analytical model (e.g., "Beam", "Column", "General").
    arbitrary_definition : str, optional
        Reference to varying/tapered beam definition.
    internal_nodes : tuple[str, ...], optional
        Non-geometry-defining nodes (e.g., analysis points).
    length : float, optional
        Distance between endpoints in meters.
    geometrical_shape : GeometricalShapeType, optional
        Overall curve type of the member.
    lcs : LCSType
        Local coordinate system determination method.
    lcs_rotation : float
        Rotation around x-axis in degrees. Required.
    lcs_x : float
        X coordinate for LCS definition in meters.
    lcs_y : float
        Y coordinate for LCS definition in meters.
    lcs_z : float
        Z coordinate for LCS definition in meters.
    system_line : SystemLineType
        Alignment of analytical axis relative to physical section.
    behaviour : BehaviourType
        Force transfer capability of the member.
    structural_y_eccentricity_begin : float, optional
        Physical-to-analytical offset begin (display only) in millimeters.
    structural_y_eccentricity_end : float, optional
        Physical-to-analytical offset end (display only) in millimeters.
    structural_z_eccentricity_begin : float, optional
        Physical-to-analytical offset begin (display only) in millimeters.
    structural_z_eccentricity_end : float, optional
        Physical-to-analytical offset end (display only) in millimeters.
    analysis_y_eccentricity_begin : float
        Physical-to-analytical offset begin (affects forces) in millimeters.
    analysis_y_eccentricity_end : float
        Physical-to-analytical offset end (affects forces) in millimeters.
    analysis_z_eccentricity_begin : float
        Physical-to-analytical offset begin (affects forces) in millimeters.
    analysis_z_eccentricity_end : float
        Physical-to-analytical offset end (affects forces) in millimeters.
    layer : str, optional
        Custom grouping classification.
    color : str, optional
        Hex color format (#AARRGGBB).
    parent_id : str, optional
        Parent ID for segmented curved geometry tracking (UUID format).
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name or cross_section is empty.
        If fewer than 2 nodes are provided.
        If number of segments doesn't match nodes - 1.

    Examples
    --------
    >>> from blueprints.saf import StructuralCurveMember, SegmentType, LCSType, SystemLineType, BehaviourType
    >>> # Simple beam
    >>> beam = StructuralCurveMember(
    ...     name="B1",
    ...     cross_section="CS1",
    ...     nodes=("N1", "N2"),
    ...     segments=(SegmentType.LINE,),
    ...     lcs=LCSType.Z_BY_VECTOR,
    ...     lcs_rotation=0.0,
    ...     lcs_x=0.0,
    ...     lcs_y=0.0,
    ...     lcs_z=1.0,
    ...     system_line=SystemLineType.CENTRE,
    ...     behaviour=BehaviourType.STANDARD,
    ...     analysis_y_eccentricity_begin=0.0,
    ...     analysis_y_eccentricity_end=0.0,
    ...     analysis_z_eccentricity_begin=0.0,
    ...     analysis_z_eccentricity_end=0.0,
    ... )

    >>> # Curved member with multiple segments
    >>> curved_beam = StructuralCurveMember(
    ...     name="B2",
    ...     cross_section="CS2",
    ...     nodes=("N3", "N4", "N5"),
    ...     segments=(
    ...         SegmentType.CIRCULAR_ARC,
    ...         SegmentType.LINE,
    ...     ),
    ...     member_type="Beam",
    ...     geometrical_shape=GeometricalShapeType.CIRCULAR_ARC,
    ...     lcs=LCSType.Y_BY_VECTOR,
    ...     lcs_rotation=45.0,
    ...     lcs_x=1.0,
    ...     lcs_y=0.0,
    ...     lcs_z=0.0,
    ...     system_line=SystemLineType.TOP,
    ...     behaviour=BehaviourType.STANDARD,
    ...     analysis_y_eccentricity_begin=50.0,
    ...     analysis_y_eccentricity_end=50.0,
    ...     analysis_z_eccentricity_begin=0.0,
    ...     analysis_z_eccentricity_end=0.0,
    ... )
    """

    name: str
    cross_section: str
    nodes: tuple[str, ...]
    segments: tuple[SegmentType, ...]
    lcs: LCSType
    lcs_rotation: float
    lcs_x: float
    lcs_y: float
    lcs_z: float
    system_line: SystemLineType
    behaviour: BehaviourType
    analysis_y_eccentricity_begin: float
    analysis_y_eccentricity_end: float
    analysis_z_eccentricity_begin: float
    analysis_z_eccentricity_end: float
    member_type: str = ""
    arbitrary_definition: str = ""
    internal_nodes: tuple[str, ...] = ()
    length: float | None = None
    geometrical_shape: GeometricalShapeType | None = None
    structural_y_eccentricity_begin: float | None = None
    structural_y_eccentricity_end: float | None = None
    structural_z_eccentricity_begin: float | None = None
    structural_z_eccentricity_end: float | None = None
    layer: str = ""
    color: str = ""
    parent_id: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate curve member properties.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.cross_section:
            raise ValueError("cross_section cannot be empty")

        if len(self.nodes) < 2:
            raise ValueError("nodes must contain at least 2 nodes")

        if len(self.segments) != len(self.nodes) - 1:
            raise ValueError(f"segments length ({len(self.segments)}) must equal nodes length minus 1 ({len(self.nodes) - 1})")

        # Validate that all node names are non-empty
        for i, node in enumerate(self.nodes):
            if not node:
                raise ValueError(f"Node name at index {i} cannot be empty")

        # Validate internal nodes are non-empty if provided
        for i, node in enumerate(self.internal_nodes):
            if not node:
                raise ValueError(f"Internal node name at index {i} cannot be empty")
