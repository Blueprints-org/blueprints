"""Tests for StructuralSurfaceActionThermal dataclass.

Comprehensive test suite covering initialization, validation, and immutability
of the StructuralSurfaceActionThermal class following SAF specification.
"""

import pytest

from blueprints.saf.loads.structural_surface_action_thermal import (
    StructuralSurfaceActionThermal,
    Variation,
)


class TestStructuralSurfaceActionThermalValidInitialization:
    """Tests for valid StructuralSurfaceActionThermal initialization."""

    def test_constant_temperature(self) -> None:
        """Test thermal load with constant temperature."""
        thermal = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.name == "LT1"
        assert thermal.variation == Variation.CONSTANT
        assert thermal.temp_t == 25.0
        assert thermal.two_d_member == "S1"

    def test_linear_temperature_variation(self) -> None:
        """Test thermal load with linear temperature variation."""
        thermal = StructuralSurfaceActionThermal(
            name="LT2",
            variation=Variation.LINEAR,
            temp_t=30.0,
            temp_b=10.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.variation == Variation.LINEAR
        assert thermal.temp_t == 30.0
        assert thermal.temp_b == 10.0

    def test_negative_temperature(self) -> None:
        """Test thermal load with negative temperature (cooling)."""
        thermal = StructuralSurfaceActionThermal(
            name="LT3",
            variation=Variation.CONSTANT,
            temp_t=-15.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.temp_t == -15.0

    def test_zero_temperature(self) -> None:
        """Test thermal load with zero temperature."""
        thermal = StructuralSurfaceActionThermal(
            name="LT4",
            variation=Variation.CONSTANT,
            temp_t=0.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.temp_t == 0.0

    def test_thermal_on_member_region(self) -> None:
        """Test thermal load on specific member region."""
        thermal = StructuralSurfaceActionThermal(
            name="LT5",
            variation=Variation.CONSTANT,
            temp_t=20.0,
            load_case="LC1",
            two_d_member="S1",
            two_d_member_region="R1",
        )
        assert thermal.two_d_member_region == "R1"

    def test_thermal_with_uuid(self) -> None:
        """Test thermal load with UUID identifier."""
        thermal = StructuralSurfaceActionThermal(
            name="LT6",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
            id="550e8400-e29b-41d4-a716-446655440000",
        )
        assert thermal.id == "550e8400-e29b-41d4-a716-446655440000"

    def test_very_large_temperature(self) -> None:
        """Test thermal load with very large temperature."""
        thermal = StructuralSurfaceActionThermal(
            name="LT7",
            variation=Variation.CONSTANT,
            temp_t=1000.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.temp_t == 1000.0

    def test_very_small_temperature(self) -> None:
        """Test thermal load with very small temperature."""
        thermal = StructuralSurfaceActionThermal(
            name="LT8",
            variation=Variation.CONSTANT,
            temp_t=0.1,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.temp_t == 0.1

    def test_linear_with_different_temperatures(self) -> None:
        """Test linear variation with significantly different top and bottom temperatures."""
        thermal = StructuralSurfaceActionThermal(
            name="LT9",
            variation=Variation.LINEAR,
            temp_t=50.0,
            temp_b=-10.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.temp_t == 50.0
        assert thermal.temp_b == -10.0

    def test_linear_with_same_temperatures(self) -> None:
        """Test linear variation with same top and bottom temperatures."""
        thermal = StructuralSurfaceActionThermal(
            name="LT10",
            variation=Variation.LINEAR,
            temp_t=25.0,
            temp_b=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.temp_t == 25.0
        assert thermal.temp_b == 25.0


class TestStructuralSurfaceActionThermalValidation:
    """Tests for StructuralSurfaceActionThermal validation."""

    def test_linear_variation_requires_temp_b(self) -> None:
        """Test that LINEAR variation requires temp_b."""
        with pytest.raises(ValueError, match="temp_b must be specified"):
            StructuralSurfaceActionThermal(
                name="LT1",
                variation=Variation.LINEAR,
                temp_t=25.0,
                load_case="LC1",
                two_d_member="S1",
            )

    def test_constant_variation_does_not_require_temp_b(self) -> None:
        """Test that CONSTANT variation does not require temp_b."""
        thermal = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.temp_b is None


class TestStructuralSurfaceActionThermalEquality:
    """Tests for StructuralSurfaceActionThermal equality."""

    def test_equal_thermals_with_same_attributes(self) -> None:
        """Test that thermal loads with same attributes are equal."""
        t1 = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        t2 = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert t1 == t2

    def test_unequal_thermals_different_temperatures(self) -> None:
        """Test that thermal loads with different temperatures are not equal."""
        t1 = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        t2 = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=30.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert t1 != t2

    def test_unequal_thermals_different_variations(self) -> None:
        """Test that thermal loads with different variations are not equal."""
        t1 = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        t2 = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.LINEAR,
            temp_t=25.0,
            temp_b=20.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert t1 != t2

    def test_hashable_thermals(self) -> None:
        """Test that thermal loads are hashable (can be used in sets/dicts)."""
        thermal = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        thermal_set = {thermal}
        assert thermal in thermal_set

    def test_frozen_immutability(self) -> None:
        """Test that thermal load instances are frozen (immutable)."""
        thermal = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        with pytest.raises(AttributeError):
            thermal.temp_t = 30.0  # type: ignore[misc]


class TestVariationEnum:
    """Tests for Variation enum."""

    def test_constant_variation(self) -> None:
        """Test CONSTANT variation."""
        assert Variation.CONSTANT.value == "Constant"

    def test_linear_variation(self) -> None:
        """Test LINEAR variation."""
        assert Variation.LINEAR.value == "Linear"

    def test_all_variations_exist(self) -> None:
        """Test that all variations are defined."""
        variations = list(Variation)
        assert len(variations) == 2
        assert Variation.CONSTANT in variations
        assert Variation.LINEAR in variations


class TestStructuralSurfaceActionThermalEdgeCases:
    """Tests for StructuralSurfaceActionThermal edge cases."""

    def test_fractional_temperature(self) -> None:
        """Test thermal load with fractional temperature."""
        thermal = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.75,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.temp_t == 25.75

    def test_linear_with_negative_bottom_temperature(self) -> None:
        """Test linear variation with negative bottom temperature."""
        thermal = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.LINEAR,
            temp_t=40.0,
            temp_b=-20.0,
            load_case="LC1",
            two_d_member="S1",
        )
        assert thermal.temp_t == 40.0
        assert thermal.temp_b == -20.0

    def test_multiple_thermal_loads_in_set(self) -> None:
        """Test that multiple thermal loads can be stored in a set."""
        t1 = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        t2 = StructuralSurfaceActionThermal(
            name="LT2",
            variation=Variation.LINEAR,
            temp_t=30.0,
            temp_b=10.0,
            load_case="LC1",
            two_d_member="S2",
        )
        thermal_set = {t1, t2}
        assert len(thermal_set) == 2
        assert t1 in thermal_set
        assert t2 in thermal_set

    def test_thermal_in_dict(self) -> None:
        """Test that thermal loads can be used as dict keys."""
        thermal = StructuralSurfaceActionThermal(
            name="LT1",
            variation=Variation.CONSTANT,
            temp_t=25.0,
            load_case="LC1",
            two_d_member="S1",
        )
        thermal_dict = {thermal: "description"}
        assert thermal_dict[thermal] == "description"
