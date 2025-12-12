"""Structural point moment definitions following SAF specification.

Point moments represent concentrated moment loads applied to nodes or 1D members
at specific positions with defined directions and coordinate systems.
"""

from dataclasses import dataclass
from enum import Enum


class MomentDirection(str, Enum):
    """Direction of point moment following SAF specification.

    Specifies the axis of the moment.
    """

    MX = "Mx"
    MY = "My"
    MZ = "Mz"


class ForceAction(str, Enum):
    """Type of point moment application following SAF specification.

    Specifies whether the moment is applied at a node or on a 1D member.
    """

    IN_NODE = "In node"
    ON_BEAM = "On beam"


class CoordinateSystem(str, Enum):
    """Coordinate system for point moment following SAF specification.

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
class StructuralPointMoment:
    """Structural point moment following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralpointmoment.html.

    A point moment represents a concentrated moment applied at a specific location
    in a structure, either at a node or on a 1D member. The moment direction is
    defined by the moment axis (Mx, My, or Mz).

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "PF3").
    direction : MomentDirection
        Moment axis: Mx, My, or Mz.
    force_action : ForceAction
        Application type: In node or On beam.
    value : float
        Moment magnitude in kNm.
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
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If force_action = IN_NODE but reference_node is empty.
        If force_action = ON_BEAM but reference_member is empty.
        If force_action = ON_BEAM but origin is not specified.
        If force_action = ON_BEAM but coordinate_definition is not specified.
        If force_action = ON_BEAM but position is not specified.

    Examples
    --------
    >>> from blueprints.saf import StructuralPointMoment, MomentDirection, ForceAction, CoordinateSystem
    >>> # Moment at node
    >>> moment_at_node = StructuralPointMoment(
    ...     name="M1",
    ...     direction=MomentDirection.MZ,
    ...     force_action=ForceAction.IN_NODE,
    ...     value=15.0,
    ...     load_case="LC1",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     reference_node="N1",
    ... )

    >>> # Moment on beam
    >>> moment_on_beam = StructuralPointMoment(
    ...     name="M2",
    ...     direction=MomentDirection.MY,
    ...     force_action=ForceAction.ON_BEAM,
    ...     value=20.0,
    ...     load_case="LC2",
    ...     coordinate_system=CoordinateSystem.LOCAL,
    ...     reference_member="B1",
    ...     origin=Origin.FROM_START,
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     position=2.5,
    ... )
    """

    name: str
    direction: MomentDirection
    force_action: ForceAction
    value: float
    load_case: str
    coordinate_system: CoordinateSystem
    reference_node: str = ""
    reference_member: str = ""
    action_type: str = ""
    origin: Origin | None = None
    coordinate_definition: CoordinateDefinition | None = None
    position: float | None = None
    id: str = ""

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_force_action_requirements()

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
