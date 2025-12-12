"""Structural curve action thermal (thermal line load) definitions following SAF specification.

Thermal actions on beams represent temperature changes applied to 1D members or ribs.
Can be constant or linear with up to 4 temperature components.
"""

from dataclasses import dataclass
from enum import Enum


class ForceAction(str, Enum):
    """Type of thermal curve action application following SAF specification.

    Specifies whether the thermal load is applied to a beam or rib.
    """

    ON_BEAM = "On beam"
    ON_RIB = "On rib"


class Variation(str, Enum):
    """Temperature variation type following SAF specification.

    Specifies whether the temperature is constant or varies linearly.
    """

    CONSTANT = "Constant"
    LINEAR = "Linear"


class CoordinateDefinition(str, Enum):
    """Position measurement type following SAF specification.

    Specifies whether positions are in meters or percentage.
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class Origin(str, Enum):
    """Origin reference for position following SAF specification.

    Specifies whether positions are measured from start or end.
    """

    FROM_START = "From start"
    FROM_END = "From end"


@dataclass(frozen=True)
class StructuralCurveActionThermal:
    """Structural curve action thermal following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralcurveactionthermal.html.

    A thermal curve action represents temperature changes applied to a 1D member (beam) or rib.
    The temperature can be constant across the cross-section or vary linearly with up to 4
    temperature components (left, right, top, bottom).

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "LT1").
    force_action : ForceAction
        Target type: On beam or On rib.
    variation : Variation
        Temperature variation: Constant or Linear.
    load_case : str
        Reference to StructuralLoadCase name.
    coordinate_definition : CoordinateDefinition
        Position measurement: Absolute (meters) or Relative (percentage).
    origin : Origin
        Position reference: From start or From end.
    start_point : float
        Start position in meters or relative (0.0-1.0).
    end_point : float
        End position in meters or relative (0.0-1.0).
    delta_t : float | None, optional
        Temperature change in °C for constant variation.
        Required when variation = CONSTANT.
    temp_l : float | None, optional
        Temperature change on left side in °C for linear variation.
        Required when variation = LINEAR.
    temp_r : float | None, optional
        Temperature change on right side in °C for linear variation.
        Required when variation = LINEAR.
    temp_t : float | None, optional
        Temperature change on top surface in °C for linear variation.
        Required when variation = LINEAR.
    temp_b : float | None, optional
        Temperature change on bottom surface in °C for linear variation.
        Required when variation = LINEAR.
    member : str, optional
        Member name (StructuralCurveMember). Required when force_action = ON_BEAM.
    member_rib : str, optional
        Rib name (StructuralCurveMemberRib). Required when force_action = ON_RIB.
    parent_id : str, optional
        UUID for segmented curved geometry tracking.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If variation = CONSTANT but delta_t is not specified.
        If variation = LINEAR but any of temp_l/temp_r/temp_t/temp_b is not specified.
        If force_action = ON_BEAM but member is not specified.
        If force_action = ON_RIB but member_rib is not specified.

    Examples
    --------
    >>> from blueprints.saf import StructuralCurveActionThermal, ForceAction, Variation, CoordinateDefinition, Origin
    >>> # Constant thermal load on beam
    >>> thermal_const = StructuralCurveActionThermal(
    ...     name="LT1",
    ...     force_action=ForceAction.ON_BEAM,
    ...     variation=Variation.CONSTANT,
    ...     load_case="LC1",
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     origin=Origin.FROM_START,
    ...     start_point=0.0,
    ...     end_point=5.0,
    ...     delta_t=25.0,
    ...     member="B1",
    ... )

    >>> # Linear thermal load on rib with 4 components
    >>> thermal_linear = StructuralCurveActionThermal(
    ...     name="LT2",
    ...     force_action=ForceAction.ON_RIB,
    ...     variation=Variation.LINEAR,
    ...     load_case="LC1",
    ...     coordinate_definition=CoordinateDefinition.ABSOLUTE,
    ...     origin=Origin.FROM_START,
    ...     start_point=0.0,
    ...     end_point=3.5,
    ...     temp_l=20.0,
    ...     temp_r=15.0,
    ...     temp_t=30.0,
    ...     temp_b=10.0,
    ...     member_rib="R1",
    ... )
    """

    name: str
    force_action: ForceAction
    variation: Variation
    load_case: str
    coordinate_definition: CoordinateDefinition
    origin: Origin
    start_point: float
    end_point: float
    delta_t: float | None = None
    temp_l: float | None = None
    temp_r: float | None = None
    temp_t: float | None = None
    temp_b: float | None = None
    member: str = ""
    member_rib: str = ""
    parent_id: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_variation_requirements()
        self._validate_force_action_requirements()

    def _validate_variation_requirements(self) -> None:
        """Validate requirements based on variation type."""
        if self.variation == Variation.CONSTANT and self.delta_t is None:
            raise ValueError("delta_t must be specified when variation = Variation.CONSTANT")
        if self.variation == Variation.LINEAR:
            if self.temp_l is None:
                raise ValueError("temp_l must be specified when variation = Variation.LINEAR")
            if self.temp_r is None:
                raise ValueError("temp_r must be specified when variation = Variation.LINEAR")
            if self.temp_t is None:
                raise ValueError("temp_t must be specified when variation = Variation.LINEAR")
            if self.temp_b is None:
                raise ValueError("temp_b must be specified when variation = Variation.LINEAR")

    def _validate_force_action_requirements(self) -> None:
        """Validate requirements based on force_action type."""
        if self.force_action == ForceAction.ON_BEAM and not self.member:
            raise ValueError("member must be specified when force_action = ForceAction.ON_BEAM")
        if self.force_action == ForceAction.ON_RIB and not self.member_rib:
            raise ValueError("member_rib must be specified when force_action = ForceAction.ON_RIB")
