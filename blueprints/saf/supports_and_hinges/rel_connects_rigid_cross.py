"""Rigid cross connection definitions for crossing 1D members following SAF specification.

Rel connects rigid cross defines structural behavior at nodes where two 1D
elements are being crossed and commonly used for structural bracing.
"""

from dataclasses import dataclass
from enum import Enum


class Constraint(str, Enum):
    """Constraint type for crossing member degree of freedom following SAF specification.

    Specifies constraint behavior for a degree of freedom.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"
    COMPRESSION_ONLY = "Compression only"
    TENSION_ONLY = "Tension only"
    FLEXIBLE_COMPRESSION_ONLY = "Flexible compression only"
    FLEXIBLE_TENSION_ONLY = "Flexible tension only"
    NON_LINEAR = "Non linear"


class ConnectionType(str, Enum):
    """Connection type classification for rigid cross following SAF specification.

    Informational classification of connection behavior.
    """

    FIXED = "Fixed"
    HINGED = "Hinged"
    CUSTOM = "Custom"


@dataclass(frozen=True)
class RelConnectsRigidCross:
    """Rigid cross connection at node where two 1D members cross following SAF specification.

    Definition following https://www.saf.guide/en/stable/supports-and-hinges/relconnectsrigidcross.html.

    Defines structural behavior at a node where two 1D elements cross, commonly
    used for structural bracing. Connection axes derive from member orientation:
    first axis aligns with member 1, second with member 2, third perpendicular
    to the plane they define.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "RC1").
    member1 : str
        First StructuralCurveMember identifier.
    member2 : str
        Second StructuralCurveMember identifier.
    u1 : Constraint
        Translation constraint for member 1.
    u2 : Constraint
        Translation constraint for member 2.
    u : Constraint
        Translation constraint for the cross direction (perpendicular to both members).
    fi1 : Constraint
        Rotation constraint for member 1.
    fi2 : Constraint
        Rotation constraint for member 2.
    fi : Constraint
        Rotation constraint for the cross direction.
    u1_stiffness : float, optional
        Stiffness in member 1 direction when u1 = FLEXIBLE [MN/m].
        Required when u1 = FLEXIBLE or u1 is flexible variant or u1 = NON_LINEAR.
    u2_stiffness : float, optional
        Stiffness in member 2 direction when u2 = FLEXIBLE [MN/m].
        Required when u2 = FLEXIBLE or u2 is flexible variant or u2 = NON_LINEAR.
    u_stiffness : float, optional
        Stiffness in cross direction when u = FLEXIBLE [MN/m].
        Required when u = FLEXIBLE or u is flexible variant or u = NON_LINEAR.
    fi1_stiffness : float, optional
        Stiffness in member 1 rotation when fi1 = FLEXIBLE [MNm/rad].
        Required when fi1 = FLEXIBLE or fi1 = NON_LINEAR.
    fi2_stiffness : float, optional
        Stiffness in member 2 rotation when fi2 = FLEXIBLE [MNm/rad].
        Required when fi2 = FLEXIBLE or fi2 = NON_LINEAR.
    fi_stiffness : float, optional
        Stiffness in cross rotation when fi = FLEXIBLE [MNm/rad].
        Required when fi = FLEXIBLE or fi = NON_LINEAR.
    u1_resistance : float, optional
        Maximum allowable strain in member 1 direction when u1 = NON_LINEAR [MN].
        Required when u1 = NON_LINEAR.
    u2_resistance : float, optional
        Maximum allowable strain in member 2 direction when u2 = NON_LINEAR [MN].
        Required when u2 = NON_LINEAR.
    u_resistance : float, optional
        Maximum allowable strain in cross direction when u = NON_LINEAR [MN].
        Required when u = NON_LINEAR.
    fi1_resistance : float, optional
        Maximum allowable rotation in member 1 when fi1 = NON_LINEAR [MNm].
        Required when fi1 = NON_LINEAR.
    fi2_resistance : float, optional
        Maximum allowable rotation in member 2 when fi2 = NON_LINEAR [MNm].
        Required when fi2 = NON_LINEAR.
    fi_resistance : float, optional
        Maximum allowable rotation in cross when fi = NON_LINEAR [MNm].
        Required when fi = NON_LINEAR.
    connection_type : ConnectionType, optional
        Informational classification of connection behavior.
    parent_id : str, optional
        Populated when geometry is segmented (UUID format).
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If flexibility-related constraint has no corresponding stiffness.
        If non-linear constraint has no corresponding resistance.

    Examples
    --------
    >>> from blueprints.saf import RelConnectsRigidCross, Constraint
    >>> # Fixed rigid cross
    >>> connection = RelConnectsRigidCross(
    ...     name="RC1",
    ...     member1="B1",
    ...     member2="B3",
    ...     u1=Constraint.RIGID,
    ...     u2=Constraint.RIGID,
    ...     u=Constraint.RIGID,
    ...     fi1=Constraint.RIGID,
    ...     fi2=Constraint.RIGID,
    ...     fi=Constraint.RIGID,
    ... )

    >>> # Flexible cross with stiffness
    >>> flexible_cross = RelConnectsRigidCross(
    ...     name="RC2",
    ...     member1="B2",
    ...     member2="B4",
    ...     u1=Constraint.FLEXIBLE,
    ...     u2=Constraint.RIGID,
    ...     u=Constraint.FLEXIBLE,
    ...     fi1=Constraint.RIGID,
    ...     fi2=Constraint.RIGID,
    ...     fi=Constraint.RIGID,
    ...     u1_stiffness=1000.0,
    ...     u_stiffness=500.0,
    ... )
    """

    name: str
    member1: str
    member2: str
    u1: Constraint
    u2: Constraint
    u: Constraint
    fi1: Constraint
    fi2: Constraint
    fi: Constraint
    u1_stiffness: float | None = None
    u2_stiffness: float | None = None
    u_stiffness: float | None = None
    fi1_stiffness: float | None = None
    fi2_stiffness: float | None = None
    fi_stiffness: float | None = None
    u1_resistance: float | None = None
    u2_resistance: float | None = None
    u_resistance: float | None = None
    fi1_resistance: float | None = None
    fi2_resistance: float | None = None
    fi_resistance: float | None = None
    connection_type: ConnectionType | None = None
    parent_id: str | None = None
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
        # Validate u1 constraints
        if self._is_flexible_or_nonlinear(self.u1) and self.u1_stiffness is None:
            raise ValueError("u1_stiffness must be specified when u1 is flexible or non-linear")
        if self.u1 == Constraint.NON_LINEAR and self.u1_resistance is None:
            raise ValueError("u1_resistance must be specified when u1 = NON_LINEAR")

        # Validate u2 constraints
        if self._is_flexible_or_nonlinear(self.u2) and self.u2_stiffness is None:
            raise ValueError("u2_stiffness must be specified when u2 is flexible or non-linear")
        if self.u2 == Constraint.NON_LINEAR and self.u2_resistance is None:
            raise ValueError("u2_resistance must be specified when u2 = NON_LINEAR")

        # Validate u constraints
        if self._is_flexible_or_nonlinear(self.u) and self.u_stiffness is None:
            raise ValueError("u_stiffness must be specified when u is flexible or non-linear")
        if self.u == Constraint.NON_LINEAR and self.u_resistance is None:
            raise ValueError("u_resistance must be specified when u = NON_LINEAR")

        # Validate fi1 constraints
        if self._is_flexible_or_nonlinear(self.fi1) and self.fi1_stiffness is None:
            raise ValueError("fi1_stiffness must be specified when fi1 is flexible or non-linear")
        if self.fi1 == Constraint.NON_LINEAR and self.fi1_resistance is None:
            raise ValueError("fi1_resistance must be specified when fi1 = NON_LINEAR")

        # Validate fi2 constraints
        if self._is_flexible_or_nonlinear(self.fi2) and self.fi2_stiffness is None:
            raise ValueError("fi2_stiffness must be specified when fi2 is flexible or non-linear")
        if self.fi2 == Constraint.NON_LINEAR and self.fi2_resistance is None:
            raise ValueError("fi2_resistance must be specified when fi2 = NON_LINEAR")

        # Validate fi constraints
        if self._is_flexible_or_nonlinear(self.fi) and self.fi_stiffness is None:
            raise ValueError("fi_stiffness must be specified when fi is flexible or non-linear")
        if self.fi == Constraint.NON_LINEAR and self.fi_resistance is None:
            raise ValueError("fi_resistance must be specified when fi = NON_LINEAR")

    @staticmethod
    def _is_flexible_or_nonlinear(constraint: Constraint) -> bool:
        """Check if constraint is flexible or non-linear variant."""
        return constraint in (
            Constraint.FLEXIBLE,
            Constraint.FLEXIBLE_COMPRESSION_ONLY,
            Constraint.FLEXIBLE_TENSION_ONLY,
            Constraint.NON_LINEAR,
        )
