"""Structural edge connection definitions following SAF specification.

Edge connections define line supports on edges of 2D structural members that
constrain movement along six independent parameters: three translational and
three rotational axes.
"""

from dataclasses import dataclass
from enum import Enum


class BoundaryCondition(str, Enum):
    """Boundary condition type for edge connection following SAF specification.

    Specifies the type of edge the support is applied to.
    """

    ON_EDGE = "On edge"
    ON_SUBREGION_EDGE = "On subregion edge"
    ON_OPENING_EDGE = "On opening edge"
    ON_INTERNAL_EDGE = "On internal edge"


class TranslationConstraint(str, Enum):
    """Translation constraint type for edge connection following SAF specification.

    Specifies constraint behavior in translational directions.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"
    COMPRESSION_ONLY = "Compression only"
    TENSION_ONLY = "Tension only"


class RotationConstraint(str, Enum):
    """Rotation constraint type for edge connection following SAF specification.

    Specifies constraint behavior in rotational directions.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"


class CoordinateSystem(str, Enum):
    """Coordinate system for edge connection following SAF specification.

    Global or local coordinate system reference.
    """

    GLOBAL = "Global"
    LOCAL = "Local"


class Origin(str, Enum):
    """Origin reference for edge connection following SAF specification.

    Specifies whether position is measured from start or end of edge.
    """

    FROM_START = "From start"
    FROM_END = "From end"


class CoordinateDefinition(str, Enum):
    """Coordinate definition type for edge connection following SAF specification.

    Specifies whether position is absolute (meters) or relative (percentage).
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class SupportType(str, Enum):
    """Support type classification for edge connection following SAF specification.

    Informational classification of support behavior.
    """

    FIXED = "Fixed"
    HINGED = "Hinged"
    SLIDING = "Sliding"
    CUSTOM = "Custom"


@dataclass(frozen=True)
class StructuralEdgeConnection:
    """Structural edge connection following SAF specification.

    Definition following https://www.saf.guide/en/stable/supports-and-hinges/structuraledgeconnection.html.

    Defines line supports on edges of 2D structural members that constrain
    movement along six independent parameters: three translational and three
    rotational axes.

    Attributes
    ----------
    name : str
        Human-readable unique identifier.
    boundary_condition : BoundaryCondition
        Type of edge: On edge, On subregion edge, On opening edge, or On internal edge.
    ux : TranslationConstraint
        Translation constraint in X direction.
    uy : TranslationConstraint
        Translation constraint in Y direction.
    uz : TranslationConstraint
        Translation constraint in Z direction.
    fix : RotationConstraint
        Rotation constraint around X axis.
    fiy : RotationConstraint
        Rotation constraint around Y axis.
    fiz : RotationConstraint
        Rotation constraint around Z axis.
    coordinate_system : CoordinateSystem
        Global or local coordinate system reference.
    coordinate_definition : CoordinateDefinition
        Absolute (meters) or relative (percentage) position definition.
    origin : Origin
        Position measured from start or end of edge.
    start_point : float
        Support position start location.
    end_point : float
        Support position end location.
    two_d_member : str, optional
        StructuralSurfaceMember identifier. Required when boundary_condition = ON_EDGE.
    two_d_member_region : str, optional
        StructuralSurfaceRegion identifier. Required when boundary_condition = ON_SUBREGION_EDGE.
    two_d_member_opening : str, optional
        StructuralSurfaceOpening identifier. Required when boundary_condition = ON_OPENING_EDGE.
    internal_edge : str, optional
        Internal edge identifier. Required when boundary_condition = ON_INTERNAL_EDGE.
    edge_index : int, optional
        1-based index of the edge (edge numbering starts at 1).
    support_type : SupportType, optional
        Informational classification of support behavior.
    parent_id : str, optional
        Populated when geometry is segmented (UUID format).
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If boundary_condition = ON_EDGE but two_d_member is not specified.
        If boundary_condition = ON_SUBREGION_EDGE but two_d_member_region is not specified.
        If boundary_condition = ON_OPENING_EDGE but two_d_member_opening is not specified.
        If boundary_condition = ON_INTERNAL_EDGE but internal_edge is not specified.

    Examples
    --------
    >>> from blueprints.saf import StructuralEdgeConnection, BoundaryCondition, TranslationConstraint, RotationConstraint
    >>> # Edge connection on 2D member
    >>> connection = StructuralEdgeConnection(
    ...     name="Se1",
    ...     two_d_member="M1",
    ...     boundary_condition=BoundaryCondition.ON_EDGE,
    ...     ux=TranslationConstraint.RIGID,
    ...     uy=TranslationConstraint.RIGID,
    ...     uz=TranslationConstraint.RIGID,
    ...     fix=RotationConstraint.RIGID,
    ...     fiy=RotationConstraint.RIGID,
    ...     fiz=RotationConstraint.RIGID,
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     origin=Origin.FROM_START,
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     start_point=0.0,
    ...     end_point=1.0,
    ... )

    >>> # Hinged connection on subregion edge
    >>> hinged = StructuralEdgeConnection(
    ...     name="Se2",
    ...     two_d_member_region="R1",
    ...     boundary_condition=BoundaryCondition.ON_SUBREGION_EDGE,
    ...     ux=TranslationConstraint.RIGID,
    ...     uy=TranslationConstraint.RIGID,
    ...     uz=TranslationConstraint.RIGID,
    ...     fix=RotationConstraint.FREE,
    ...     fiy=RotationConstraint.FREE,
    ...     fiz=RotationConstraint.FREE,
    ...     coordinate_system=CoordinateSystem.LOCAL,
    ...     origin=Origin.FROM_START,
    ...     coordinate_definition=CoordinateDefinition.RELATIVE,
    ...     start_point=0.0,
    ...     end_point=100.0,
    ...     edge_index=2,
    ... )
    """

    name: str
    boundary_condition: BoundaryCondition
    ux: TranslationConstraint
    uy: TranslationConstraint
    uz: TranslationConstraint
    fix: RotationConstraint
    fiy: RotationConstraint
    fiz: RotationConstraint
    coordinate_system: CoordinateSystem
    coordinate_definition: CoordinateDefinition
    origin: Origin
    start_point: float
    end_point: float
    two_d_member: str | None = None
    two_d_member_region: str | None = None
    two_d_member_opening: str | None = None
    internal_edge: str | None = None
    edge_index: int | None = None
    support_type: SupportType | None = None
    parent_id: str | None = None
    id: str = ""

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_boundary_condition_requirements()

    def _validate_boundary_condition_requirements(self) -> None:
        """Validate requirements based on boundary condition type."""
        if self.boundary_condition == BoundaryCondition.ON_EDGE and self.two_d_member is None:
            raise ValueError("two_d_member must be specified when boundary_condition = ON_EDGE")
        if self.boundary_condition == BoundaryCondition.ON_SUBREGION_EDGE and self.two_d_member_region is None:
            raise ValueError("two_d_member_region must be specified when boundary_condition = ON_SUBREGION_EDGE")
        if self.boundary_condition == BoundaryCondition.ON_OPENING_EDGE and self.two_d_member_opening is None:
            raise ValueError("two_d_member_opening must be specified when boundary_condition = ON_OPENING_EDGE")
        if self.boundary_condition == BoundaryCondition.ON_INTERNAL_EDGE and self.internal_edge is None:
            raise ValueError("internal_edge must be specified when boundary_condition = ON_INTERNAL_EDGE")
