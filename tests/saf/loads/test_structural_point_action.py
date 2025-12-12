"""Tests for StructuralPointAction dataclass."""

import pytest

from blueprints.saf.loads.structural_point_action import (
    CoordinateDefinition,
    CoordinateSystem,
    Direction,
    ForceAction,
    Origin,
    StructuralPointAction,
)


class TestStructuralPointAction:
    """Tests for StructuralPointAction dataclass."""

    # Valid Initialization Tests - In Node Loads

    def test_in_node_load_x_direction_global(self) -> None:
        """Test point load at node in X direction (global)."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.X,
            force_action=ForceAction.IN_NODE,
            value="50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )

        assert action.name == "F1"
        assert action.direction == Direction.X
        assert action.force_action == ForceAction.IN_NODE
        assert action.value == "50"
        assert action.reference_node == "N1"

    def test_in_node_load_y_direction_local(self) -> None:
        """Test point load at node in Y direction (local)."""
        action = StructuralPointAction(
            name="F2",
            direction=Direction.Y,
            force_action=ForceAction.IN_NODE,
            value="-25.5",
            load_case="LC1",
            coordinate_system=CoordinateSystem.LOCAL,
            reference_node="N2",
        )

        assert action.direction == Direction.Y
        assert action.value == "-25.5"
        assert action.coordinate_system == CoordinateSystem.LOCAL

    def test_in_node_load_z_direction(self) -> None:
        """Test point load at node in Z direction."""
        action = StructuralPointAction(
            name="F3",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-100",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N3",
        )

        assert action.direction == Direction.Z

    def test_in_node_load_vector_direction(self) -> None:
        """Test point load at node with vector direction."""
        action = StructuralPointAction(
            name="F4",
            direction=Direction.VECTOR,
            force_action=ForceAction.IN_NODE,
            value="10;20;-30",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N4",
        )

        assert action.direction == Direction.VECTOR
        assert action.value == "10;20;-30"

    def test_in_node_load_with_action_type(self) -> None:
        """Test in-node load with action type specified."""
        action = StructuralPointAction(
            name="F5",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N5",
            action_type="Wind",
        )

        assert action.action_type == "Wind"

    def test_in_node_load_with_id(self) -> None:
        """Test in-node load with UUID id."""
        uuid = "550e8400-e29b-41d4-a716-446655440000"
        action = StructuralPointAction(
            name="F6",
            direction=Direction.X,
            force_action=ForceAction.IN_NODE,
            value="30",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N6",
            id=uuid,
        )

        assert action.id == uuid

    # Valid Initialization Tests - On Beam Loads

    def test_on_beam_load_single_at_start(self) -> None:
        """Test point load on beam at start (single)."""
        action = StructuralPointAction(
            name="F7",
            direction=Direction.Z,
            force_action=ForceAction.ON_BEAM,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B1",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=0.0,
        )

        assert action.force_action == ForceAction.ON_BEAM
        assert action.origin == Origin.FROM_START
        assert action.position == 0.0

    def test_on_beam_load_from_end(self) -> None:
        """Test point load on beam measured from end."""
        action = StructuralPointAction(
            name="F8",
            direction=Direction.Y,
            force_action=ForceAction.ON_BEAM,
            value="25",
            load_case="LC1",
            coordinate_system=CoordinateSystem.LOCAL,
            reference_member="B2",
            origin=Origin.FROM_END,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=1.5,
        )

        assert action.origin == Origin.FROM_END
        assert action.coordinate_system == CoordinateSystem.LOCAL

    def test_on_beam_load_relative_position(self) -> None:
        """Test point load on beam with relative position."""
        action = StructuralPointAction(
            name="F9",
            direction=Direction.X,
            force_action=ForceAction.ON_BEAM,
            value="20",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B3",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            position=0.5,
        )

        assert action.coordinate_definition == CoordinateDefinition.RELATIVE

    def test_on_beam_load_vector_direction(self) -> None:
        """Test point load on beam with vector direction."""
        action = StructuralPointAction(
            name="F10",
            direction=Direction.VECTOR,
            force_action=ForceAction.ON_BEAM,
            value="5;10;-15",
            load_case="LC1",
            coordinate_system=CoordinateSystem.LOCAL,
            reference_member="B4",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=2.0,
        )

        assert action.direction == Direction.VECTOR

    def test_on_beam_load_repeated_single_load(self) -> None:
        """Test repeated point loads on beam (default repeat=1)."""
        action = StructuralPointAction(
            name="F11",
            direction=Direction.Z,
            force_action=ForceAction.ON_BEAM,
            value="-30",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B5",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=1.0,
            repeat=1,
        )

        assert action.repeat == 1

    def test_on_beam_load_repeated_multiple(self) -> None:
        """Test multiple repeated point loads on beam."""
        action = StructuralPointAction(
            name="F12",
            direction=Direction.Z,
            force_action=ForceAction.ON_BEAM,
            value="-20",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B6",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=0.0,
            repeat=5,
            delta=2.0,
        )

        assert action.repeat == 5
        assert action.delta == 2.0

    def test_on_beam_load_with_action_type(self) -> None:
        """Test on-beam load with action type."""
        action = StructuralPointAction(
            name="F13",
            direction=Direction.Z,
            force_action=ForceAction.ON_BEAM,
            value="-25",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B7",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=1.5,
            action_type="Snow",
        )

        assert action.action_type == "Snow"

    # Validation Tests - Direction and Value Format

    def test_vector_direction_requires_semicolon_format(self) -> None:
        """Test that Vector direction requires X;Y;Z format."""
        with pytest.raises(
            ValueError,
            match=r"value must be in 'X;Y;Z' format for Vector direction",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.VECTOR,
                force_action=ForceAction.IN_NODE,
                value="10",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_node="N1",
            )

    def test_single_axis_direction_rejects_vector_format(self) -> None:
        """Test that X/Y/Z directions reject vector format."""
        with pytest.raises(
            ValueError,
            match=r"value must be a single numeric value",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.X,
                force_action=ForceAction.IN_NODE,
                value="10;20;30",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_node="N1",
            )

    def test_y_direction_rejects_vector_format(self) -> None:
        """Test that Y direction rejects vector format."""
        with pytest.raises(
            ValueError,
            match=r"value must be a single numeric value",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.Y,
                force_action=ForceAction.IN_NODE,
                value="5;10;15",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_node="N1",
            )

    # Validation Tests - In Node Requirements

    def test_in_node_without_reference_node_raises_error(self) -> None:
        """Test that IN_NODE without reference_node raises error."""
        with pytest.raises(
            ValueError,
            match=r"reference_node must be specified when force_action = ForceAction.IN_NODE",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.Z,
                force_action=ForceAction.IN_NODE,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
            )

    def test_in_node_with_empty_reference_node_raises_error(self) -> None:
        """Test that IN_NODE with empty reference_node raises error."""
        with pytest.raises(
            ValueError,
            match=r"reference_node must be specified when force_action = ForceAction.IN_NODE",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.Z,
                force_action=ForceAction.IN_NODE,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_node="",
            )

    # Validation Tests - On Beam Requirements

    def test_on_beam_without_reference_member_raises_error(self) -> None:
        """Test that ON_BEAM without reference_member raises error."""
        with pytest.raises(
            ValueError,
            match=r"reference_member must be specified when force_action = ForceAction.ON_BEAM",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.Z,
                force_action=ForceAction.ON_BEAM,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                position=1.0,
            )

    def test_on_beam_without_origin_raises_error(self) -> None:
        """Test that ON_BEAM without origin raises error."""
        with pytest.raises(
            ValueError,
            match=r"origin must be specified when force_action = ForceAction.ON_BEAM",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.Z,
                force_action=ForceAction.ON_BEAM,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="B1",
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                position=1.0,
            )

    def test_on_beam_without_coordinate_definition_raises_error(self) -> None:
        """Test that ON_BEAM without coordinate_definition raises error."""
        with pytest.raises(
            ValueError,
            match=r"coordinate_definition must be specified when force_action = ForceAction.ON_BEAM",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.Z,
                force_action=ForceAction.ON_BEAM,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="B1",
                origin=Origin.FROM_START,
                position=1.0,
            )

    def test_on_beam_without_position_raises_error(self) -> None:
        """Test that ON_BEAM without position raises error."""
        with pytest.raises(
            ValueError,
            match=r"position must be specified when force_action = ForceAction.ON_BEAM",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.Z,
                force_action=ForceAction.ON_BEAM,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="B1",
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
            )

    # Validation Tests - Repeat and Delta

    def test_negative_repeat_raises_error(self) -> None:
        """Test that negative repeat count raises error."""
        with pytest.raises(
            ValueError,
            match=r"repeat must be >= 0",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.Z,
                force_action=ForceAction.IN_NODE,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_node="N1",
                repeat=-1,
            )

    def test_repeat_greater_than_one_requires_delta(self) -> None:
        """Test that repeat > 1 requires delta to be specified."""
        with pytest.raises(
            ValueError,
            match=r"delta must be specified when repeat > 1",
        ):
            StructuralPointAction(
                name="F_INVALID",
                direction=Direction.Z,
                force_action=ForceAction.ON_BEAM,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="B1",
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                position=0.0,
                repeat=3,
            )

    # Edge Cases and Properties

    def test_action_equality(self) -> None:
        """Test that two actions with same values are equal."""
        action1 = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        action2 = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )

        assert action1 == action2

    def test_action_inequality(self) -> None:
        """Test that actions with different values are not equal."""
        action1 = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        action2 = StructuralPointAction(
            name="F2",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )

        assert action1 != action2

    def test_action_hashable(self) -> None:
        """Test that actions are hashable (can be used in sets/dicts)."""
        action1 = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        action2 = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )

        action_set = {action1, action2}
        assert len(action_set) == 1

    def test_action_frozen(self) -> None:
        """Test that action is immutable (frozen)."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )

        with pytest.raises(AttributeError):
            action.name = "F2"

    def test_action_type_optional(self) -> None:
        """Test that action_type is optional."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )

        assert action.action_type == ""

    def test_id_optional(self) -> None:
        """Test that id is optional."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )

        assert action.id == ""

    def test_delta_optional_when_repeat_is_one(self) -> None:
        """Test that delta is optional when repeat = 1."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
            repeat=1,
        )

        assert action.delta is None

    # Comprehensive Enum Tests

    def test_all_direction_values(self) -> None:
        """Test that all Direction enum values work."""
        for direction in Direction:
            if direction == Direction.VECTOR:
                value = "10;20;30"
            else:
                value = "50"

            action = StructuralPointAction(
                name="F_TEST",
                direction=direction,
                force_action=ForceAction.IN_NODE,
                value=value,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_node="N1",
            )
            assert action.direction == direction

    def test_all_coordinate_system_values(self) -> None:
        """Test that all CoordinateSystem enum values work."""
        for coord_sys in CoordinateSystem:
            action = StructuralPointAction(
                name="F_TEST",
                direction=Direction.Z,
                force_action=ForceAction.IN_NODE,
                value="-50",
                load_case="LC1",
                coordinate_system=coord_sys,
                reference_node="N1",
            )
            assert action.coordinate_system == coord_sys

    def test_all_origin_values_on_beam(self) -> None:
        """Test that all Origin enum values work on beam."""
        for origin in Origin:
            action = StructuralPointAction(
                name="F_TEST",
                direction=Direction.Z,
                force_action=ForceAction.ON_BEAM,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="B1",
                origin=origin,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                position=1.0,
            )
            assert action.origin == origin

    def test_all_coordinate_definition_values_on_beam(self) -> None:
        """Test that all CoordinateDefinition enum values work on beam."""
        for coord_def in CoordinateDefinition:
            action = StructuralPointAction(
                name="F_TEST",
                direction=Direction.Z,
                force_action=ForceAction.ON_BEAM,
                value="-50",
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="B1",
                origin=Origin.FROM_START,
                coordinate_definition=coord_def,
                position=1.0,
            )
            assert action.coordinate_definition == coord_def

    # Additional Edge Cases

    def test_zero_position_on_beam(self) -> None:
        """Test load at start of beam (position=0)."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.ON_BEAM,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B1",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=0.0,
        )

        assert action.position == 0.0

    def test_relative_position_as_percentage(self) -> None:
        """Test relative position specified as percentage (0-1)."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.ON_BEAM,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B1",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            position=0.75,
        )

        assert action.position == 0.75

    def test_large_repeat_count(self) -> None:
        """Test with large repeat count."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.ON_BEAM,
            value="-10",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B1",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=0.0,
            repeat=100,
            delta=0.5,
        )

        assert action.repeat == 100
        assert action.delta == 0.5

    def test_negative_load_value(self) -> None:
        """Test with negative load value (downward load)."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-250.75",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )

        assert action.value == "-250.75"

    def test_vector_with_negative_components(self) -> None:
        """Test vector with negative components."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.VECTOR,
            force_action=ForceAction.IN_NODE,
            value="-10;-20;-30",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )

        assert action.value == "-10;-20;-30"

    def test_repeat_zero_for_single_load(self) -> None:
        """Test repeat=0 for single load."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.IN_NODE,
            value="-50",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
            repeat=0,
        )

        assert action.repeat == 0

    def test_fractional_delta(self) -> None:
        """Test with fractional delta spacing."""
        action = StructuralPointAction(
            name="F1",
            direction=Direction.Z,
            force_action=ForceAction.ON_BEAM,
            value="-20",
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B1",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=0.0,
            repeat=10,
            delta=0.25,
        )

        assert action.delta == 0.25
