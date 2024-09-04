"""Tests of the materials soil module."""

from typing import Type

import pytest

from blueprints.materials.soil import SoilConsistencies, SoilConsolidationStates, SoilMainTypes, SoilMinorCompositions, SoilType


@pytest.mark.parametrize(
    ("main_type", "minor_composition", "consolidation_state", "consistency", "description"),
    [
        (SoilMainTypes.SAND, SoilMinorCompositions.CLEAN, None, SoilConsistencies.LOOSE, None),
        (SoilMainTypes.LOAM, SoilMinorCompositions.VERY_SANDY, None, None, None),
        (SoilMainTypes.PEAT, None, SoilConsolidationStates.NORMALLY_CONSOLIDATED, None, None),
        (SoilMainTypes.PEAT, None, SoilConsolidationStates.NORMALLY_CONSOLIDATED, None, "Veen, nvt"),
    ],
)
def test_soil_type_init_valid_input(
    main_type: SoilMainTypes,
    minor_composition: SoilMinorCompositions,
    consolidation_state: SoilConsolidationStates | None,
    consistency: SoilConsistencies | None,
    description: str | None,
) -> None:
    """Tests initialization of SoilType for valid input."""
    # Giving None as input
    soil_type = SoilType(
        main_type=main_type,
        minor_composition=minor_composition,
        consolidation_state=consolidation_state,
        consistency=consistency,
        description=description,
    )

    assert soil_type.main_type == main_type
    assert soil_type.minor_composition == minor_composition
    assert soil_type.consolidation_state == consolidation_state
    assert soil_type.consistency == consistency
    assert soil_type.description == description

    # Skipping parameters given as None
    default_kwargs = {
        "main_type": main_type,
        "minor_composition": minor_composition,
        "consolidation_state": consolidation_state,
        "consistency": consistency,
        "description": description,
    }

    kwargs = {k: v for k, v in default_kwargs.items() if v is not None}

    soil_type = SoilType(**kwargs)  # type: ignore[PGH003]

    assert soil_type.main_type == main_type
    assert soil_type.minor_composition == minor_composition
    assert soil_type.consolidation_state == consolidation_state
    assert soil_type.consistency == consistency
    assert soil_type.description == description


@pytest.mark.parametrize(
    ("main_type", "minor_composition", "consolidation_state", "consistency", "description", "expected_error", "expected_message_pattern"),
    [
        # Wrong types
        ("sand", SoilMinorCompositions.CLEAN, None, SoilConsistencies.LOOSE, None, TypeError, "`main_type`"),
        (SoilMainTypes.SAND, "clean", None, SoilConsistencies.LOOSE, None, TypeError, "`minor_composition`"),
        (SoilMainTypes.SAND, SoilMinorCompositions.CLEAN, "None", SoilConsistencies.LOOSE, None, TypeError, "`consolidation_state`"),
        (SoilMainTypes.SAND, SoilMinorCompositions.CLEAN, None, "loose", None, TypeError, "`consistency`"),
        (SoilMainTypes.SAND, SoilMinorCompositions.CLEAN, None, SoilConsistencies.LOOSE, 1, TypeError, "`description`"),
    ],
)
def test_soil_type_init_invalid_input(
    main_type: SoilMainTypes,
    minor_composition: SoilMinorCompositions,
    consolidation_state: SoilConsolidationStates | None,
    consistency: SoilConsistencies | None,
    description: str | None,
    expected_error: Type[Exception],
    expected_message_pattern: str,
) -> None:
    """Tests expected errors for SoilType initialization with invalid input. Note that this also test the property setters."""
    with pytest.raises(expected_error, match=expected_message_pattern):
        SoilType(
            main_type=main_type,
            minor_composition=minor_composition,
            consolidation_state=consolidation_state,
            consistency=consistency,
            description=description,
        )


@pytest.mark.parametrize(
    ("main_type", "minor_composition", "consolidation_state", "consistency", "expected_default_description"),
    [
        (SoilMainTypes.CLAY, None, None, None, "Clay"),
        (SoilMainTypes.LOAM, SoilMinorCompositions.VERY_SANDY, None, None, "Loam, Very sandy"),
        (SoilMainTypes.SAND, SoilMinorCompositions.CLEAN, None, SoilConsistencies.LOOSE, "Sand, Clean, Loose"),
        (SoilMainTypes.PEAT, None, SoilConsolidationStates.NORMALLY_CONSOLIDATED, None, "Peat, Normally consolidated"),
    ],
)
def test_soil_type_default_description(
    main_type: SoilMainTypes,
    minor_composition: SoilMinorCompositions,
    consolidation_state: SoilConsolidationStates | None,
    consistency: SoilConsistencies | None,
    expected_default_description: str,
) -> None:
    """Tests the property method `default_description` of SoilType."""
    soil_type = SoilType(
        main_type=main_type,
        minor_composition=minor_composition,
        consolidation_state=consolidation_state,
        consistency=consistency,
    )

    assert soil_type.default_description == expected_default_description
