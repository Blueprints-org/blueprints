"""Structural point support definitions following SAF specification.

Point supports define boundary conditions at nodes or on beams using six parameters:
three translational (X, Y, Z) and three rotational (around X, Y, Z axes).
"""

from dataclasses import dataclass
from enum import Enum


class BoundaryCondition(str, Enum):
    """Boundary condition type for point support following SAF specification.

    Specifies whether support is located at a node or on a beam.
    """

    IN_NODE = "In node"
    ON_BEAM = "On beam"


class TranslationConstraint(str, Enum):
    """Translation constraint type for point support following SAF specification.

    Specifies constraint behavior in translational directions.
    """

    RIGID = "Rigid"
    FREE = "Free"
    FLEXIBLE = "Flexible"
    COMPRESSION_ONLY = "Compression only"
    TENSION_ONLY = "Tension only"
    FLEXIBLE_COMPRESSION_ONLY = "Flexible compression only"
    FLEXIBLE_TENSION_ONLY = "Flexible tension only"
    NON_LINEAR = "Non linear"


class RotationConstraint(str, Enum):
    """Rotation constraint type for point support following SAF specification.

    Specifies constraint behavior in rotational directions.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"
    NON_LINEAR = "Non linear"


class CoordinateSystem(str, Enum):
    """Coordinate system for point support on beam following SAF specification.

    Global or local coordinate system reference.
    """

    GLOBAL = "Global"
    LOCAL = "Local"


class Origin(str, Enum):
    """Origin reference for point support on beam following SAF specification.

    Specifies whether position is measured from start or end of member.
    """

    FROM_START = "From start"
    FROM_END = "From end"


class CoordinateDefinition(str, Enum):
    """Coordinate definition type for point support on beam following SAF specification.

    Specifies whether position is absolute (meters) or relative (percentage).
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class SupportType(str, Enum):
    """Support type classification for point support following SAF specification.

    Informational classification of support behavior.
    """

    FIXED = "Fixed"
    HINGED = "Hinged"
    SLIDING = "Sliding"
    CUSTOM = "Custom"


@dataclass(frozen=True)
class StructuralPointSupport:
    """Structural point support following SAF specification.

    Definition following https://www.saf.guide/en/stable/supports-and-hinges/structuralpointsupport.html.

    Defines boundary conditions at nodes or on beams using six parameters: three
    translational (X, Y, Z) and three rotational (around X, Y, Z axes).

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "Sn6").
    boundary_condition : BoundaryCondition
        Support location: In node or On beam.
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
    node : str, optional
        Node identifier. Required when boundary_condition = IN_NODE.
    member : str, optional
        Member identifier. Required when boundary_condition = ON_BEAM.
    coordinate_system : CoordinateSystem, optional
        Coordinate system. Required when boundary_condition = ON_BEAM.
    origin : Origin, optional
        Position reference. Required when boundary_condition = ON_BEAM.
    coordinate_definition : CoordinateDefinition, optional
        Position definition type. Required when boundary_condition = ON_BEAM.
    position_x : float, optional
        Position along member in meters or percentage. Required when boundary_condition = ON_BEAM.
    support_type : SupportType, optional
        Informational classification of support behavior.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If boundary_condition = IN_NODE but node is not specified.
        If boundary_condition = ON_BEAM but member is not specified.
        If boundary_condition = ON_BEAM but coordinate_system is not specified.
        If boundary_condition = ON_BEAM but origin is not specified.
        If boundary_condition = ON_BEAM but coordinate_definition is not specified.
        If boundary_condition = ON_BEAM but position_x is not specified.

    Examples
    --------
    >>> from blueprints.saf import StructuralPointSupport, BoundaryCondition, TranslationConstraint, RotationConstraint
    >>> # Node support with all rigid constraints
    >>> support = StructuralPointSupport(
    ...     name="Sn6",
    ...     boundary_condition=BoundaryCondition.IN_NODE,
    ...     node="N1",
    ...     ux=TranslationConstraint.RIGID,
    ...     uy=TranslationConstraint.RIGID,
    ...     uz=TranslationConstraint.RIGID,
    ...     fix=RotationConstraint.RIGID,
    ...     fiy=RotationConstraint.RIGID,
    ...     fiz=RotationConstraint.RIGID,
    ... )

    >>> # Hinged support (fixed translation, free rotation)
    >>> hinged = StructuralPointSupport(
    ...     name="Sn7",
    ...     boundary_condition=BoundaryCondition.IN_NODE,
    ...     node="N2",
    ...     ux=TranslationConstraint.RIGID,
    ...     uy=TranslationConstraint.RIGID,
    ...     uz=TranslationConstraint.RIGID,
    ...     fix=RotationConstraint.FREE,
    ...     fiy=RotationConstraint.FREE,
    ...     fiz=RotationConstraint.FREE,
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
    node: str | None = None
    member: str | None = None
    coordinate_system: CoordinateSystem | None = None
    origin: Origin | None = None
    coordinate_definition: CoordinateDefinition | None = None
    position_x: float | None = None
    support_type: SupportType | None = None
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
        if self.boundary_condition == BoundaryCondition.IN_NODE:
            if self.node is None:
                raise ValueError("node must be specified when boundary_condition = IN_NODE")
        elif self.boundary_condition == BoundaryCondition.ON_BEAM:
            if self.member is None:
                raise ValueError("member must be specified when boundary_condition = ON_BEAM")
            if self.coordinate_system is None:
                raise ValueError("coordinate_system must be specified when boundary_condition = ON_BEAM")
            if self.origin is None:
                raise ValueError("origin must be specified when boundary_condition = ON_BEAM")
            if self.coordinate_definition is None:
                raise ValueError("coordinate_definition must be specified when boundary_condition = ON_BEAM")
            if self.position_x is None:
                raise ValueError("position_x must be specified when boundary_condition = ON_BEAM")
