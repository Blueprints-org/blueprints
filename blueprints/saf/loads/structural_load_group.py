"""Structural load group definitions following SAF specification.

Load groups organize how load cases are combined in structural analysis.
"""

from dataclasses import dataclass
from enum import Enum


class LoadGroupType(str, Enum):
    """Enumeration for load group type.

    Defines the category of load group following SAF specification.
    """

    PERMANENT = "Permanent"
    VARIABLE = "Variable"
    ACCIDENTAL = "Accidental"
    SEISMIC = "Seismic"
    MOVING = "Moving"
    TENSIONING = "Tensioning"
    FIRE = "Fire"


class Relation(str, Enum):
    """Enumeration for load group relation type.

    Controls how load cases in the group are combined in load combinations.
    """

    EXCLUSIVE = "Exclusive"
    STANDARD = "Standard"
    TOGETHER = "Together"


@dataclass(frozen=True)
class StructuralLoadGroup:
    """Structural load group following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralloadgroup.html.

    Load groups organize and control how load cases are combined together in
    structural analysis. They enable designation of which load cases must, must not,
    or can act together.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "LG1").
    load_group_type : LoadGroupType
        Category of load group. One of: Permanent, Variable, Accidental, Seismic,
        Moving, Tensioning, Fire.
    relation : Relation
        Controls combination behavior. One of: Exclusive, Standard, Together.
        - Exclusive: Load cases from the group never appear together
        - Standard: Sorts load cases without affecting combination generation
        - Together: All load cases always appear in every combination (Permanent only)
    load_type : str, optional
        Load type classification. Required when load_group_type = VARIABLE.
        Valid values: Domestic, Offices, Congregation, Shopping, Storage,
        Vehicle <30kN, Vehicle >30kN, Roofs, Snow, Wind, Temperature.
    id : str, optional
        Unique identifier (UUID format).

    Raises
    ------
    ValueError
        If load_group_type = VARIABLE but load_type is not specified.
        If relation = TOGETHER but load_group_type != PERMANENT.
        If relation = EXCLUSIVE but load_group_type = PERMANENT.
        If load_type is not a valid SAF load type value.

    Examples
    --------
    >>> lg_permanent = StructuralLoadGroup(name="LG1", load_group_type=LoadGroupType.PERMANENT, relation=Relation.STANDARD)

    >>> lg_variable = StructuralLoadGroup(name="LG2", load_group_type=LoadGroupType.VARIABLE, relation=Relation.EXCLUSIVE, load_type="Snow")
    """

    name: str
    load_group_type: LoadGroupType
    relation: Relation
    load_type: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        # Validate load_type requirement for Variable
        if self.load_group_type == LoadGroupType.VARIABLE and not self.load_type:
            raise ValueError("load_type must be specified when load_group_type = LoadGroupType.VARIABLE")

        # Validate Together relation only for Permanent
        if self.relation == Relation.TOGETHER and self.load_group_type != LoadGroupType.PERMANENT:
            raise ValueError("relation = Relation.TOGETHER only valid for load_group_type = LoadGroupType.PERMANENT")

        # Validate Exclusive relation not for Permanent
        if self.relation == Relation.EXCLUSIVE and self.load_group_type == LoadGroupType.PERMANENT:
            raise ValueError("relation = Relation.EXCLUSIVE not valid for load_group_type = LoadGroupType.PERMANENT")

        # Validate load_type is from valid values if specified
        if self.load_type:
            valid_load_types = {
                "Domestic",
                "Offices",
                "Congregation",
                "Shopping",
                "Storage",
                "Vehicle <30kN",
                "Vehicle >30kN",
                "Roofs",
                "Snow",
                "Wind",
                "Temperature",
            }
            if self.load_type not in valid_load_types:
                raise ValueError(f"load_type '{self.load_type}' is not a valid SAF load type. Valid values: {', '.join(sorted(valid_load_types))}")
