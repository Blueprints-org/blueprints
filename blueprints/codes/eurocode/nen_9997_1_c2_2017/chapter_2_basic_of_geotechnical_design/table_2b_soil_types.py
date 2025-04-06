from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from functools import cache, cached_property
from os import name

from blueprints.materials.soil import (SoilConsistencies,
                                       SoilConsolidationStates, SoilMainTypes,
                                       SoilMinorCompositions, SoilType)


@dataclass
class SoilTypeTable2bOld(SoilType):
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
    dutch_name: str | None = None

@dataclass(frozen=True)
class SoilTypeTable2b:

    main_type: SoilMainTypes
    """The soil type of the main portion of the soil mix."""
    name: str
    """The (English) name of the soil type."""
    dutch_name: str
    """The Dutch name of the soil type."""

    @cached_property
    def as_dict(self) -> dict[str, str]:
        """Returns the soil type as a dictionary."""
        return {
            "name": self.name,
            "dutch_name": self.dutch_name,
            "main_type": self.main_type.value,
        }

class SoilTypesTable2b(Enum):
    # Gravel, slighly silty, loose
    GRAVEL_SL_SILTY_LOOSE = SoilTypeTable2b(
        main_type=SoilMainTypes.GRAVEL,
        name="Gravel, slightly silty, loose",
        dutch_name="Grind, zwak siltig, los",
    )

    # Gravel, slightly silty, medium dense
    GRAVEL_SL_SILTY_MEDIUM_DENSE = SoilTypeTable2b(
        main_type=SoilMainTypes.GRAVEL,
        name="Gravel, slightly silty, medium dense",
        dutch_name="Grind, zwak siltig, matig",
    )

    # Gravel, slightly silty, dense
    GRAVEL_SL_SILTY_DENSE = SoilTypeTable2b(
        main_type=SoilMainTypes.GRAVEL,
        name="Gravel, slightly silty, dense",
        dutch_name="Grind, zwak siltig, vast",
    )

    # Gravel, very silty, loose
    GRAVEL_V_SILTY_LOOSE = SoilTypeTable2b(
        main_type=SoilMainTypes.GRAVEL,
        name="Gravel, very silty, loose",
        dutch_name="Grind, sterk siltig, los",
    )

    # Gravel, very silty, medium dense
    GRAVEL_V_SILTY_MEDIUM_DENSE = SoilTypeTable2b(
        main_type=SoilMainTypes.GRAVEL,
        name="Gravel, very silty, medium dense",
        dutch_name="Grind, sterk siltig, matig",
    )

    # Gravel, very silty, dense
    GRAVEL_V_SILTY_DENSE = SoilTypeTable2b(
        main_type=SoilMainTypes.GRAVEL,
        name="Gravel, very silty, dense",
        dutch_name="Grind, sterk siltig, vast",
    )

    # Sand, clean, loose
    SAND_CLEAN_LOOSE = SoilTypeTable2b(
        main_type=SoilMainTypes.SAND,
        name="Sand, clean, loose",
        dutch_name="Zand, schoon, los",
    )

    # Sand, clean, medium dense
    SAND_CLEAN_MEDIUM_DENSE = SoilTypeTable2b(
        main_type=SoilMainTypes.SAND,
        name="Sand, clean, medium dense",
        dutch_name="Zand, schoon, matig",
    )

    # Sand, clean, dense
    SAND_CLEAN_DENSE = SoilTypeTable2b(
        main_type=SoilMainTypes.SAND,
        name="Sand, clean, dense",
        dutch_name="Zand, schoon, vast",
    )

    # Sand, sligthly silty, clayey
    SAND_SL_SILTY_CLAYEY = SoilTypeTable2b(
        main_type=SoilMainTypes.SAND,
        name="Sand, slightly silty, clayey",
        dutch_name="Zand, zwak siltig, kleiig",
    )

    # Sand, very silty, clayey
    SAND_V_SILTY_CLAYEY = SoilTypeTable2b(
        main_type=SoilMainTypes.SAND,
        name="Sand, very silty, clayey",
        dutch_name="Zand, sterk siltig, kleiig",
    )

    # Loam, slightly sandy, loose
    LOAM_SL_SANDY_SOFT = SoilTypeTable2b(
        main_type=SoilMainTypes.LOAM,
        name="Loam, slightly sandy, loose",
        dutch_name="Leem, zwak zandig, los",
    )

    # Loam, slightly sandy, medium stiff
    LOAM_SL_SANDY_MEDIUM_STIFF = SoilTypeTable2b(
        main_type=SoilMainTypes.LOAM,
        name="Loam, slightly sandy, medium stiff",
        dutch_name="Leem, zwak zandig, matig",
    )

    # Loam, slightly sandy, stiff
    LOAM_SL_SANDY_STIFF = SoilTypeTable2b(
        main_type=SoilMainTypes.LOAM,
        name="Loam, slightly sandy, stiff",
        dutch_name="Leem, zwak zandig, vast",
    )

    # Loam, very sandy
    LOAM_V_SANDY = SoilTypeTable2b(
        main_type=SoilMainTypes.LOAM,
        name="Loam, very sandy",
        dutch_name="Leem, sterk zandig",
    )

    # Clay, clean, soft
    CLAY_CLEAN_SOFT = SoilTypeTable2b(
        main_type=SoilMainTypes.CLAY,
        name="Clay, clean, soft",
        dutch_name="Klei, schoon, slap",
    )

    # Clay, clean, medium stiff
    CLAY_CLEAN_MEDIUM_STIFF = SoilTypeTable2b(
        main_type=SoilMainTypes.CLAY,
        name="Clay, clean, medium stiff",
        dutch_name="Klei, schoon, matig",
    )

    # Clay, clean, stiff
    CLAY_CLEAN_STIFF = SoilTypeTable2b(
        main_type=SoilMainTypes.CLAY,
        name="Clay, clean, stiff",
        dutch_name="Klei, schoon, vast",
    )

    # Clay, slightly sandy, soft
    CLAY_SL_SANDY_SOFT = SoilTypeTable2b(
        main_type=SoilMainTypes.CLAY,
        name="Clay, slightly sandy, soft",
        dutch_name="Klei, zwak zandig, slap",
    )

    # Clay, slightly sandy, medium stiff
    CLAY_SL_SANDY_MEDIUM_STIFF = SoilTypeTable2b(
        main_type=SoilMainTypes.CLAY,
        name="Clay, slightly sandy, medium stiff",
        dutch_name="Klei, zwak zandig, matig",
    )

    # Clay, slightly sandy, stiff
    CLAY_SL_SANDY_STIFF = SoilTypeTable2b(
        main_type=SoilMainTypes.CLAY,
        name="Clay, slightly sandy, stiff",
        dutch_name="Klei, zwak zandig, vast",
    )

    # Clay, very sandy
    CLAY_V_SANDY = SoilTypeTable2b(
        main_type=SoilMainTypes.CLAY,
        name="Clay, very sandy",
        dutch_name="Klei, sterk zandig",
    )

    # Clay, organic, soft
    CLAY_ORGANIC_SOFT = SoilTypeTable2b(
        main_type=SoilMainTypes.CLAY,
        name="Clay, organic, soft",
        dutch_name="Klei, organisch, slap",
    )

    # Clay, organic, medium stiff
    CLAY_ORGANIC_MEDIUM_STIFF = SoilTypeTable2b(
        main_type=SoilMainTypes.CLAY,
        name="Clay, organic, medium stiff",
        dutch_name="Klei, organisch, matig",
    )

    # Peat, normally consolidated
    PEAT_NC = SoilTypeTable2b(
        main_type=SoilMainTypes.PEAT, 
        name="Peat, normally consolidated",
        dutch_name="Veen, niet voorbelast",
    )

    # Peat, overconsolidated
    PEAT_OC = SoilTypeTable2b(
        main_type=SoilMainTypes.PEAT,
        name="Peat, overconsolidated",
        dutch_name="Veen, voorbelast",
    )

    @cached_property
    def _get_name_map(self) -> dict[str, SoilTypesTable2b]:
        """Returns a map of the soil types by their name or Dutch name."""
        return {item.value.name: item for item in SoilTypesTable2b} | {item.value.dutch_name: item for item in SoilTypesTable2b}

    def get_soil_type_by_name(self, name: str) -> SoilTypesTable2b:
        """Get a soil type by its name or Dutch name.
        
        Parameters
        ----------
        name : str
            The name or Dutch name of the soil type.
            
        Returns
        -------
        SoilTypesTable2b
            The soil type.
        
        Raises
        ------
        ValueError
            If the soil type with the given name is not found.
        """

        try:
            return self._get_name_map[name]
        except KeyError:
            available_names = '\n'.join(self._get_name_map.keys())
            raise ValueError(f"Soil type with name '{name}' not found. Expected one of the following:\n{available_names}")


