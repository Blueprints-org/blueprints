"""Structural curve connection definitions following SAF specification.

Curve connections define line supports on 1D members or ribs that constrain
movement along six independent parameters: three translational and three rotational axes.
"""

from dataclasses import dataclass
from enum import Enum


class TranslationConstraint(str, Enum):
    """Translation constraint type for curve connection following SAF specification.

    Specifies constraint behavior in translational directions.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"
    COMPRESSION_ONLY = "Compression only"
    TENSION_ONLY = "Tension only"


class RotationConstraint(str, Enum):
    """Rotation constraint type for curve connection following SAF specification.

    Specifies constraint behavior in rotational directions.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"


class CoordinateSystem(str, Enum):
    """Coordinate system for curve connection following SAF specification.

    Global or local coordinate system reference.
    """

    GLOBAL = "Global"
    LOCAL = "Local"


class Origin(str, Enum):
    """Origin reference for curve connection following SAF specification.

    Specifies whether position is measured from start or end of member.
    """

    FROM_START = "From start"
    FROM_END = "From end"


class CoordinateDefinition(str, Enum):
    """Coordinate definition type for curve connection following SAF specification.

    Specifies whether position is absolute (meters) or relative (percentage).
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class SupportType(str, Enum):
    """Support type classification for curve connection following SAF specification.

    Informational classification of support behavior.
    """

    FIXED = "Fixed"
    HINGED = "Hinged"
    SLIDING = "Sliding"
    CUSTOM = "Custom"


@dataclass(frozen=True)
class StructuralCurveConnection:
    """Structural curve connection following SAF specification.

    Definition following https://www.saf.guide/en/stable/supports-and-hinges/structuralcurveconnection.html.

    Defines line supports on 1D members or ribs that constrain movement along six
    independent parameters: three translational and three rotational axes.

    Attributes
    ----------
    name : str
        Human-readable unique identifier.
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
        Position measured from start or end of member.
    start_point : float
        Support position start location.
    end_point : float
        Support position end location.
    member : str, optional
        StructuralCurveMember identifier. Required if support attaches to curve member.
    member_rib : str, optional
        StructuralCurveMemberRib identifier. Required if support attaches to rib.
    support_type : SupportType, optional
        Informational classification of support behavior.
    parent_id : str, optional
        Populated when curved geometry is segmented (UUID format).
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If both member and member_rib are None.
        If both member and member_rib are specified.

    Examples
    --------
    >>> from blueprints.saf import (
    ...     StructuralCurveConnection,
    ...     TranslationConstraint,
    ...     RotationConstraint,
    ...     CoordinateSystem,
    ...     Origin,
    ...     CoordinateDefinition,
    ... )
    >>> # Curve connection on beam
    >>> connection = StructuralCurveConnection(
    ...     name="Sc1",
    ...     member="B1",
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
    """

    name: str
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
    member: str | None = None
    member_rib: str | None = None
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
        self._validate_member_requirements()

    def _validate_member_requirements(self) -> None:
        """Validate that exactly one of member or member_rib is specified."""
        if self.member is None and self.member_rib is None:
            raise ValueError("Either member or member_rib must be specified")
        if self.member is not None and self.member_rib is not None:
            raise ValueError("Cannot specify both member and member_rib")
