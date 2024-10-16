"""Module containing definitions of soil types and soil materials."""

from dataclasses import dataclass
from enum import Enum


class SoilMainTypes(Enum):
    """Soil types based on grain size, representing the main portion of the soil mix."""

    GRAVEL = "Gravel"
    SAND = "Sand"
    SILT = "Silt"
    LOAM = "Loam"
    CLAY = "Clay"
    PEAT = "Peat"


class SoilMinorCompositions(Enum):
    """Soil minor compositions, representing the minor portion of the soil mix."""

    CLEAN = "Clean"

    SLITGHTLY_SILTY = "Slightly silty"
    VERY_SILTY = "Very silty"

    SLIGHTLY_CLAYEY = "Slightly clayey"
    VERY_CLAYEY = "Very clayey"

    SLIGHTLY_SANDY = "Slightly sandy"
    VERY_SANDY = "Very sandy"

    ORGANIC = "Organic"


class SoilConsolidationStates(Enum):
    """Consolidation states of the soil."""

    UNCONSOLIDATED = "Unconsolidated"
    NORMALLY_CONSOLIDATED = "Normally consolidated"
    SLIGHTLY_OVERCONSOLIDATED = "Slightly consolidated"
    MODERATELY_OVERCONSOLIDATED = "Moderately overconsolidated"
    HIGHLY_OVERCONSOLIDATED = "Highly consolidated"


class SoilConsistencies(Enum):
    """Consistencies of the soil."""

    # Clay-like consistencies
    VERY_SOFT = "Very soft"
    SOFT = "Soft"
    MEDIUM_STIFF = "Medium stiff"
    STIFF = "Stiff"
    HARD = "Hard"

    # Sand-like consistencies
    VERY_LOOSE = "Very loose"
    LOOSE = "Loose"
    MEDIUM_DENSE = "Medium dense"
    DENSE = "Dense"
    VERY_DENSE = "Very dense"


@dataclass
class SoilType:
    """Class representing a soil type.

    Parameters
    ----------
    main_type : SoilMainTypes
        The soil type of the main portion of the soil mix.
    minor_composition : SoilMinorCompositions, optional
        The composition of the minor portion of the soil mix, by default None.
    consolidation_state : SoilConsolidationStates, optional
        The consolidation state of the soil, by default None.
    consistency : SoilConsistencies, optional
        The consistency of the soil, by default None.
    description : str, optional
        The custom description of the soil, by default None.
    """

    main_type: SoilMainTypes
    minor_composition: SoilMinorCompositions | None = None
    consolidation_state: SoilConsolidationStates | None = None
    consistency: SoilConsistencies | None = None
    description: str | None = None

    @property
    def default_description(self) -> str:
        """The default description of the soil type based on the `main_type`, `minor_composition`, `consolidation_state`, and `consistency`."""
        default_description = self.main_type.value

        for prop in [self.minor_composition, self.consolidation_state, self.consistency]:
            if prop is not None:
                assert isinstance(prop, Enum)
                default_description += ", " + prop.value
        return default_description
