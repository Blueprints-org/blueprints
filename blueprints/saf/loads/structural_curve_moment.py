"""Structural curve moment (distributed line moment) definitions following SAF specification.

Curve moments represent distributed line moments applied to 1D members or 2D member edges.
Can be constant or trapezoidal, acting around X, Y, Z axes.
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class MomentDirection(str, Enum):
    """Direction (axis) of curve moment following SAF specification.

    Specifies the axis around which the moment acts.
    """

    MX = "Mx"
    MY = "My"
    MZ = "Mz"


class ForceAction(str, Enum):
    """Type of curve moment application following SAF specification.

    Specifies where the moment load is applied.
    """

    ON_BEAM = "On beam"
    ON_EDGE = "On edge"
    ON_SUBREGION_EDGE = "On subregion edge"
    ON_OPENING_EDGE = "On opening edge"
    ON_RIB = "On rib"
    ON_INTERNAL_EDGE = "On internal edge"


class Distribution(str, Enum):
    """Distribution type of curve moment following SAF specification.

    Specifies how the moment varies along the member.
    """

    UNIFORM = "Uniform"
    TRAPEZ = "Trapez"


class CoordinateSystem(str, Enum):
    """Coordinate system for curve moment following SAF specification.

    Global or local coordinate system reference.
    """

    GLOBAL = "Global"
    LOCAL = "Local"


class Location(str, Enum):
    """Location type for curve moment application following SAF specification.

    Specifies whether moment is applied based on length or projection.
    """

    LENGTH = "Length"
    PROJECTION = "Projection"


class CoordinateDefinition(str, Enum):
    """Position measurement type for curve moment following SAF specification.

    Specifies whether positions are in meters or percentage.
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class Origin(str, Enum):
    """Origin reference for curve moment positions following SAF specification.

    Specifies whether positions are measured from start or end.
    """

    FROM_START = "From start"
    FROM_END = "From end"


class Extent(str, Enum):
    """Extent of curve moment for multi-span members following SAF specification.

    Specifies whether moment applies to full member or span.
    """

    FULL = "Full"
    SPAN = "Span"


