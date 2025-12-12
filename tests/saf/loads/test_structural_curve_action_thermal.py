"""Tests for StructuralCurveActionThermal dataclass.

Comprehensive test suite covering initialization, validation, and immutability
of the StructuralCurveActionThermal class following SAF specification.
"""

import pytest

from blueprints.saf.loads.structural_curve_action_thermal import (
    CoordinateDefinition,
    ForceAction,
    Origin,
    StructuralCurveActionThermal,
    Variation,
)


class TestStructuralCurveActionThermalValidInitialization:
    """Tests for valid StructuralCurveActionThermal initialization."""

    def test_constant_thermal_on_beam(self) -> None:
        """Test constant thermal load on beam."""
        thermal = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=25.0,
            member="B1",
        )
        assert thermal.name == "LT1"
        assert thermal.variation == Variation.CONSTANT
        assert thermal.delta_t == 25.0

    def test_linear_thermal_on_beam(self) -> None:
        """Test linear thermal load on beam."""
        thermal = StructuralCurveActionThermal(
            name="LT2",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.LINEAR,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            temp_l=20.0,
            temp_r=15.0,
            temp_t=30.0,
            temp_b=10.0,
            member="B1",
        )
        assert thermal.variation == Variation.LINEAR
        assert thermal.temp_l == 20.0
        assert thermal.temp_r == 15.0
        assert thermal.temp_t == 30.0
        assert thermal.temp_b == 10.0

    def test_constant_thermal_on_rib(self) -> None:
        """Test constant thermal load on rib."""
        thermal = StructuralCurveActionThermal(
            name="LT3",
            force_action=ForceAction.ON_RIB,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=3.0,
            delta_t=15.0,
            member_rib="R1",
        )
        assert thermal.force_action == ForceAction.ON_RIB
        assert thermal.member_rib == "R1"

    def test_linear_thermal_on_rib(self) -> None:
        """Test linear thermal load on rib."""
        thermal = StructuralCurveActionThermal(
            name="LT4",
            force_action=ForceAction.ON_RIB,
            variation=Variation.LINEAR,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=3.5,
            temp_l=20.0,
            temp_r=15.0,
            temp_t=30.0,
            temp_b=10.0,
            member_rib="R1",
        )
        assert thermal.force_action == ForceAction.ON_RIB

    def test_relative_positions(self) -> None:
        """Test thermal load with relative positions."""
        thermal = StructuralCurveActionThermal(
            name="LT5",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.RELATIVE,
            origin=Origin.FROM_START,
            start_point=0.2,
            end_point=0.8,
            delta_t=20.0,
            member="B1",
        )
        assert thermal.coordinate_definition == CoordinateDefinition.RELATIVE
        assert thermal.start_point == 0.2
        assert thermal.end_point == 0.8

    def test_from_end_origin(self) -> None:
        """Test thermal load with FROM_END origin."""
        thermal = StructuralCurveActionThermal(
            name="LT6",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_END,
            start_point=0.0,
            end_point=2.5,
            delta_t=18.0,
            member="B1",
        )
        assert thermal.origin == Origin.FROM_END

    def test_negative_temperature(self) -> None:
        """Test thermal load with negative temperature (cooling)."""
        thermal = StructuralCurveActionThermal(
            name="LT7",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=-15.0,
            member="B1",
        )
        assert thermal.delta_t == -15.0

    def test_with_uuid(self) -> None:
        """Test thermal load with UUID identifier."""
        thermal = StructuralCurveActionThermal(
            name="LT8",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=25.0,
            member="B1",
            id="550e8400-e29b-41d4-a716-446655440000",
        )
        assert thermal.id == "550e8400-e29b-41d4-a716-446655440000"

    def test_linear_with_mixed_temperature_values(self) -> None:
        """Test linear variation with mixed positive and negative temperatures."""
        thermal = StructuralCurveActionThermal(
            name="LT9",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.LINEAR,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            temp_l=30.0,
            temp_r=-10.0,
            temp_t=40.0,
            temp_b=-20.0,
            member="B1",
        )
        assert thermal.temp_l == 30.0
        assert thermal.temp_r == -10.0


