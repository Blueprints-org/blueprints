"""Tests for StructuralPointActionFree dataclass.

Comprehensive test suite covering initialization, validation, and immutability
of the StructuralPointActionFree class following SAF specification.
"""

import pytest

from blueprints.saf.loads.structural_point_action_free import (
    Direction,
    StructuralPointActionFree,
)


class TestStructuralPointActionFreeValidInitialization:
    """Tests for valid StructuralPointActionFree initialization."""

    def test_point_load_x_direction(self) -> None:
        """Test free point load in X direction."""
        load = StructuralPointActionFree(
            name="FF1",
            direction=Direction.X,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=10.0,
        )
        assert load.name == "FF1"
        assert load.direction == Direction.X
        assert load.coordinate_x == 1.0
        assert load.coordinate_y == 2.0
        assert load.coordinate_z == 3.0
        assert load.value == 10.0

    def test_point_load_y_direction(self) -> None:
        """Test free point load in Y direction."""
        load = StructuralPointActionFree(
            name="FF2",
            direction=Direction.Y,
            load_case="LC1",
            coordinate_x=0.5,
            coordinate_y=1.5,
            coordinate_z=2.5,
            value=20.0,
        )
        assert load.direction == Direction.Y
        assert load.value == 20.0

    def test_point_load_z_direction(self) -> None:
        """Test free point load in Z direction."""
        load = StructuralPointActionFree(
            name="FF3",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=1.0,
            coordinate_z=3.25,
            value=-50.0,
        )
        assert load.direction == Direction.Z
        assert load.value == -50.0

    def test_vector_point_load(self) -> None:
        """Test free point load with vector direction."""
        load = StructuralPointActionFree(
            name="FF4",
            direction=Direction.VECTOR,
            load_case="LC1",
            coordinate_x=2.5,
            coordinate_y=3.0,
            coordinate_z=2.0,
            vector="10;10;-50",
        )
        assert load.direction == Direction.VECTOR
        assert load.vector == "10;10;-50"

    def test_negative_coordinate_values(self) -> None:
        """Test free point load with negative coordinates."""
        load = StructuralPointActionFree(
            name="FF5",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=-1.0,
            coordinate_y=-2.0,
            coordinate_z=-1.5,
            value=-30.0,
        )
        assert load.coordinate_x == -1.0
        assert load.coordinate_y == -2.0
        assert load.coordinate_z == -1.5

    def test_zero_coordinates(self) -> None:
        """Test free point load at origin."""
        load = StructuralPointActionFree(
            name="FF6",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=0.0,
            coordinate_y=0.0,
            coordinate_z=0.0,
            value=-10.0,
        )
        assert load.coordinate_x == 0.0
        assert load.coordinate_y == 0.0
        assert load.coordinate_z == 0.0

    def test_with_action_type(self) -> None:
        """Test free point load with action type."""
        load = StructuralPointActionFree(
            name="FF7",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=-25.0,
            action_type="Wind",
        )
        assert load.action_type == "Wind"

    def test_with_uuid(self) -> None:
        """Test free point load with UUID identifier."""
        load = StructuralPointActionFree(
            name="FF8",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=-10.0,
            id="550e8400-e29b-41d4-a716-446655440000",
        )
        assert load.id == "550e8400-e29b-41d4-a716-446655440000"

    def test_large_coordinate_values(self) -> None:
        """Test free point load with large coordinate values."""
        load = StructuralPointActionFree(
            name="FF9",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=100.5,
            coordinate_y=200.75,
            coordinate_z=50.25,
            value=-40.0,
        )
        assert load.coordinate_x == 100.5
        assert load.coordinate_y == 200.75
        assert load.coordinate_z == 50.25

    def test_vector_with_negative_components(self) -> None:
        """Test vector load with negative components."""
        load = StructuralPointActionFree(
            name="FF10",
            direction=Direction.VECTOR,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            vector="-10;20;-30",
        )
        assert load.vector == "-10;20;-30"