@dataclass(frozen=True)
class StructuralCurveMoment:
    """Structural curve moment (distributed line moment) following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralcurvemoment.html.

    A curve moment represents a distributed line moment applied to a 1D member or 2D member
    edge. The moment can be constant (uniform) or varying linearly (trapezoidal) along the
    load application region.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "LMS1").
    force_action : ForceAction
        Target type: On beam, On edge, On subregion edge, On opening edge, On rib, On internal edge.
    distribution : Distribution
        Moment distribution: Uniform or Trapez (linearly varying).
    direction : MomentDirection
        Moment axis: Mx, My, or Mz.
    load_case : str
        Reference to StructuralLoadCase name.
    coordinate_system : CoordinateSystem
        Global or Local coordinate system.
    location : Location
        Moment application method: Length or Projection.
    coordinate_definition : CoordinateDefinition
        Position measurement: Absolute (meters) or Relative (percentage).
    origin : Origin
        Position reference: From start or From end.
    extent : Extent
        Span coverage: Full or Span.
    start_point : float
        Start position in meters or relative (0.0-1.0).
    end_point : float
        End position in meters or relative (0.0-1.0).
    value_1 : float
        Moment magnitude in kNm/m. Closer to origin for trapezoidal distribution.
    value_2 : float | None, optional
        Second moment magnitude in kNm/m for trapezoidal distribution.
        Further from origin. Required when distribution = TRAPEZ.
    member : str, optional
        Member name (StructuralCurveMember). Required when force_action = ON_BEAM.
    member_rib : str, optional
        Rib name (StructuralCurveMemberRib). Required when force_action = ON_RIB.
    two_d_member : str, optional
        2D member name (StructuralSurfaceMember). Required for edge-based force_action.
    two_d_member_region : str, optional
        Region name (StructuralSurfaceMemberRegion). Required when force_action = ON_SUBREGION_EDGE.
    two_d_member_opening : str, optional
        Opening name (StructuralSurfaceMemberOpening). Required when force_action = ON_OPENING_EDGE.
    edge : int | None, optional
        Edge index starting at 1. Required for edge-based force_action.
    internal_edge : str, optional
        Internal edge name (StructuralCurveEdge). Required when force_action = ON_INTERNAL_EDGE.
    action_type : str, optional
        Load classification (e.g., "Standard", "Wind", "Snow").
    parent_id : str, optional
        UUID for segmented curved geometry tracking.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If distribution = TRAPEZ but value_2 is not specified.
        If force_action = ON_BEAM but member is not specified.
        And other conditional validation errors.

    Examples
    --------
    >>> from blueprints.saf import (
    ...     StructuralCurveMoment,
    ...     MomentDirection,
    ...     ForceAction,
    ...     Distribution,
    ...     CoordinateSystem,
    ...     Location,
    ...     CoordinateDefinition,
    ...     Origin,
    ...     Extent,
    ... )
    >>> # Uniform line moment on beam
    >>> moment = StructuralCurveMoment(
    ...     name="LM1",
    ...     force_action=ForceAction.ON_BEAM,
    ...     distribution=Distribution.UNIFORM,
    ...     direction=MomentDirection.MY,
    ...     load_case="LC1",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.LENGTH,
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     origin=Origin.FROM_START,
    ...     extent=Extent.FULL,
    ...     start_point=0.0,
    ...     end_point=5.0,
    ...     value_1=10.0,
    ...     member="B1",
    ... )

    >>> # Trapezoidal moment on 2D member edge
    >>> trapezoidal = StructuralCurveMoment(
    ...     name="LM2",
    ...     force_action=ForceAction.ON_EDGE,
    ...     distribution=Distribution.TRAPEZ,
    ...     direction=MomentDirection.MZ,
    ...     load_case="LC2",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.LENGTH,
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     origin=Origin.FROM_START,
    ...     extent=Extent.FULL,
    ...     start_point=0.0,
    ...     end_point=4.0,
    ...     value_1=10.0,
    ...     value_2=15.0,
    ...     two_d_member="S1",
    ...     edge=1,
    ... )
    """

    name: str
    force_action: ForceAction
    distribution: Distribution
    direction: MomentDirection
    load_case: str
    coordinate_system: CoordinateSystem
    location: Location
    coordinate_definition: CoordinateDefinition
    origin: Origin
    extent: Extent
    start_point: float
    end_point: float
    value_1: float
    value_2: float | None = None
    member: str = ""
    member_rib: str = ""
    two_d_member: str = ""
    two_d_member_region: str = ""
    two_d_member_opening: str = ""
    edge: int | None = None
    internal_edge: str = ""
    action_type: str = ""
    parent_id: str = ""
    id: str = ""

    _EDGE_BASED_ACTIONS: ClassVar[set[str]] = {
        "On edge",
        "On subregion edge",
        "On opening edge",
        "On internal edge",
    }

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_force_action_requirements()
        self._validate_distribution_requirements()

    def _validate_force_action_requirements(self) -> None:
        """Validate requirements based on force_action type."""
        if self.force_action == ForceAction.ON_BEAM and not self.member:
            raise ValueError("member must be specified when force_action = ForceAction.ON_BEAM")
        if self.force_action == ForceAction.ON_RIB and not self.member_rib:
            raise ValueError("member_rib must be specified when force_action = ForceAction.ON_RIB")
        if self.force_action == ForceAction.ON_EDGE:
            self._validate_edge_requirements("On edge")
        elif self.force_action == ForceAction.ON_SUBREGION_EDGE:
            if not self.two_d_member_region:
                raise ValueError("two_d_member_region must be specified when force_action = ForceAction.ON_SUBREGION_EDGE")
            self._validate_edge_requirements("On subregion edge")
        elif self.force_action == ForceAction.ON_OPENING_EDGE and not self.two_d_member_opening:
            raise ValueError("two_d_member_opening must be specified when force_action = ForceAction.ON_OPENING_EDGE")
        elif self.force_action == ForceAction.ON_OPENING_EDGE and self.two_d_member_opening:
            self._validate_edge_requirements("On opening edge")
        elif self.force_action == ForceAction.ON_INTERNAL_EDGE and not self.internal_edge:
            raise ValueError("internal_edge must be specified when force_action = ForceAction.ON_INTERNAL_EDGE")

    def _validate_edge_requirements(self, action_name: str) -> None:
        """Validate common edge-based action requirements."""
        if not self.two_d_member:
            raise ValueError(f"two_d_member must be specified when force_action = {action_name}")
        if self.edge is None:
            raise ValueError(f"edge must be specified when force_action = {action_name}")

    def _validate_distribution_requirements(self) -> None:
        """Validate requirements based on distribution type."""
        if self.distribution == Distribution.TRAPEZ and self.value_2 is None:
            raise ValueError("value_2 must be specified when distribution = TRAPEZ")
