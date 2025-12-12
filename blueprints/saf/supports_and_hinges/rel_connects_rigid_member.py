"""Rigid member connection definitions following SAF specification.

Rel connects rigid member enables connections between up to two of: nodes,
1D members, 2D member edges, or internal edges.
"""

from dataclasses import dataclass
from enum import Enum


class RigidType(str, Enum):
    """Rigid connection type following SAF specification.

    Defines whether connection uses automatic (Fixed) or user-defined (Custom) behavior.
    """

    FIXED = "Fixed"
    CUSTOM = "Custom"


class TranslationConstraint(str, Enum):
    """Translation constraint type for rigid member connection following SAF specification.

    Specifies constraint behavior in translational directions.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"
    COMPRESSION_ONLY = "Compression only"
    TENSION_ONLY = "Tension only"
    FLEXIBLE_COMPRESSION_ONLY = "Flexible compression only"
    FLEXIBLE_TENSION_ONLY = "Flexible tension only"
    NON_LINEAR = "Non linear"


class RotationConstraint(str, Enum):
    """Rotation constraint type for rigid member connection following SAF specification.

    Specifies constraint behavior in rotational directions.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"
    NON_LINEAR = "Non linear"


@dataclass(frozen=True)
class RelConnectsRigidMember:
    """Rigid member connection following SAF specification.

    Definition following https://www.saf.guide/en/stable/supports-and-hinges/relconnectsrigidmember.html.

    Enables connections between up to two of: nodes (StructuralPointConnection),
    1D members (StructuralCurveMember), 2D member edges (StructuralSurfaceMember),
    or internal edges (StructuralCurveEdge). Local coordinate system is given by
    first node and its related object.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "RM1").
    connection_type : RigidType
        Type: Fixed (automatic constraints) or Custom (user-defined).
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
    ux_stiffness : float, optional
        Stiffness in X direction when ux is flexible [MN/m²].
        Required when ux = FLEXIBLE or ux is flexible variant or ux = NON_LINEAR.
    uy_stiffness : float, optional
        Stiffness in Y direction when uy is flexible [MN/m²].
        Required when uy = FLEXIBLE or uy is flexible variant or uy = NON_LINEAR.
    uz_stiffness : float, optional
        Stiffness in Z direction when uz is flexible [MN/m²].
        Required when uz = FLEXIBLE or uz is flexible variant or uz = NON_LINEAR.
    fix_stiffness : float, optional
        Stiffness around X axis when fix is flexible [MNm/rad/m].
        Required when fix = FLEXIBLE or fix = NON_LINEAR.
    fiy_stiffness : float, optional
        Stiffness around Y axis when fiy is flexible [MNm/rad/m].
        Required when fiy = FLEXIBLE or fiy = NON_LINEAR.
    fiz_stiffness : float, optional
        Stiffness around Z axis when fiz is flexible [MNm/rad/m].
        Required when fiz = FLEXIBLE or fiz = NON_LINEAR.
    ux_resistance : float, optional
        Resistance in X direction for non-linear behavior [MN/m].
        Required when ux = NON_LINEAR.
    uy_resistance : float, optional
        Resistance in Y direction for non-linear behavior [MN/m].
        Required when uy = NON_LINEAR.
    uz_resistance : float, optional
        Resistance in Z direction for non-linear behavior [MN/m].
        Required when uz = NON_LINEAR.
    fix_resistance : float, optional
        Resistance around X axis for non-linear behavior [MNm/m].
        Required when fix = NON_LINEAR.
    fiy_resistance : float, optional
        Resistance around Y axis for non-linear behavior [MNm/m].
        Required when fiy = NON_LINEAR.
    fiz_resistance : float, optional
        Resistance around Z axis for non-linear behavior [MNm/m].
        Required when fiz = NON_LINEAR.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If flexibility-related constraint has no corresponding stiffness.
        If non-linear constraint has no corresponding resistance.

    Examples
    --------
    >>> from blueprints.saf import RelConnectsRigidMember, RigidType, TranslationConstraint, RotationConstraint
    >>> # Fixed rigid member connection
    >>> connection = RelConnectsRigidMember(
    ...     name="RM1",
    ...     connection_type=RigidType.FIXED,
    ...     ux=TranslationConstraint.RIGID,
    ...     uy=TranslationConstraint.RIGID,
    ...     uz=TranslationConstraint.RIGID,
    ...     fix=RotationConstraint.RIGID,
    ...     fiy=RotationConstraint.RIGID,
    ...     fiz=RotationConstraint.RIGID,
    ... )

    >>> # Custom flexible member connection
    >>> flexible_connection = RelConnectsRigidMember(
    ...     name="RM2",
    ...     connection_type=RigidType.CUSTOM,
    ...     ux=TranslationConstraint.FLEXIBLE,
    ...     uy=TranslationConstraint.RIGID,
    ...     uz=TranslationConstraint.RIGID,
    ...     fix=RotationConstraint.FLEXIBLE,
    ...     fiy=RotationConstraint.RIGID,
    ...     fiz=RotationConstraint.RIGID,
    ...     ux_stiffness=1000.0,
    ...     fix_stiffness=500.0,
    ... )
    """

    name: str
    connection_type: RigidType
    ux: TranslationConstraint
    uy: TranslationConstraint
    uz: TranslationConstraint
    fix: RotationConstraint
    fiy: RotationConstraint
    fiz: RotationConstraint
    ux_stiffness: float | None = None
    uy_stiffness: float | None = None
    uz_stiffness: float | None = None
    fix_stiffness: float | None = None
    fiy_stiffness: float | None = None
    fiz_stiffness: float | None = None
    ux_resistance: float | None = None
    uy_resistance: float | None = None
    uz_resistance: float | None = None
    fix_resistance: float | None = None
    fiy_resistance: float | None = None
    fiz_resistance: float | None = None
    id: str = ""

    def __post_init__(self) -> None:
        """Validate stiffness and resistance requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_stiffness_and_resistance_requirements()

    def _validate_stiffness_and_resistance_requirements(self) -> None:  # noqa: C901
        """Validate stiffness and resistance parameters based on constraints."""
        # Validate ux constraints
        if self._is_flexible_or_nonlinear(self.ux) and self.ux_stiffness is None:
            raise ValueError("ux_stiffness must be specified when ux is flexible or non-linear")
        if self.ux == TranslationConstraint.NON_LINEAR and self.ux_resistance is None:
            raise ValueError("ux_resistance must be specified when ux = NON_LINEAR")

        # Validate uy constraints
        if self._is_flexible_or_nonlinear(self.uy) and self.uy_stiffness is None:
            raise ValueError("uy_stiffness must be specified when uy is flexible or non-linear")
        if self.uy == TranslationConstraint.NON_LINEAR and self.uy_resistance is None:
            raise ValueError("uy_resistance must be specified when uy = NON_LINEAR")

        # Validate uz constraints
        if self._is_flexible_or_nonlinear(self.uz) and self.uz_stiffness is None:
            raise ValueError("uz_stiffness must be specified when uz is flexible or non-linear")
        if self.uz == TranslationConstraint.NON_LINEAR and self.uz_resistance is None:
            raise ValueError("uz_resistance must be specified when uz = NON_LINEAR")

        # Validate fix constraints
        if self._is_flexible_or_nonlinear_rotation(self.fix) and self.fix_stiffness is None:
            raise ValueError("fix_stiffness must be specified when fix is flexible or non-linear")
        if self.fix == RotationConstraint.NON_LINEAR and self.fix_resistance is None:
            raise ValueError("fix_resistance must be specified when fix = NON_LINEAR")

        # Validate fiy constraints
        if self._is_flexible_or_nonlinear_rotation(self.fiy) and self.fiy_stiffness is None:
            raise ValueError("fiy_stiffness must be specified when fiy is flexible or non-linear")
        if self.fiy == RotationConstraint.NON_LINEAR and self.fiy_resistance is None:
            raise ValueError("fiy_resistance must be specified when fiy = NON_LINEAR")

        # Validate fiz constraints
        if self._is_flexible_or_nonlinear_rotation(self.fiz) and self.fiz_stiffness is None:
            raise ValueError("fiz_stiffness must be specified when fiz is flexible or non-linear")
        if self.fiz == RotationConstraint.NON_LINEAR and self.fiz_resistance is None:
            raise ValueError("fiz_resistance must be specified when fiz = NON_LINEAR")

    @staticmethod
    def _is_flexible_or_nonlinear(constraint: TranslationConstraint) -> bool:
        """Check if translation constraint is flexible or non-linear variant."""
        return constraint in (
            TranslationConstraint.FLEXIBLE,
            TranslationConstraint.FLEXIBLE_COMPRESSION_ONLY,
            TranslationConstraint.FLEXIBLE_TENSION_ONLY,
            TranslationConstraint.NON_LINEAR,
        )

    @staticmethod
    def _is_flexible_or_nonlinear_rotation(constraint: RotationConstraint) -> bool:
        """Check if rotation constraint is flexible or non-linear."""
        return constraint in (
            RotationConstraint.FLEXIBLE,
            RotationConstraint.NON_LINEAR,
        )