class TestStructuralPointActionFreeValidation:
    """Tests for StructuralPointActionFree validation."""

    def test_vector_direction_requires_vector(self) -> None:
        """Test that VECTOR direction requires vector."""
        with pytest.raises(ValueError, match="vector must be specified"):
            StructuralPointActionFree(
                name="FF1",
                direction=Direction.VECTOR,
                load_case="LC1",
                coordinate_x=1.0,
                coordinate_y=2.0,
                coordinate_z=3.0,
            )

    def test_vector_format_validation(self) -> None:
        """Test that vector format must contain semicolons."""
        with pytest.raises(ValueError, match="must be in 'X;Y;Z' format"):
            StructuralPointActionFree(
                name="FF1",
                direction=Direction.VECTOR,
                load_case="LC1",
                coordinate_x=1.0,
                coordinate_y=2.0,
                coordinate_z=3.0,
                vector="10,20,30",  # Wrong format
            )

    def test_single_axis_direction_requires_value(self) -> None:
        """Test that single-axis directions require value."""
        with pytest.raises(ValueError, match="value must be specified"):
            StructuralPointActionFree(
                name="FF1",
                direction=Direction.X,
                load_case="LC1",
                coordinate_x=1.0,
                coordinate_y=2.0,
                coordinate_z=3.0,
            )

    def test_x_direction_requires_value(self) -> None:
        """Test that X direction requires value."""
        with pytest.raises(ValueError, match="value must be specified"):
            StructuralPointActionFree(
                name="FF1",
                direction=Direction.X,
                load_case="LC1",
                coordinate_x=1.0,
                coordinate_y=2.0,
                coordinate_z=3.0,
            )

    def test_y_direction_requires_value(self) -> None:
        """Test that Y direction requires value."""
        with pytest.raises(ValueError, match="value must be specified"):
            StructuralPointActionFree(
                name="FF1",
                direction=Direction.Y,
                load_case="LC1",
                coordinate_x=1.0,
                coordinate_y=2.0,
                coordinate_z=3.0,
            )

    def test_z_direction_requires_value(self) -> None:
        """Test that Z direction requires value."""
        with pytest.raises(ValueError, match="value must be specified"):
            StructuralPointActionFree(
                name="FF1",
                direction=Direction.Z,
                load_case="LC1",
                coordinate_x=1.0,
                coordinate_y=2.0,
                coordinate_z=3.0,
            )


class TestStructuralPointActionFreeEquality:
    """Tests for StructuralPointActionFree equality."""

    def test_equal_loads_with_same_attributes(self) -> None:
        """Test that loads with same attributes are equal."""
        load1 = StructuralPointActionFree(
            name="FF1",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=-10.0,
        )
        load2 = StructuralPointActionFree(
            name="FF1",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=-10.0,
        )
        assert load1 == load2

    def test_unequal_loads_different_coordinates(self) -> None:
        """Test that loads with different coordinates are not equal."""
        load1 = StructuralPointActionFree(
            name="FF1",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=-10.0,
        )
        load2 = StructuralPointActionFree(
            name="FF1",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.5,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=-10.0,
        )
        assert load1 != load2

    def test_frozen_immutability(self) -> None:
        """Test that load instances are frozen (immutable)."""
        load = StructuralPointActionFree(
            name="FF1",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=-10.0,
        )
        with pytest.raises(AttributeError):
            load.value = -20.0  # type: ignore[misc]


class TestDirectionEnum:
    """Tests for Direction enum."""

    def test_x_direction(self) -> None:
        """Test X direction."""
        assert Direction.X.value == "X"

    def test_y_direction(self) -> None:
        """Test Y direction."""
        assert Direction.Y.value == "Y"

    def test_z_direction(self) -> None:
        """Test Z direction."""
        assert Direction.Z.value == "Z"

    def test_vector_direction(self) -> None:
        """Test VECTOR direction."""
        assert Direction.VECTOR.value == "Vector"

    def test_all_directions_exist(self) -> None:
        """Test that all directions are defined."""
        directions = list(Direction)
        assert len(directions) == 4


class TestStructuralPointActionFreeEdgeCases:
    """Tests for StructuralPointActionFree edge cases."""

    def test_very_large_load_value(self) -> None:
        """Test load with very large value."""
        load = StructuralPointActionFree(
            name="FF1",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=-1e10,
        )
        assert load.value == -1e10

    def test_very_small_load_value(self) -> None:
        """Test load with very small value."""
        load = StructuralPointActionFree(
            name="FF1",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=1e-10,
        )
        assert load.value == 1e-10

    def test_fractional_coordinates(self) -> None:
        """Test load with fractional coordinates."""
        load = StructuralPointActionFree(
            name="FF1",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.25,
            coordinate_y=2.75,
            coordinate_z=3.333,
            value=-15.0,
        )
        assert load.coordinate_x == 1.25
        assert load.coordinate_y == 2.75
        assert load.coordinate_z == 3.333

    def test_zero_value_load(self) -> None:
        """Test load with zero value."""
        load = StructuralPointActionFree(
            name="FF1",
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x=1.0,
            coordinate_y=2.0,
            coordinate_z=3.0,
            value=0.0,
        )
        assert load.value == 0.0
