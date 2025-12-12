"""Structural curve action (distributed line load) definitions following SAF specification.

Curve actions represent distributed line forces applied to 1D members or 2D member edges.
Can be constant or trapezoidal, acting in X, Y, Z directions or as vectors.
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class Direction(str, Enum):
    """Direction of curve action following SAF specification.

    Specifies whether the action is a single-axis load or a vector.
    """

    X = "X"
    Y = "Y"
    Z = "Z"
    VECTOR = "Vector"


class ForceAction(str, Enum):
    """Type of curve action application following SAF specification.

    Specifies where the load is applied.
    """

    ON_BEAM = "On beam"
    ON_EDGE = "On edge"
    ON_SUBREGION_EDGE = "On subregion edge"
    ON_OPENING_EDGE = "On opening edge"
    ON_RIB = "On rib"
    ON_INTERNAL_EDGE = "On internal edge"


class Distribution(str, Enum):
    """Distribution type of curve action following SAF specification.

    Specifies how the load varies along the member.
    """

    UNIFORM = "Uniform"
    TRAPEZ = "Trapez"


class CoordinateSystem(str, Enum):
    """Coordinate system for curve action following SAF specification.

    Global or local coordinate system reference.
    """

    GLOBAL = "Global"
    LOCAL = "Local"


class Location(str, Enum):
    """Location type for curve action application following SAF specification.

    Specifies whether load is applied based on length or projection.
    """

    LENGTH = "Length"
    PROJECTION = "Projection"


class CoordinateDefinition(str, Enum):
    """Position measurement type for curve action following SAF specification.

    Specifies whether positions are in meters or percentage.
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class Origin(str, Enum):
    """Origin reference for curve action positions following SAF specification.

    Specifies whether positions are measured from start or end.
    """

    FROM_START = "From start"
    FROM_END = "From end"


class Extent(str, Enum):
    """Extent of curve action for multi-span members following SAF specification.

    Specifies whether load applies to full member or span.
    """

    FULL = "Full"
    SPAN = "Span"


@dataclass(frozen=True)
class StructuralCurveAction:
    """Structural curve action (distributed line load) following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralcurveaction.html.

    A curve action represents a distributed line force applied to a 1D member or 2D member
    edge. The load can be constant (uniform) or varying linearly (trapezoidal) along the
    load application region.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "F3").
    force_action : ForceAction
        Target type: On beam, On edge, On subregion edge, On opening edge, On rib, On internal edge.
    distribution : Distribution
        Load distribution: Uniform or Trapez (linearly varying).
    direction : Direction
        Load direction: X, Y, Z, or Vector.
    load_case : str
        Reference to StructuralLoadCase name.
    coordinate_system : CoordinateSystem
        Global or Local coordinate system.
    location : Location
        Load application method: Length or Projection.
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
    value_1 : float | None
        Load magnitude for single-axis directions (X/Y/Z) in kN/m.
        For Vector direction: use vector_1 instead.
        Closer to origin for trapezoidal distribution.
    value_2 : float | None, optional
        Second load magnitude for trapezoidal distribution (X/Y/Z) in kN/m.
        Further from origin. Required when distribution = TRAPEZ and direction != VECTOR.
    vector_1 : str | None, optional
        Load vector for Vector direction in "X;Y;Z" format (kN/m).
        Closer to origin for trapezoidal distribution.
    vector_2 : str | None, optional
        Second load vector for trapezoidal distribution in "X;Y;Z" format (kN/m).
        Further from origin. Required when distribution = TRAPEZ and direction = VECTOR.
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
    eccentricity_ey : float, optional
        Y-direction offset in mm. Default: 0.
    eccentricity_ez : float, optional
        Z-direction offset in mm. Default: 0.
    action_type : str, optional
        Load classification (e.g., "Standard", "Wind", "Snow").
    parent_id : str, optional
        UUID for segmented curved geometry tracking.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If direction = Vector but vector_1 is not specified.
        If direction = X/Y/Z but value_1 is not specified.
        If distribution = TRAPEZ but value_2/vector_2 is not specified.
        If force_action = ON_BEAM but member is not specified.
        And other conditional validation errors.

    Examples
    --------
    >>> from blueprints.saf import (
    ...     StructuralCurveAction,
    ...     Direction,
    ...     ForceAction,
    ...     Distribution,
    ...     CoordinateSystem,
    ...     Location,
    ...     CoordinateDefinition,
    ...     Origin,
    ...     Extent,
    ... )
    >>> # Uniform line load on beam
    >>> load = StructuralCurveAction(
    ...     name="F1",
    ...     force_action=ForceAction.ON_BEAM,
    ...     distribution=Distribution.UNIFORM,
    ...     direction=Direction.Z,
    ...     load_case="LC1",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.LENGTH,
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     origin=Origin.FROM_START,
    ...     extent=Extent.FULL,
    ...     start_point=0.0,
    ...     end_point=5.0,
    ...     value_1=-50.0,
    ... )

    >>> # Trapezoidal load on 2D member edge
    >>> trapezoidal = StructuralCurveAction(
    ...     name="F2",
    ...     force_action=ForceAction.ON_EDGE,
    ...     distribution=Distribution.TRAPEZ,
    ...     direction=Direction.X,
    ...     load_case="LC2",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.LENGTH,
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     origin=Origin.FROM_START,
    ...     extent=Extent.FULL,
    ...     start_point=0.0,
    ...     end_point=4.0,
    ...     value_1=-100.0,
    ...     value_2=-150.0,
    ...     two_d_member="S1",
    ...     edge=1,
    ... )
    """

    name: str
    force_action: ForceAction
    distribution: Distribution
    direction: Direction
    load_case: str
    coordinate_system: CoordinateSystem
    location: Location
    coordinate_definition: CoordinateDefinition
    origin: Origin
    extent: Extent
    start_point: float
    end_point: float
    value_1: float | None = None
    value_2: float | None = None
    vector_1: str | None = None
    vector_2: str | None = None
    member: str = ""
    member_rib: str = ""
    two_d_member: str = ""
    two_d_member_region: str = ""
    two_d_member_opening: str = ""
    edge: int | None = None
    internal_edge: str = ""
    eccentricity_ey: float = 0.0
    eccentricity_ez: float = 0.0
    action_type: str = ""
    parent_id: str = ""
    id: str = ""

    _SINGLE_AXIS_DIRECTIONS: ClassVar[set[str]] = {"X", "Y", "Z"}
    _VECTOR_PATTERN: ClassVar[str] = ";"
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
        self._validate_direction_value_format()
        self._validate_force_action_requirements()
        self._validate_distribution_requirements()

    def _validate_direction_value_format(self) -> None:
        """Validate that direction and value/vector format are consistent."""
        if self.direction == Direction.VECTOR:
            if self.vector_1 is None:
                raise ValueError("vector_1 must be specified when direction = Direction.VECTOR")
            if self._VECTOR_PATTERN not in self.vector_1:
                raise ValueError(f"vector_1 must be in 'X;Y;Z' format for Vector direction, got '{self.vector_1}'")
        elif self.direction.value in self._SINGLE_AXIS_DIRECTIONS:
            if self.value_1 is None:
                raise ValueError(f"value_1 must be specified when direction = {self.direction.value}")

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
        if self.distribution == Distribution.TRAPEZ:
            if self.direction == Direction.VECTOR:
                if self.vector_2 is None:
                    raise ValueError("vector_2 must be specified when distribution = TRAPEZ and direction = VECTOR")
            elif self.value_2 is None:
                raise ValueError("value_2 must be specified when distribution = TRAPEZ and direction != VECTOR")