class TestStructuralCurveActionThermalValidation:
    """Tests for StructuralCurveActionThermal validation."""

    def test_constant_requires_delta_t(self) -> None:
        """Test that CONSTANT variation requires delta_t."""
        with pytest.raises(ValueError, match="delta_t must be specified"):
            StructuralCurveActionThermal(
                name="LT1",
                force_action=ForceAction.ON_BEAM,
                variation=Variation.CONSTANT,
                load_case="LC1",
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=5.0,
                member="B1",
            )

    def test_linear_requires_all_temperatures(self) -> None:
        """Test that LINEAR variation requires all 4 temperature components."""
        with pytest.raises(ValueError, match="temp_l must be specified"):
            StructuralCurveActionThermal(
                name="LT1",
                force_action=ForceAction.ON_BEAM,
                variation=Variation.LINEAR,
                load_case="LC1",
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=5.0,
                temp_r=15.0,
                temp_t=30.0,
                temp_b=10.0,
                member="B1",
            )

    def test_linear_requires_temp_r(self) -> None:
        """Test that LINEAR variation requires temp_r."""
        with pytest.raises(ValueError, match="temp_r must be specified"):
            StructuralCurveActionThermal(
                name="LT1",
                force_action=ForceAction.ON_BEAM,
                variation=Variation.LINEAR,
                load_case="LC1",
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=5.0,
                temp_l=20.0,
                temp_t=30.0,
                temp_b=10.0,
                member="B1",
            )

    def test_linear_requires_temp_t(self) -> None:
        """Test that LINEAR variation requires temp_t."""
        with pytest.raises(ValueError, match="temp_t must be specified"):
            StructuralCurveActionThermal(
                name="LT1",
                force_action=ForceAction.ON_BEAM,
                variation=Variation.LINEAR,
                load_case="LC1",
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=5.0,
                temp_l=20.0,
                temp_r=15.0,
                temp_b=10.0,
                member="B1",
            )

    def test_linear_requires_temp_b(self) -> None:
        """Test that LINEAR variation requires temp_b."""
        with pytest.raises(ValueError, match="temp_b must be specified"):
            StructuralCurveActionThermal(
                name="LT1",
                force_action=ForceAction.ON_BEAM,
                variation=Variation.LINEAR,
                load_case="LC1",
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=5.0,
                temp_l=20.0,
                temp_r=15.0,
                temp_t=30.0,
                member="B1",
            )

    def test_on_beam_requires_member(self) -> None:
        """Test that ON_BEAM force action requires member."""
        with pytest.raises(ValueError, match="member must be specified"):
            StructuralCurveActionThermal(
                name="LT1",
                force_action=ForceAction.ON_BEAM,
                variation=Variation.CONSTANT,
                load_case="LC1",
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=5.0,
                delta_t=25.0,
            )

    def test_on_rib_requires_member_rib(self) -> None:
        """Test that ON_RIB force action requires member_rib."""
        with pytest.raises(ValueError, match="member_rib must be specified"):
            StructuralCurveActionThermal(
                name="LT1",
                force_action=ForceAction.ON_RIB,
                variation=Variation.CONSTANT,
                load_case="LC1",
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=5.0,
                delta_t=25.0,
            )


class TestStructuralCurveActionThermalEquality:
    """Tests for StructuralCurveActionThermal equality."""

    def test_equal_thermals_with_same_attributes(self) -> None:
        """Test that thermals with same attributes are equal."""
        t1 = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=25.0,
            member="B1",
        )
        t2 = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=25.0,
            member="B1",
        )
        assert t1 == t2

    def test_unequal_thermals_different_temperatures(self) -> None:
        """Test that thermals with different temperatures are not equal."""
        t1 = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=25.0,
            member="B1",
        )
        t2 = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=30.0,
            member="B1",
        )
        assert t1 != t2

    def test_frozen_immutability(self) -> None:
        """Test that thermal instances are frozen (immutable)."""
        thermal = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=25.0,
            member="B1",
        )
        with pytest.raises(AttributeError):
            thermal.delta_t = 30.0  # type: ignore[misc]


class TestStructuralCurveActionThermalEdgeCases:
    """Tests for StructuralCurveActionThermal edge cases."""

    def test_very_large_temperature(self) -> None:
        """Test thermal with very large temperature."""
        thermal = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=1000.0,
            member="B1",
        )
        assert thermal.delta_t == 1000.0

    def test_very_small_temperature(self) -> None:
        """Test thermal with very small fractional temperature."""
        thermal = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=0.1,
            member="B1",
        )
        assert thermal.delta_t == 0.1

    def test_zero_temperature(self) -> None:
        """Test thermal with zero temperature."""
        thermal = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.CONSTANT,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            delta_t=0.0,
            member="B1",
        )
        assert thermal.delta_t == 0.0

    def test_linear_with_zero_temperatures(self) -> None:
        """Test linear variation with zero temperatures."""
        thermal = StructuralCurveActionThermal(
            name="LT1",
            force_action=ForceAction.ON_BEAM,
            variation=Variation.LINEAR,
            load_case="LC1",
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            temp_l=0.0,
            temp_r=0.0,
            temp_t=0.0,
            temp_b=0.0,
            member="B1",
        )
        assert thermal.temp_l == 0.0