# class SoilTypesTable2b(Enum):
#     # Gravel, slighly silty, loose
#     GRAVEL_SL_LOOSE = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.GRAVEL,
#         minor_composition=SoilMinorCompositions.SLITGHTLY_SILTY,
#         consistency=SoilConsistencies.LOOSE,
#         consolidation_state=None,
#         dutch_name="Grind, zwak siltig, los",
#     )

#     # Gravel, slightly silty, medium dense
#     GRAVEL_SL_SILTY_MEDIUM_DENSE = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.GRAVEL,
#         minor_composition=SoilMinorCompositions.SLITGHTLY_SILTY,
#         consistency=SoilConsistencies.MEDIUM_DENSE,
#         consolidation_state=None,
#         dutch_name="Grind, zwak siltig, matig",
#     )

#     # Gravel, slightly silty, dense
#     GRAVEL_SL_SILTY_DENSE = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.GRAVEL,
#         minor_composition=SoilMinorCompositions.SLITGHTLY_SILTY,
#         consistency=SoilConsistencies.DENSE,
#         consolidation_state=None,
#         dutch_name="Grind, zwak siltig, vast",
#     )

#     # Gravel, very silty, loose
#     GRAVEL_V_SILTY_LOOSE = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.GRAVEL,
#         minor_composition=SoilMinorCompositions.VERY_SILTY,
#         consistency=SoilConsistencies.LOOSE,
#         consolidation_state=None,
#         dutch_name="Grind, sterk siltig, los",
#     )

