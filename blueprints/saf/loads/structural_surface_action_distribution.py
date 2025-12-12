"""Structural surface action distribution definitions following SAF specification.

Surface action distribution describes how surface loads distribute to other structural
members, addressing "load panels" and "load distribution" scenarios.
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class Type(str, Enum):
    """Distribution type for surface action following SAF specification.

    Specifies where the load distributes.
    """

    NODES = "Nodes"
    EDGES = "Edges"
    BEAMS_AND_EDGES = "Beams and edges"


class LcsType(str, Enum):
    """Local coordinate system type for surface action distribution following SAF specification.

    Establishes local coordinate system orientation.
    """

    X_BY_VECTOR = "x by vector"
    Y_BY_VECTOR = "y by vector"
    TILT_OF_VECTOR_DEFINED_BY_POINT = "Tilt of vector defined by point"


class DistributionTo(str, Enum):
    """Distribution direction for surface action following SAF specification.

    Specifies load distribution method.
    """

    ONE_WAY_X = "One way - X"
    ONE_WAY_Y = "One way - Y"
    TWO_WAY = "Two way"


class Edge(str, Enum):
    """Edge type for polygon segments following SAF specification.

    Specifies how nodes are connected.
    """

    LINE = "Line"
    CIRCULAR_ARC = "Circular arc"
    CIRCLE_BY_3_POINTS = "Circle by 3 points"
    CIRCLE_AND_POINT = "Circle and point"
    PARABOLIC_ARC = "Parabolic arc"
    BEZIER = "Bezier"
    SPLINE = "Spline"


@dataclass(frozen=True)
class StructuralSurfaceActionDistribution:
    """Structural surface action distribution following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralsurfaceactiondistribution-1.html.

    This object describes how surface loads distribute to other structural members,
    addressing "load panels" and "load distribution" scenarios.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "FL1").
    type : Type
        Distribution type: Nodes, Edges, or Beams and edges.
    nodes : str
        Node identifiers that define the distribution shape, semicolon-separated (e.g., "N81;N263;N659;N660").
    edges : str
        Edge types between consecutive nodes, semicolon-separated (e.g., "Line;Circular arc;Line").
    lcs_type : LcsType
        Local coordinate system orientation: x by vector, y by vector, or Tilt of vector defined by point.
    coordinate_x : float
        X-direction coordinate of vector in meters.
    coordinate_y : float
        Y-direction coordinate of vector in meters.
    coordinate_z : float
        Z-direction coordinate of vector in meters.
    lcs_rotation : float
        Rotation angle around Z axis in degrees that defines distribution angle.
    distribution_to : DistributionTo
        Load distribution method: One way - X, One way - Y, or Two way.
    layer : str, optional
        Layer identifier (e.g., "Load panel").
    load_applied_to : str, optional
        Beam identifiers where load is applied, semicolon-separated (e.g., "B1;B2;B3;B5").
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If nodes is empty string.
        If edges is empty string.

    Examples
    --------
    >>> from blueprints.saf import StructuralSurfaceActionDistribution, Type, LcsType, DistributionTo
    >>> # Distribute load to nodes
    >>> dist = StructuralSurfaceActionDistribution(
    ...     name="FL1",
    ...     type=Type.NODES,
    ...     nodes="N81;N263;N659;N660",
    ...     edges="Line;Line;Line;Line",
    ...     lcs_type=LcsType.X_BY_VECTOR,
    ...     coordinate_x=1.0,
    ...     coordinate_y=0.0,
    ...     coordinate_z=1.2,
    ...     lcs_rotation=45.0,
    ...     distribution_to=DistributionTo.ONE_WAY_X,
    ... )

    >>> # Distribute to beams and edges
    >>> dist_beams = StructuralSurfaceActionDistribution(
    ...     name="FL2",
    ...     type=Type.BEAMS_AND_EDGES,
    ...     nodes="N1;N2;N3;N4",
    ...     edges="Line;Line;Line;Line",
    ...     lcs_type=LcsType.Y_BY_VECTOR,
    ...     coordinate_x=0.0,
    ...     coordinate_y=1.0,
    ...     coordinate_z=0.0,
    ...     lcs_rotation=0.0,
    ...     distribution_to=DistributionTo.TWO_WAY,
    ...     load_applied_to="B1;B2;B3;B5",
    ... )
    """

    name: str
    type: Type
    nodes: str
    edges: str
    lcs_type: LcsType
    coordinate_x: float
    coordinate_y: float
    coordinate_z: float
    lcs_rotation: float
    distribution_to: DistributionTo
    layer: str = ""
    load_applied_to: str = ""
    id: str = ""

    _SEPARATOR: ClassVar[str] = ";"

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_required_fields()

    def _validate_required_fields(self) -> None:
        """Validate that required fields are not empty."""
        if not self.nodes:
            raise ValueError("nodes cannot be empty string")
        if not self.edges:
            raise ValueError("edges cannot be empty string")
