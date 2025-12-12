"""Structural load case definitions following SAF specification.

Load cases group individual loads from the same action source.
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class ActionType(str, Enum):
    """Enumeration for load case action type.

    Defines the category of action in a load case following SAF specification.
    """

    PERMANENT = "Permanent"
    VARIABLE = "Variable"
    ACCIDENTAL = "Accidental"


@dataclass(frozen=True)
class StructuralLoadCase:
    """Structural load case following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralloadcase.html.

    A load case groups individual loads from the same action source. It must
    reference a valid StructuralLoadGroup object with compatible settings.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "LC1").
    action_type : ActionType
        Category of action. One of: Permanent, Variable, or Accidental.
    load_group : str
        Reference to StructuralLoadGroup name with compatible settings.
    load_type : str
        Subtype of load. Valid values depend on action_type:
        - Permanent: "Self weight", "Others", "Prestress", "Standard"
        - Variable: "Others", "Dynamic", "Static", "Temperature", "Wind",
          "Snow", "Maintenance", "Fire", "Moving", "Seismic", "Standard"
        - Accidental: "Others", "Dynamic", "Static", "Temperature", "Wind",
          "Snow", "Maintenance", "Fire", "Moving", "Seismic", "Standard"
    duration : str, optional
        Duration classification. Required when action_type = VARIABLE.
        Valid values: "Long", "Medium", "Short", "Instantaneous".
    description : str, optional
        Additional context (e.g., "Offices – Cat.B").
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If action_type = VARIABLE but duration is not specified.
        If load_type is not valid for the specified action_type.
        If duration is specified with an invalid value.

    Examples
    --------
    >>> from blueprints.saf import StructuralLoadCase, ActionType
    >>> lc_permanent = StructuralLoadCase(name="LC1", action_type=ActionType.PERMANENT, load_group="LG1", load_type="Standard")

    >>> lc_variable = StructuralLoadCase(name="LC2", action_type=ActionType.VARIABLE, load_group="LG2", load_type="Snow", duration="Short")
    """

    name: str
    action_type: ActionType
    load_group: str
    load_type: str
    duration: str = ""
    description: str = ""
    id: str = ""

    # Valid load types for each action type
    _LOAD_TYPES_PERMANENT: ClassVar[set[str]] = {
        "Self weight",
        "Others",
        "Prestress",
        "Standard",
    }
    _LOAD_TYPES_VARIABLE: ClassVar[set[str]] = {
        "Others",
        "Dynamic",
        "Static",
        "Temperature",
        "Wind",
        "Snow",
        "Maintenance",
        "Fire",
        "Moving",
        "Seismic",
        "Standard",
    }
    _LOAD_TYPES_ACCIDENTAL: ClassVar[set[str]] = {
        "Others",
        "Dynamic",
        "Static",
        "Temperature",
        "Wind",
        "Snow",
        "Maintenance",
        "Fire",
        "Moving",
        "Seismic",
        "Standard",
    }
    _VALID_DURATIONS: ClassVar[set[str]] = {
        "Long",
        "Medium",
        "Short",
        "Instantaneous",
    }

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        # Validate duration requirement for Variable
        if self.action_type == ActionType.VARIABLE and not self.duration:
            raise ValueError("duration must be specified when action_type = ActionType.VARIABLE")

        # Validate load_type based on action_type
        if self.action_type == ActionType.PERMANENT:
            valid_types = self._LOAD_TYPES_PERMANENT
        elif self.action_type == ActionType.VARIABLE:
            valid_types = self._LOAD_TYPES_VARIABLE
        else:  # ACCIDENTAL
            valid_types = self._LOAD_TYPES_ACCIDENTAL

        if self.load_type not in valid_types:
            raise ValueError(
                f"load_type '{self.load_type}' is not valid for "
                f"action_type = {self.action_type.value}. "
                f"Valid values: {', '.join(sorted(valid_types))}"
            )

        # Validate duration value if specified
        if self.duration and self.duration not in self._VALID_DURATIONS:
            raise ValueError(f"duration '{self.duration}' is not valid. Valid values: {', '.join(sorted(self._VALID_DURATIONS))}")
