"""Hinge definitions for 1D structural members following SAF specification.

Rel connects structural member defines hinges on 1D members with partial or
no constraints on one or both ends, allowing partial continuity.
"""

from dataclasses import dataclass
from enum import Enum


class Position(str, Enum):
    """Position type for hinge on member following SAF specification.

    Specifies where the hinge is located on the member.
    """

    BEGIN = "Begin"
    END = "End"
    BOTH = "Both"


class Constraint(str, Enum):
    """Constraint type for hinge degree of freedom following SAF specification.

    Specifies constraint behavior for a degree of freedom.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"


@dataclass(frozen=True)
class RelConnectsStructuralMember:
    """Hinge on 1D structural member following SAF specification.

    Definition following https://www.saf.guide/en/stable/supports-and-hinges/relconnectsstructuralmember.html.

    Defines hinges on 1D members with partial or no constraints, allowing
    partial continuity at connections.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "H1").
    member : str
        StructuralMember identifier that this hinge connects to.
    position : Position
        Hinge location: Begin, End, or Both (applies to both ends).
    ux : Constraint
        Translation constraint in X direction.
    uy : Constraint
        Translation constraint in Y direction.
    uz : Constraint
        Translation constraint in Z direction.
    fix : Constraint
        Rotation constraint around X axis.
    fiy : Constraint
        Rotation constraint around Y axis.
    fiz : Constraint
        Rotation constraint around Z axis.
    ux_stiffness : float, optional
        Stiffness in X direction when ux = FLEXIBLE [MN/m]. Required when ux = FLEXIBLE.
    uy_stiffness : float, optional
        Stiffness in Y direction when uy = FLEXIBLE [MN/m]. Required when uy = FLEXIBLE.
    uz_stiffness : float, optional
        Stiffness in Z direction when uz = FLEXIBLE [MN/m]. Required when uz = FLEXIBLE.
    fix_stiffness : float, optional
        Stiffness around X axis when fix = FLEXIBLE [MNm/rad]. Required when fix = FLEXIBLE.
    fiy_stiffness : float, optional
        Stiffness around Y axis when fiy = FLEXIBLE [MNm/rad]. Required when fiy = FLEXIBLE.
    fiz_stiffness : float, optional
        Stiffness around Z axis when fiz = FLEXIBLE [MNm/rad]. Required when fiz = FLEXIBLE.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If ux = FLEXIBLE but ux_stiffness is not specified.
        If uy = FLEXIBLE but uy_stiffness is not specified.
        If uz = FLEXIBLE but uz_stiffness is not specified.
        If fix = FLEXIBLE but fix_stiffness is not specified.
        If fiy = FLEXIBLE but fiy_stiffness is not specified.
        If fiz = FLEXIBLE but fiz_stiffness is not specified.

    Examples
    --------
    >>> from blueprints.saf import RelConnectsStructuralMember, Constraint, Position
    >>> # Hinged end (free rotations, rigid translations)
    >>> hinge = RelConnectsStructuralMember(
    ...     name="H1",
    ...     member="B1",
    ...     position=Position.END,
    ...     ux=Constraint.RIGID,
    ...     uy=Constraint.RIGID,
    ...     uz=Constraint.RIGID,
    ...     fix=Constraint.FREE,
    ...     fiy=Constraint.FREE,
    ...     fiz=Constraint.FREE,
    ... )

    >>> # Flexible hinge (partial constraints)
    >>> flexible_hinge = RelConnectsStructuralMember(
    ...     name="H2",
    ...     member="B2",
    ...     position=Position.BOTH,
    ...     ux=Constraint.RIGID,
    ...     uy=Constraint.FLEXIBLE,
    ...     uz=Constraint.RIGID,
    ...     fix=Constraint.RIGID,
    ...     fiy=Constraint.FLEXIBLE,
    ...     fiz=Constraint.RIGID,
    ...     uy_stiffness=1000.0,
    ...     fiy_stiffness=500.0,
    ... )
    """

    name: str
    member: str
    position: Position
    ux: Constraint
    uy: Constraint
    uz: Constraint
    fix: Constraint
    fiy: Constraint
    fiz: Constraint
    ux_stiffness: float | None = None
    uy_stiffness: float | None = None
    uz_stiffness: float | None = None
    fix_stiffness: float | None = None
    fiy_stiffness: float | None = None
    fiz_stiffness: float | None = None
    id: str = ""

    def __post_init__(self) -> None:
        """Validate stiffness requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_stiffness_requirements()

    def _validate_stiffness_requirements(self) -> None:
        """Validate that stiffness values are provided when constraints are flexible."""
        if self.ux == Constraint.FLEXIBLE and self.ux_stiffness is None:
            raise ValueError("ux_stiffness must be specified when ux = Constraint.FLEXIBLE")
        if self.uy == Constraint.FLEXIBLE and self.uy_stiffness is None:
            raise ValueError("uy_stiffness must be specified when uy = Constraint.FLEXIBLE")
        if self.uz == Constraint.FLEXIBLE and self.uz_stiffness is None:
            raise ValueError("uz_stiffness must be specified when uz = Constraint.FLEXIBLE")
        if self.fix == Constraint.FLEXIBLE and self.fix_stiffness is None:
            raise ValueError("fix_stiffness must be specified when fix = Constraint.FLEXIBLE")
        if self.fiy == Constraint.FLEXIBLE and self.fiy_stiffness is None:
            raise ValueError("fiy_stiffness must be specified when fiy = Constraint.FLEXIBLE")
        if self.fiz == Constraint.FLEXIBLE and self.fiz_stiffness is None:
            raise ValueError("fiz_stiffness must be specified when fiz = Constraint.FLEXIBLE")
