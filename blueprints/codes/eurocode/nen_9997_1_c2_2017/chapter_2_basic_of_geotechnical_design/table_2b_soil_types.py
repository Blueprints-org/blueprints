from enum import Enum

from blueprints.materials.soil import (SoilConsistencies,
                                       SoilConsolidationStates, SoilMainTypes,
                                       SoilMinorCompositions, SoilType)


class SoilTypesTable2b(Enum):
    # Gravel, slighly silty, loose
    GRAVEL_SL_LOOSE = SoilType(
        main_type=SoilMainTypes.GRAVEL,
        minor_composition=SoilMinorCompositions.SLITGHTLY_SILTY,
        consistency=SoilConsistencies.LOOSE,
        consolidation_state=None,
    )

    # Gravel, slightly silty, medium dense
    GRAVEL_SL_SILTY_MEDIUM_DENSE = SoilType(
        main_type=SoilMainTypes.GRAVEL,
        minor_composition=SoilMinorCompositions.SLITGHTLY_SILTY,
        consistency=SoilConsistencies.MEDIUM_DENSE,
        consolidation_state=None,
    )

    # Gravel, slightly silty, dense
    GRAVEL_SL_SILTY_DENSE = SoilType(
        main_type=SoilMainTypes.GRAVEL,
        minor_composition=SoilMinorCompositions.SLITGHTLY_SILTY,
        consistency=SoilConsistencies.DENSE,
        consolidation_state=None,
    )

    # Gravel, very silty, loose
    GRAVEL_V_SILTY_LOOSE = SoilType(
        main_type=SoilMainTypes.GRAVEL,
        minor_composition=SoilMinorCompositions.VERY_SILTY,
        consistency=SoilConsistencies.LOOSE,
        consolidation_state=None,
    )

    # Gravel, very silty, medium dense
    GRAVEL_V_SILTY_MEDIUM_DENSE = SoilType(
        main_type=SoilMainTypes.GRAVEL,
        minor_composition=SoilMinorCompositions.VERY_SILTY,
        consistency=SoilConsistencies.MEDIUM_DENSE,
        consolidation_state=None,
    )

    # Gravel, very silty, dense
    GRAVEL_V_SILTY_DENSE = SoilType(
        main_type=SoilMainTypes.GRAVEL,
        minor_composition=SoilMinorCompositions.VERY_SILTY,
        consistency=SoilConsistencies.DENSE,
        consolidation_state=None,
    )

    # Sand, clean, loose
    SAND_CLEAN_LOOSE = SoilType(
        main_type=SoilMainTypes.SAND,
        minor_composition=SoilMinorCompositions.CLEAN,
        consistency=SoilConsistencies.LOOSE,
        consolidation_state=None,
    )

    # Sand, clean, medium dense
    SAND_CLEAN_MEDIUM_DENSE = SoilType(
        main_type=SoilMainTypes.SAND,
        minor_composition=SoilMinorCompositions.CLEAN,
        consistency=SoilConsistencies.MEDIUM_DENSE,
        consolidation_state=None,
    )

    # Sand, clean, dense
    SAND_CLEAN_DENSE = SoilType(
        main_type=SoilMainTypes.SAND,
        minor_composition=SoilMinorCompositions.CLEAN,
        consistency=SoilConsistencies.DENSE,
        consolidation_state=None,
    )

    # Sand, sligthly silty, clayey
    SAND_SL_SILTY_CLAYEY = SoilType(
        main_type=SoilMainTypes.SAND,
        minor_composition=SoilMinorCompositions.SLIGHTLY_SILTY_CLAYEY,
        consistency=None,
        consolidation_state=None,
    )

    # Sand, very silty, clayey
    SAND_V_SILTY_CLAYEY = SoilType(
        main_type=SoilMainTypes.SAND,
        minor_composition=SoilMinorCompositions.VERY_SILTY_CLAYEY,
        consistency=None,
        consolidation_state=None,
    )

    # Loam, slightly sandy, loose
    LOAM_SL_SANDY_SOFT = SoilType(
        main_type=SoilMainTypes.LOAM,
        minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
        consistency=SoilConsistencies.SOFT,
        consolidation_state=None,
    )

    # Loam, slightly sandy, medium stiff
    LOAM_SL_SANDY_MEDIUM_STIFF = SoilType(
        main_type=SoilMainTypes.LOAM,
        minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
        consistency=SoilConsistencies.MEDIUM_STIFF,
        consolidation_state=None,
    )

    # Loam, slightly sandy, stiff
    LOAM_SL_SANDY_STIFF = SoilType(
        main_type=SoilMainTypes.LOAM,
        minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
        consistency=SoilConsistencies.STIFF,
        consolidation_state=None,
    )

    # Loam, slightly sandy
    LOAM_SL_SANDY = SoilType(
        main_type=SoilMainTypes.LOAM,
        minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
        consistency=None,
        consolidation_state=None,
    )

    # Loam, very sandy
    LOAM_V_SANDY = SoilType(
        main_type=SoilMainTypes.LOAM,
        minor_composition=SoilMinorCompositions.VERY_SANDY,
        consistency=None,
        consolidation_state=None,
    )

    # Clay, clean, soft
    CLAY_CLEAN_SOFT = SoilType(
        main_type=SoilMainTypes.CLAY,
        minor_composition=SoilMinorCompositions.CLEAN,
        consistency=SoilConsistencies.SOFT,
        consolidation_state=None,
    )

    # Clay, clean, medium stiff
    CLAY_CLEAN_MEDIUM_STIFF = SoilType(
        main_type=SoilMainTypes.CLAY,
        minor_composition=SoilMinorCompositions.CLEAN,
        consistency=SoilConsistencies.MEDIUM_STIFF,
        consolidation_state=None,
    )

    # Clay, clean, stiff
    CLAY_CLEAN_STIFF = SoilType(
        main_type=SoilMainTypes.CLAY,
        minor_composition=SoilMinorCompositions.CLEAN,
        consistency=SoilConsistencies.STIFF,
        consolidation_state=None,
    )

    # Clay, slightly sandy, soft
    CLAY_SL_SANDY_SOFT = SoilType(
        main_type=SoilMainTypes.CLAY,
        minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
        consistency=SoilConsistencies.SOFT,
        consolidation_state=None,
    )

    # Clay, slightly sandy, medium stiff
    CLAY_SL_SANDY_MEDIUM_STIFF = SoilType(
        main_type=SoilMainTypes.CLAY,
        minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
        consistency=SoilConsistencies.MEDIUM_STIFF,
        consolidation_state=None,
    )

    # Clay, slightly sandy, stiff
    CLAY_SL_SANDY_STIFF = SoilType(
        main_type=SoilMainTypes.CLAY,
        minor_composition=SoilMinorCompositions.SLIGHTLY_SANDY,
        consistency=SoilConsistencies.STIFF,
        consolidation_state=None,
    )

    # Clay, very sandy
    CLAY_V_SANDY = SoilType(
        main_type=SoilMainTypes.CLAY,
        minor_composition=SoilMinorCompositions.VERY_SANDY,
        consistency=None,
        consolidation_state=None,
    )

    # Clay, organic
    CLAY_ORGANIC = SoilType(
        main_type=SoilMainTypes.CLAY,
        minor_composition=SoilMinorCompositions.ORGANIC,
        consistency=None,
        consolidation_state=None,
    )

    # Peat, normally consolidated
    PEAT_NC = SoilType(
        main_type=SoilMainTypes.PEAT, minor_composition=None, consistency=None, consolidation_state=SoilConsolidationStates.NORMALLY_CONSOLIDATED
    )

    # Peat, overconsolidated
    PEAT_OC = SoilType(
        main_type=SoilMainTypes.PEAT,
        minor_composition=None,
        consistency=None,
        consolidation_state=SoilConsolidationStates.MODERATELY_OVERCONSOLIDATED,
    )


