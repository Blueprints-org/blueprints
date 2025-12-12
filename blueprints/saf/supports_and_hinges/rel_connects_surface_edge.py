"""Hinge definitions for 2D member edges following SAF specification.

Rel connects surface edge defines hinges on 2D member edges with partial or
no constraints, allowing partial continuity.
"""

from dataclasses import dataclass
from enum import Enum


class Constraint(str, Enum):
    """Constraint type for hinge degree of freedom following SAF specification.

    Specifies constraint behavior for a degree of freedom.
    """

    FREE = "Free"
    RIGID = "Rigid"
    FLEXIBLE = "Flexible"


class CoordinateDefinition(str, Enum):
    """Coordinate definition type for edge hinge following SAF specification.

    Specifies whether position is absolute (meters) or relative (percentage).
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class Origin(str, Enum):
    """Origin reference for edge hinge following SAF specification.

    Specifies whether position is measured from start or end of edge.
    """

    FROM_START = "From start"
    FROM_END = "From end"


@dataclass(frozen=True)
class RelConnectsSurfaceEdge:
    """Hinge on 2D member edge following SAF specification.

    Definition following https://www.saf.guide/en/stable/supports-and-hinges/relconnectssurfaceedge.html.

    Defines hinges on 2D member edges with partial or no constraints, allowing
    partial continuity at edge connections.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "H1").
    two_d_member : str
        StructuralSurfaceMember identifier that this hinge connects to.
    edge : int
        0-based index of the edge (edge numbering starts at 0). CRITICAL: Unlike other SAF objects
        which use 1-based indexing, edge indices are 0-based.
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
    coordinate_definition : CoordinateDefinition
        Absolute (meters) or relative (percentage) position definition.
    origin : Origin
        Position measured from start or end of edge.
    start_point : float
        Hinge position start location.
    end_point : float
        Hinge position end location.
    ux_stiffness : float, optional
        Stiffness in X direction when ux = FLEXIBLE [MN/m²]. Required when ux = FLEXIBLE.
    uy_stiffness : float, optional
        Stiffness in Y direction when uy = FLEXIBLE [MN/m²]. Required when uy = FLEXIBLE.
    uz_stiffness : float, optional
        Stiffness in Z direction when uz = FLEXIBLE [MN/m²]. Required when uz = FLEXIBLE.
    fix_stiffness : float, optional
        Stiffness around X axis when fix = FLEXIBLE [MNm/rad/m]. Required when fix = FLEXIBLE.
    fiy_stiffness : float, optional
        Stiffness around Y axis when fiy = FLEXIBLE [MNm/rad/m]. Required when fiy = FLEXIBLE.
    fiz_stiffness : float, optional
        Stiffness around Z axis when fiz = FLEXIBLE [MNm/rad/m]. Required when fiz = FLEXIBLE.
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
    >>> from blueprints.saf import RelConnectsSurfaceEdge, Constraint, CoordinateDefinition, Origin
    >>> # Hinged edge (free rotations, rigid translations)
    >>> hinge = RelConnectsSurfaceEdge(
    ...     name="H1",
    ...     two_d_member="M1",
    ...     edge=0,
    ...     ux=Constraint.RIGID,
    ...     uy=Constraint.RIGID,
    ...     uz=Constraint.RIGID,
    ...     fix=Constraint.FREE,
    ...     fiy=Constraint.FREE,
    ...     fiz=Constraint.FREE,
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     origin=Origin.FROM_START,
    ...     start_point=0.0,
    ...     end_point=1.0,
    ... )

    >>> # Flexible hinge (partial constraints)
    >>> flexible_hinge = RelConnectsSurfaceEdge(
    ...     name="H2",
    ...     two_d_member="M2",
    ...     edge=1,
    ...     ux=Constraint.RIGID,
    ...     uy=Constraint.FLEXIBLE,
    ...     uz=Constraint.RIGID,
    ...     fix=Constraint.RIGID,
    ...     fiy=Constraint.FLEXIBLE,
    ...     fiz=Constraint.RIGID,
    ...     coordinate_definition=CoordinateDefinition.RELATIVE,
    ...     origin=Origin.FROM_START,
    ...     start_point=0.0,
    ...     end_point=100.0,
    ...     uy_stiffness=500.0,
    ...     fiy_stiffness=250.0,
    ... )
    """

    name: str
    two_d_member: str
    edge: int
    ux: Constraint
    uy: Constraint
    uz: Constraint
    fix: Constraint
    fiy: Constraint
    fiz: Constraint
    coordinate_definition: CoordinateDefinition
    origin: Origin
    start_point: float
    end_point: float
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