#     # Gravel, very silty, medium dense
#     GRAVEL_V_SILTY_MEDIUM_DENSE = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.GRAVEL,
#         minor_composition=SoilMinorCompositions.VERY_SILTY,
#         consistency=SoilConsistencies.MEDIUM_DENSE,
#         consolidation_state=None,
#         dutch_name="Grind, sterk siltig, matig",
#     )

#     # Gravel, very silty, dense
#     GRAVEL_V_SILTY_DENSE = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.GRAVEL,
#         minor_composition=SoilMinorCompositions.VERY_SILTY,
#         consistency=SoilConsistencies.DENSE,
#         consolidation_state=None,
#         dutch_name="Grind, sterk siltig, vast",
#     )

#     # Sand, clean, loose
#     SAND_CLEAN_LOOSE = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.SAND,
#         minor_composition=SoilMinorCompositions.CLEAN,
#         consistency=SoilConsistencies.LOOSE,
#         consolidation_state=None,
#         dutch_name="Zand, schoon, los",
#     )

#     # Sand, clean, medium dense
#     SAND_CLEAN_MEDIUM_DENSE = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.SAND,
#         minor_composition=SoilMinorCompositions.CLEAN,
#         consistency=SoilConsistencies.MEDIUM_DENSE,
#         consolidation_state=None,
#         dutch_name="Zand, schoon, matig",
#     )

#     # Sand, clean, dense
#     SAND_CLEAN_DENSE = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.SAND,
#         minor_composition=SoilMinorCompositions.CLEAN,
#         consistency=SoilConsistencies.DENSE,
#         consolidation_state=None,
#         dutch_name="Zand, schoon, vast",
#     )

