"""Structural load combination definitions following SAF specification.

Load combinations group individual load cases with associated factors and multipliers
for structural analysis under different limit states and design standards.
"""

from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class Category(str, Enum):
    """Load combination category following SAF specification.

    Defines the limit state or design standard category of a load combination.
    """

    ULS = "ULS"
    SLS = "SLS"
    ALS = "ALS"
    ACCORDING_NATIONAL_STANDARD = "According national standard"
    NOT_DEFINED = "Not defined"


class CombinationType(str, Enum):
    """Load combination type following SAF specification.

    Defines how load cases are combined for analysis.
    """

    ENVELOPE = "Envelope"
    LINEAR = "Linear"
    NONLINEAR = "Nonlinear"


class NationalStandard(str, Enum):
    """National standard types for load combinations following SAF specification.

    Specifies which design standard is used when category = ACCORDING_NATIONAL_STANDARD.
    """

    EN_ULS_STR_GEO_SET_B = "EN-ULS (STR/GEO) Set B"
    EN_ULS_STR_GEO_SET_C = "EN-ULS (STR/GEO) Set C"
    EN_ACCIDENTAL_1 = "EN-Accidental 1"
    EN_ACCIDENTAL_2 = "EN-Accidental 2"
    EN_SEISMIC = "EN-Seismic"
    EN_SLS_CHARACTERISTIC = "EN-SLS Characteristic"
    EN_SLS_FREQUENT = "EN-SLS Frequent"
    EN_SLS_QUASI_PERMANENT = "EN-SLS Quasi-permanent"
    IBC_LRFD_ULTIMATE = "IBC-LRFD ultimate"
    IBC_ASD_ULTIMATE = "IBC-ASD ultimate"
    IBC_ASD_SERVICEABILITY = "IBC-ASD serviceability"
    IBC_ASD_SEISMIC = "IBC-ASD seismic"
    IBC_LRFD_SEISMIC = "IBC-LRFD seismic"


class LoadCaseItem(NamedTuple):
    """Individual load case reference within a load combination.

    Attributes
    ----------
    load_case_name : str
        Reference to StructuralLoadCase name.
    load_factor : float
        Load factor for this case (default: 1.0).
    multiplier : float
        Multiplier for this case (default: 1.0).
    """

    load_case_name: str
    load_factor: float = 1.0
    multiplier: float = 1.0


@dataclass(frozen=True)
class StructuralLoadCombination:
    """Structural load combination following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralloadcombination.html.

    A load combination defines how multiple load cases are combined for analysis.
    Each combination references load cases with associated factors and multipliers.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "COM1").
    category : Category
        Combination category. One of: ULS, SLS, ALS, According national standard, Not defined.
    load_cases : tuple[LoadCaseItem, ...]
        Load case references with factors and multipliers. Must contain at least one item.
    national_standard : NationalStandard, optional
        National standard type. Required when category = ACCORDING_NATIONAL_STANDARD.
    combination_type : CombinationType, optional
        Type of combination: Envelope, Linear, or Nonlinear.
    description : str, optional
        Additional context describing the combination.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If load_cases is empty.
        If any load_case_name is empty string.
        If category = ACCORDING_NATIONAL_STANDARD but national_standard is not specified.
        If national_standard is specified but category != ACCORDING_NATIONAL_STANDARD.

    Examples
    --------
    >>> from blueprints.saf import StructuralLoadCombination, Category, LoadCaseItem
    >>> load_cases = (
    ...     LoadCaseItem(load_case_name="LC1", load_factor=1.35, multiplier=1.0),
    ...     LoadCaseItem(load_case_name="LC2", load_factor=1.5, multiplier=1.0),
    ... )
    >>> combo = StructuralLoadCombination(
    ...     name="COM1",
    ...     category=Category.ULS,
    ...     load_cases=load_cases,
    ... )

    >>> # With national standard
    >>> from blueprints.saf import NationalStandard
    >>> combo_nat = StructuralLoadCombination(
    ...     name="COM2",
    ...     category=Category.ACCORDING_NATIONAL_STANDARD,
    ...     load_cases=load_cases,
    ...     national_standard=NationalStandard.EN_ULS_STR_GEO_SET_B,
    ... )
    """

    name: str
    category: Category
    load_cases: tuple[LoadCaseItem, ...]
    national_standard: NationalStandard | None = None
    combination_type: CombinationType | None = None
    description: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        # Validate at least one load case
        if not self.load_cases:
            raise ValueError("load_cases must contain at least one LoadCaseItem")

        # Validate all load case names are non-empty
        for i, item in enumerate(self.load_cases):
            if not item.load_case_name:
                raise ValueError(f"load_case_name at index {i} cannot be empty")

        # Validate national_standard requirement
        if self.category == Category.ACCORDING_NATIONAL_STANDARD:
            if self.national_standard is None:
                raise ValueError("national_standard must be specified when category = Category.ACCORDING_NATIONAL_STANDARD")
        elif self.national_standard is not None:
            # Error if national_standard specified for other categories
            raise ValueError("national_standard should only be specified when category = Category.ACCORDING_NATIONAL_STANDARD")
