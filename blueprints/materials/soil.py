"""Soil material module."""

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


class SoilType:
    """Class representing a soil type."""

    def __init__(
        self,
        main_type: SoilMainTypes,
        minor_composition: SoilMinorCompositions | None = None,
        consolidation_state: SoilConsolidationStates | None = None,
        consistency: SoilConsistencies | None = None,
        description: str | None = None,
    ) -> None:
        """Initializes the soil type."""
        self.main_type = main_type
        self.minor_composition = minor_composition
        self.consolidation_state = consolidation_state
        self.consistency = consistency
        self.description = description

    @property
    def main_type(self) -> SoilMainTypes:
        """The soil type of the main portion of the soil mix."""
        return self._main_type

    @main_type.setter
    def main_type(self, main_type: SoilMainTypes) -> None:
        if not isinstance(main_type, SoilMainTypes):
            raise TypeError(f"Expected `main_type` to be of type {SoilMainTypes.__name__}, but got {type(main_type)}")

        self._main_type = main_type

    @property
    def minor_composition(self) -> SoilMinorCompositions | None:
        """The composition of the minor portion of the soil mix."""
        return self._minor_composition

    @minor_composition.setter
    def minor_composition(self, minor_composition: SoilMinorCompositions | None) -> None:
        if minor_composition is not None and not isinstance(minor_composition, SoilMinorCompositions):
            raise TypeError(f"Expected `minor_composition` to be None or of type {SoilMinorCompositions.__name__}, but got {type(minor_composition)}")

        self._minor_composition = minor_composition

    @property
    def consolidation_state(self) -> SoilConsolidationStates | None:
        """The consolidation state of the soil."""
        return self._consolidation_state

    @consolidation_state.setter
    def consolidation_state(self, consolidation_state: SoilConsolidationStates | None) -> None:
        if consolidation_state is not None and not isinstance(consolidation_state, SoilConsolidationStates):
            raise TypeError(
                f"Expected `consolidation_state` to be None or of type {SoilConsolidationStates.__name__}, but got {type(consolidation_state)}"
            )

        self._consolidation_state = consolidation_state

    @property
    def consistency(self) -> SoilConsistencies | None:
        """The consistency of the soil."""
        return self._consistency

    @consistency.setter
    def consistency(self, consistency: SoilConsistencies | None) -> None:
        if consistency is not None and not isinstance(consistency, SoilConsistencies):
            raise TypeError(f"Expected `consistency` to be None or of type {SoilConsistencies.__name__}, but got {type(consistency)}")

        self._consistency = consistency

    @property
    def description(self) -> str | None:
        """The custom description of the soil."""
        return self._description

    @description.setter
    def description(self, description: str | None) -> None:
        if description is not None and not isinstance(description, str):
            raise TypeError(f"Expected `description` to be None or of type {str.__name__}, but got {type(description)}")

        self._description = description

    @property
    def default_description(self) -> str:
        """The default description of the soil type based on the `main_type`, `minor_composition`, `consolidation_state`, and `consistency`."""
        s = self.main_type.value

        for prop in [self.minor_composition, self.consolidation_state, self.consistency]:
            if prop is not None:
                s += ", " + prop.value
        return s