#     # Sand, sligthly silty, clayey
#     SAND_SL_SILTY_CLAYEY = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.SAND,
#         minor_composition=SoilMinorCompositions.SLIGHTLY_SILTY_CLAYEY,
#         consistency=None,
#         consolidation_state=None,
#         dutch_name="Zand, zwak siltig, kleiig",
#     )

#     # Sand, very silty, clayey
#     SAND_V_SILTY_CLAYEY = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.SAND,
#         minor_composition=SoilMinorCompositions.VERY_SILTY_CLAYEY,
#         consistency=None,
#         consolidation_state=None,
#     )

#     # Loam, slightly sandy, loose
#     LOAM_SL_SANDY_SOFT = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.LOAM,
#         minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
#         consistency=SoilConsistencies.SOFT,
#         consolidation_state=None,
#     )

#     # Loam, slightly sandy, medium stiff
#     LOAM_SL_SANDY_MEDIUM_STIFF = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.LOAM,
#         minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
#         consistency=SoilConsistencies.MEDIUM_STIFF,
#         consolidation_state=None,
#     )

#     # Loam, slightly sandy, stiff
#     LOAM_SL_SANDY_STIFF = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.LOAM,
#         minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
#         consistency=SoilConsistencies.STIFF,
#         consolidation_state=None,
#     )

#     # Loam, slightly sandy
#     LOAM_SL_SANDY = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.LOAM,
#         minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
#         consistency=None,
#         consolidation_state=None,
#     )

#     # Loam, very sandy
#     LOAM_V_SANDY = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.LOAM,
#         minor_composition=SoilMinorCompositions.VERY_SANDY,
#         consistency=None,
#         consolidation_state=None,
#     )

#     # Clay, clean, soft
#     CLAY_CLEAN_SOFT = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.CLAY,
#         minor_composition=SoilMinorCompositions.CLEAN,
#         consistency=SoilConsistencies.SOFT,
#         consolidation_state=None,
#     )

#     # Clay, clean, medium stiff
#     CLAY_CLEAN_MEDIUM_STIFF = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.CLAY,
#         minor_composition=SoilMinorCompositions.CLEAN,
#         consistency=SoilConsistencies.MEDIUM_STIFF,
#         consolidation_state=None,
#     )

#     # Clay, clean, stiff
#     CLAY_CLEAN_STIFF = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.CLAY,
#         minor_composition=SoilMinorCompositions.CLEAN,
#         consistency=SoilConsistencies.STIFF,
#         consolidation_state=None,
#     )

#     # Clay, slightly sandy, soft
#     CLAY_SL_SANDY_SOFT = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.CLAY,
#         minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
#         consistency=SoilConsistencies.SOFT,
#         consolidation_state=None,
#     )

#     # Clay, slightly sandy, medium stiff
#     CLAY_SL_SANDY_MEDIUM_STIFF = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.CLAY,
#         minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
#         consistency=SoilConsistencies.MEDIUM_STIFF,
#         consolidation_state=None,
#     )

#     # Clay, slightly sandy, stiff
#     CLAY_SL_SANDY_STIFF = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.CLAY,
#         minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
#         consistency=SoilConsistencies.STIFF,
#         consolidation_state=None,
#     )

#     # Clay, very sandy
#     CLAY_V_SANDY = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.CLAY,
#         minor_composition=SoilMinorCompositions.VERY_SANDY,
#         consistency=None,
#         consolidation_state=None,
#     )

#     # Clay, organic
#     CLAY_ORGANIC = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.CLAY,
#         minor_composition=SoilMinorCompositions.ORGANIC,
#         consistency=None,
#         consolidation_state=None,
#     )

#     # Peat, normally consolidated
#     PEAT_NC = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.PEAT, minor_composition=None, consistency=None, consolidation_state=SoilConsolidationStates.NORMALLY_CONSOLIDATED
#     )

#     # Peat, overconsolidated
#     PEAT_OC = SoilTypeTable2bOld(
#         main_type=SoilMainTypes.PEAT,
#         minor_composition=None,
#         consistency=None,
#         consolidation_state=SoilConsolidationStates.MODERATELY_OVERCONSOLIDATED,
#     )


