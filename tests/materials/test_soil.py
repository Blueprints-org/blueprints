"""Tests of the materials soil module."""

import pytest

from blueprints.materials.soil import SoilConsistencies, SoilConsolidationStates, SoilMainTypes, SoilMinorCompositions, SoilType


class TestSoilType:
    """Tests for the SoilType class."""

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
        self,
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

        assert soil_type

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
        self,
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
