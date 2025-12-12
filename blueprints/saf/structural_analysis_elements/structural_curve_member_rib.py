"""Rib member definition for structural analysis following SAF specification.

A 1D structural member (rib) associated with slabs, where the slab's cooperating portion
is termed the effective width.
"""

from dataclasses import dataclass
from enum import Enum


class RibAlignmentType(str, Enum):
    """Alignment of rib relative to slab following SAF specification.

    Defines how the rib cross-section is positioned relative to the slab surface.
    """

    BOTTOM = "Bottom"
    CENTRE = "Centre"
    TOP = "Top"


class RibConnectionType(str, Enum):
    """Type of shear connection for composite action following SAF specification.

    Defines the shear connection methodology between rib and slab.
    """

    FULL_SHEAR_CONNECTION = "Full shear connection"
    PARTIAL_SHEAR_CONNECTION = "Partial shear connection"
    WITHOUT_COMPOSITE_ACTION = "Without Composite Action"
    USER_DEFINED_ECCENTRICITY = "User Defined Eccentricity"


class RibShapeType(str, Enum):
    """Shape of the rib effective width following SAF specification.

    Defines the effective width configuration for composite calculations.
    """

    T_SYMMETRIC = "T Symmetric"
    RIGHT = "Right"
    LEFT = "Left"
    T_NON_SYMMETRIC = "T Non-symmetric"


class RibBehaviourType(str, Enum):
    """Behaviour in analysis for rib member following SAF specification.

    Defines the force transfer capability of the rib.
    """

    STANDARD = "Standard"
    AXIAL_FORCE_ONLY = "Axial force only"


class RibEffectiveWidthType(str, Enum):
    """Method for specifying effective width following SAF specification.

    Defines how effective width is determined.
    """

    NUMBER_OF_THICKNESS = "Number Of Thickness"
    WIDTH = "Width"


class SegmentType(str, Enum):
    """Segment type between consecutive nodes following SAF specification."""

    LINE = "Line"
    CIRCULAR_ARC = "Circular Arc"
    BEZIER = "Bezier"
    PARABOLIC_ARC = "Parabolic arc"
    SPLINE = "Spline"


@dataclass(frozen=True)
class StructuralCurveMemberRib:
    """Structural rib member (1D member on slab) following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralcurvememberrib.html.

    A 1D structural member (rib) associated with slabs, where the slab's cooperating
    portion is termed the effective width.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "R1").
    two_d_member : str
        Reference to parent StructuralSurfaceMember by name.
    cross_section : str
        Reference to StructuralCrossSection by name.
    nodes : tuple[str, ...]
        Ordered nodes from beginning to end. Must contain at least 2 nodes.
    segments : tuple[SegmentType, ...]
        Shape between consecutive nodes. Length must be len(nodes) - 1.
    geometrical_shape : str
        Overall curve type of the rib (e.g., "Line", "Circular Arc").
    alignment : RibAlignmentType
        Cross-section positioning relative to slab.
    eccentricity_z : float
        Z-direction offset from gravity center in millimeters.
    connection_type : RibConnectionType
        Shear connection methodology.
    shape_of_rib : RibShapeType
        Effective width configuration.
    behaviour : RibBehaviourType
        Force transfer capability.
    effective_width_type : RibEffectiveWidthType
        Width specification method.
    width_left : float
        Left width parameter in millimeters.
    width_right : float
        Right width parameter in millimeters.
    internal_nodes : tuple[str, ...], optional
        Non-geometry-defining nodes (e.g., analysis points).
    length : float | None, optional
        Distance between endpoints in meters.
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
        If name, two_d_member, or cross_section is empty.
        If fewer than 2 nodes are provided.
        If number of segments doesn't match nodes - 1.
        If any node name is empty.
        If any internal node name is empty.

    Examples
    --------
    >>> from blueprints.saf import (
    ...     StructuralCurveMemberRib,
    ...     RibAlignmentType,
    ...     RibConnectionType,
    ...     RibShapeType,
    ...     RibBehaviourType,
    ...     RibEffectiveWidthType,
    ... )
    >>> from blueprints.saf import SegmentType as RibSegmentType
    >>> # Simple rib on slab
    >>> rib = StructuralCurveMemberRib(
    ...     name="R1",
    ...     two_d_member="S1",
    ...     cross_section="CS1",
    ...     nodes=("N1", "N2"),
    ...     segments=(RibSegmentType.LINE,),
    ...     geometrical_shape="Line",
    ...     alignment=RibAlignmentType.CENTRE,
    ...     eccentricity_z=0.0,
    ...     connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
    ...     shape_of_rib=RibShapeType.T_SYMMETRIC,
    ...     behaviour=RibBehaviourType.STANDARD,
    ...     effective_width_type=RibEffectiveWidthType.WIDTH,
    ...     width_left=500.0,
    ...     width_right=500.0,
    ... )

    >>> # Rib with multiple segments and eccentricity
    >>> rib_curved = StructuralCurveMemberRib(
    ...     name="R2",
    ...     two_d_member="S2",
    ...     cross_section="CS2",
    ...     nodes=("N3", "N4", "N5"),
    ...     segments=(RibSegmentType.CIRCULAR_ARC, RibSegmentType.LINE),
    ...     geometrical_shape="Circular Arc",
    ...     alignment=RibAlignmentType.BOTTOM,
    ...     eccentricity_z=50.0,
    ...     connection_type=RibConnectionType.PARTIAL_SHEAR_CONNECTION,
    ...     shape_of_rib=RibShapeType.RIGHT,
    ...     behaviour=RibBehaviourType.STANDARD,
    ...     effective_width_type=RibEffectiveWidthType.NUMBER_OF_THICKNESS,
    ...     width_left=3.0,
    ...     width_right=3.0,
    ... )
    """

    name: str
    two_d_member: str
    cross_section: str
    nodes: tuple[str, ...]
    segments: tuple[SegmentType, ...]
    geometrical_shape: str
    alignment: RibAlignmentType
    eccentricity_z: float
    connection_type: RibConnectionType
    shape_of_rib: RibShapeType
    behaviour: RibBehaviourType
    effective_width_type: RibEffectiveWidthType
    width_left: float
    width_right: float
    internal_nodes: tuple[str, ...] = ()
    length: float | None = None
    layer: str = ""
    color: str = ""
    parent_id: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate rib member properties.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.two_d_member:
            raise ValueError("two_d_member cannot be empty")
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
