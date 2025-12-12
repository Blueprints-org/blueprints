"""Structural point action (point load) definitions following SAF specification.

Point actions represent concentrated forces applied to nodes or 1D members
at specific positions with defined directions and coordinate systems.
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class Direction(str, Enum):
    """Direction of point action following SAF specification.

    Specifies whether the action is applied in a single axis direction or as a vector.
    """

    X = "X"
    Y = "Y"
    Z = "Z"
    VECTOR = "Vector"


class ForceAction(str, Enum):
    """Type of point action application following SAF specification.

    Specifies whether the action is applied at a node or on a 1D member.
    """

    IN_NODE = "In node"
    ON_BEAM = "On beam"


class CoordinateSystem(str, Enum):
    """Coordinate system for point action following SAF specification.

    Global or local coordinate system reference.
    """

    GLOBAL = "Global"
    LOCAL = "Local"


class Origin(str, Enum):
    """Origin reference for position on member following SAF specification.

    Applies only when force_action = ON_BEAM.
    """

    FROM_START = "From start"
    FROM_END = "From end"


class CoordinateDefinition(str, Enum):
    """Position measurement type on member following SAF specification.

    Applies only when force_action = ON_BEAM.
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


@dataclass(frozen=True)
class StructuralPointAction:
    """Structural point action (concentrated load) following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralpointaction.html.

    A point action represents a concentrated force applied at a specific location
    in a structure, either at a node or on a 1D member. The force direction can be
    single-axis (X, Y, Z) or vector-based (X;Y;Z components).

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "F3").
    direction : Direction
        Load direction: X, Y, Z, or Vector.
    force_action : ForceAction
        Application type: In node or On beam.
    value : str
        Load value or vector. For X/Y/Z directions: numeric value in kN.
        For Vector direction: "X;Y;Z" format in kN (e.g., "10;10;0").
    load_case : str
        Reference to StructuralLoadCase name.
    coordinate_system : CoordinateSystem
        Global or Local coordinate system.
    reference_node : str, optional
        Node name reference. Required when force_action = IN_NODE.
    reference_member : str, optional
        Member name reference. Required when force_action = ON_BEAM.
    action_type : str, optional
        Load classification (e.g., "Standard", "Wind", "Snow", "Self weight").
    origin : Origin, optional
        "From start" or "From end". Required when force_action = ON_BEAM.
    coordinate_definition : CoordinateDefinition, optional
        Absolute or Relative. Required when force_action = ON_BEAM.
    position : float, optional
        Position on member in meters (or percentage if Relative). Required when force_action = ON_BEAM.
    repeat : int, optional
        Number of repeated loads (default: 1). Use 0 for single load.
    delta : float, optional
        Spacing between repeated loads in meters.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If direction = Vector but value is not in "X;Y;Z" format.
        If direction = X/Y/Z but value is in "X;Y;Z" format.
        If force_action = IN_NODE but reference_node is empty.
        If force_action = ON_BEAM but reference_member is empty.
        If force_action = ON_BEAM but origin is not specified.
        If force_action = ON_BEAM but coordinate_definition is not specified.
        If force_action = ON_BEAM but position is not specified.
        If repeat < 0 (negative repeat count).

    Examples
    --------
    >>> from blueprints.saf import StructuralPointAction, Direction, ForceAction, CoordinateSystem
    >>> # Point load at node
    >>> load_at_node = StructuralPointAction(
    ...     name="F1",
    ...     direction=Direction.Z,
    ...     force_action=ForceAction.IN_NODE,
    ...     value="-50",
    ...     load_case="LC1",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     reference_node="N1",
    ... )

    >>> # Vector load on beam
    >>> load_on_beam = StructuralPointAction(
    ...     name="F2",
    ...     direction=Direction.VECTOR,
    ...     force_action=ForceAction.ON_BEAM,
    ...     value="10;10;0",
    ...     load_case="LC2",
    ...     coordinate_system=CoordinateSystem.LOCAL,
    ...     reference_member="M1",
    ...     origin=Origin.FROM_START,
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     position=2.5,
    ... )
    """

    name: str
    direction: Direction
    force_action: ForceAction
    value: str
    load_case: str
    coordinate_system: CoordinateSystem
    reference_node: str = ""
    reference_member: str = ""
    action_type: str = ""
    origin: Origin | None = None
    coordinate_definition: CoordinateDefinition | None = None
    position: float | None = None
    repeat: int = 1
    delta: float | None = None
    id: str = ""

    _SINGLE_AXIS_DIRECTIONS: ClassVar[set[str]] = {"X", "Y", "Z"}
    _VECTOR_PATTERN: ClassVar[str] = ";"

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_direction_value_format()
        self._validate_force_action_requirements()
        self._validate_repeat_and_delta()

    def _validate_direction_value_format(self) -> None:
        """Validate that direction and value format are consistent."""
        if self.direction == Direction.VECTOR:
            if self._VECTOR_PATTERN not in self.value:
                raise ValueError(f"value must be in 'X;Y;Z' format for Vector direction, got '{self.value}'")
        elif self.direction.value in self._SINGLE_AXIS_DIRECTIONS and self._VECTOR_PATTERN in self.value:
            raise ValueError(f"value must be a single numeric value for {self.direction.value} direction, not vector format")

    def _validate_force_action_requirements(self) -> None:
        """Validate requirements based on force_action type."""
        if self.force_action == ForceAction.IN_NODE:
            if not self.reference_node:
                raise ValueError("reference_node must be specified when force_action = ForceAction.IN_NODE")
        elif self.force_action == ForceAction.ON_BEAM:
            self._validate_on_beam_requirements()

    def _validate_on_beam_requirements(self) -> None:
        """Validate all ON_BEAM specific requirements."""
        if not self.reference_member:
            raise ValueError("reference_member must be specified when force_action = ForceAction.ON_BEAM")
        if self.origin is None:
            raise ValueError("origin must be specified when force_action = ForceAction.ON_BEAM")
        if self.coordinate_definition is None:
            raise ValueError("coordinate_definition must be specified when force_action = ForceAction.ON_BEAM")
        if self.position is None:
            raise ValueError("position must be specified when force_action = ForceAction.ON_BEAM")

    def _validate_repeat_and_delta(self) -> None:
        """Validate repeat count and delta spacing requirements."""
        if self.repeat < 0:
            raise ValueError(f"repeat must be >= 0, got {self.repeat}")
        if self.repeat > 1 and self.delta is None:
            raise ValueError("delta must be specified when repeat > 1")
