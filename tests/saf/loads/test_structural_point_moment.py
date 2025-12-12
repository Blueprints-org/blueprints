"""Tests for StructuralPointMoment dataclass.

Comprehensive test suite covering initialization, validation, and immutability
of the StructuralPointMoment class following SAF specification.
"""

import pytest

from blueprints.saf.loads.structural_point_moment import (
    CoordinateDefinition,
    CoordinateSystem,
    ForceAction,
    MomentDirection,
    Origin,
    StructuralPointMoment,
)


class TestStructuralPointMomentValidInitialization:
    """Tests for valid StructuralPointMoment initialization."""

    def test_moment_at_node_mx_direction(self) -> None:
        """Test moment at node in Mx direction."""
        moment = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MX,
            force_action=ForceAction.IN_NODE,
            value=10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        assert moment.name == "M1"
        assert moment.direction == MomentDirection.MX
        assert moment.force_action == ForceAction.IN_NODE
        assert moment.value == 10.0
        assert moment.reference_node == "N1"

    def test_moment_at_node_my_direction(self) -> None:
        """Test moment at node in My direction."""
        moment = StructuralPointMoment(
            name="M2",
            direction=MomentDirection.MY,
            force_action=ForceAction.IN_NODE,
            value=15.5,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N2",
        )
        assert moment.direction == MomentDirection.MY
        assert moment.value == 15.5

    def test_moment_at_node_mz_direction(self) -> None:
        """Test moment at node in Mz direction."""
        moment = StructuralPointMoment(
            name="M3",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=20.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N3",
        )
        assert moment.direction == MomentDirection.MZ

    def test_moment_on_beam_from_start(self) -> None:
        """Test moment on beam from start."""
        moment = StructuralPointMoment(
            name="M4",
            direction=MomentDirection.MZ,
            force_action=ForceAction.ON_BEAM,
            value=25.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B1",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=2.5,
        )
        assert moment.force_action == ForceAction.ON_BEAM
        assert moment.reference_member == "B1"
        assert moment.origin == Origin.FROM_START
        assert moment.position == 2.5

    def test_moment_on_beam_from_end(self) -> None:
        """Test moment on beam from end."""
        moment = StructuralPointMoment(
            name="M5",
            direction=MomentDirection.MY,
            force_action=ForceAction.ON_BEAM,
            value=30.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.LOCAL,
            reference_member="B2",
            origin=Origin.FROM_END,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=1.5,
        )
        assert moment.origin == Origin.FROM_END
        assert moment.coordinate_system == CoordinateSystem.LOCAL

    def test_moment_on_beam_relative_position(self) -> None:
        """Test moment on beam with relative position."""
        moment = StructuralPointMoment(
            name="M6",
            direction=MomentDirection.MX,
            force_action=ForceAction.ON_BEAM,
            value=18.0,
            load_case="LC2",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B3",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            position=0.5,  # 50% of member
        )
        assert moment.coordinate_definition == CoordinateDefinition.RELATIVE
        assert moment.position == 0.5

    def test_moment_with_action_type(self) -> None:
        """Test moment with action type specified."""
        moment = StructuralPointMoment(
            name="M7",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=12.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
            action_type="Wind",
        )
        assert moment.action_type == "Wind"

    def test_moment_with_id(self) -> None:
        """Test moment with UUID identifier."""
        moment = StructuralPointMoment(
            name="M8",
            direction=MomentDirection.MY,
            force_action=ForceAction.IN_NODE,
            value=22.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N2",
            id="550e8400-e29b-41d4-a716-446655440000",
        )
        assert moment.id == "550e8400-e29b-41d4-a716-446655440000"

    def test_negative_moment_value(self) -> None:
        """Test moment with negative value."""
        moment = StructuralPointMoment(
            name="M9",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=-50.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        assert moment.value == -50.0

    def test_zero_moment_value(self) -> None:
        """Test moment with zero value."""
        moment = StructuralPointMoment(
            name="M10",
            direction=MomentDirection.MX,
            force_action=ForceAction.IN_NODE,
            value=0.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        assert moment.value == 0.0


class TestStructuralPointMomentValidation:
    """Tests for StructuralPointMoment validation."""

    def test_in_node_requires_reference_node(self) -> None:
        """Test that IN_NODE force action requires reference_node."""
        with pytest.raises(ValueError, match="reference_node must be specified"):
            StructuralPointMoment(
                name="M1",
                direction=MomentDirection.MZ,
                force_action=ForceAction.IN_NODE,
                value=10.0,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_node="",
            )

    def test_on_beam_requires_reference_member(self) -> None:
        """Test that ON_BEAM force action requires reference_member."""
        with pytest.raises(ValueError, match="reference_member must be specified"):
            StructuralPointMoment(
                name="M1",
                direction=MomentDirection.MZ,
                force_action=ForceAction.ON_BEAM,
                value=10.0,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="",
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                position=1.0,
            )

    def test_on_beam_requires_origin(self) -> None:
        """Test that ON_BEAM force action requires origin."""
        with pytest.raises(ValueError, match="origin must be specified"):
            StructuralPointMoment(
                name="M1",
                direction=MomentDirection.MZ,
                force_action=ForceAction.ON_BEAM,
                value=10.0,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="B1",
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                position=1.0,
            )

    def test_on_beam_requires_coordinate_definition(self) -> None:
        """Test that ON_BEAM force action requires coordinate_definition."""
        with pytest.raises(ValueError, match="coordinate_definition must be specified"):
            StructuralPointMoment(
                name="M1",
                direction=MomentDirection.MZ,
                force_action=ForceAction.ON_BEAM,
                value=10.0,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="B1",
                origin=Origin.FROM_START,
                position=1.0,
            )

    def test_on_beam_requires_position(self) -> None:
        """Test that ON_BEAM force action requires position."""
        with pytest.raises(ValueError, match="position must be specified"):
            StructuralPointMoment(
                name="M1",
                direction=MomentDirection.MZ,
                force_action=ForceAction.ON_BEAM,
                value=10.0,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                reference_member="B1",
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
            )


class TestStructuralPointMomentEquality:
    """Tests for StructuralPointMoment equality and hashability."""

    def test_equal_moments_with_same_attributes(self) -> None:
        """Test that moments with same attributes are equal."""
        m1 = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        m2 = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        assert m1 == m2

    def test_unequal_moments_different_values(self) -> None:
        """Test that moments with different values are not equal."""
        m1 = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        m2 = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=20.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        assert m1 != m2

    def test_hashable_moments(self) -> None:
        """Test that moments are hashable (can be used in sets/dicts)."""
        m1 = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        moment_set = {m1}
        assert m1 in moment_set

    def test_frozen_immutability(self) -> None:
        """Test that moment instances are frozen (immutable)."""
        moment = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        with pytest.raises(AttributeError):
            moment.value = 20.0  # type: ignore[misc]


class TestMomentDirectionEnum:
    """Tests for MomentDirection enum."""

    def test_mx_direction(self) -> None:
        """Test Mx moment direction."""
        assert MomentDirection.MX.value == "Mx"

    def test_my_direction(self) -> None:
        """Test My moment direction."""
        assert MomentDirection.MY.value == "My"

    def test_mz_direction(self) -> None:
        """Test Mz moment direction."""
        assert MomentDirection.MZ.value == "Mz"

    def test_all_directions_exist(self) -> None:
        """Test that all moment directions are defined."""
        directions = list(MomentDirection)
        assert len(directions) == 3
        assert MomentDirection.MX in directions
        assert MomentDirection.MY in directions
        assert MomentDirection.MZ in directions


class TestForceActionEnum:
    """Tests for ForceAction enum."""

    def test_in_node_action(self) -> None:
        """Test IN_NODE force action."""
        assert ForceAction.IN_NODE.value == "In node"

    def test_on_beam_action(self) -> None:
        """Test ON_BEAM force action."""
        assert ForceAction.ON_BEAM.value == "On beam"

    def test_all_actions_exist(self) -> None:
        """Test that all force actions are defined."""
        actions = list(ForceAction)
        assert len(actions) == 2


class TestCoordinateSystemEnum:
    """Tests for CoordinateSystem enum."""

    def test_global_system(self) -> None:
        """Test GLOBAL coordinate system."""
        assert CoordinateSystem.GLOBAL.value == "Global"

    def test_local_system(self) -> None:
        """Test LOCAL coordinate system."""
        assert CoordinateSystem.LOCAL.value == "Local"

    def test_all_systems_exist(self) -> None:
        """Test that all coordinate systems are defined."""
        systems = list(CoordinateSystem)
        assert len(systems) == 2


class TestOriginEnum:
    """Tests for Origin enum."""

    def test_from_start_origin(self) -> None:
        """Test FROM_START origin."""
        assert Origin.FROM_START.value == "From start"

    def test_from_end_origin(self) -> None:
        """Test FROM_END origin."""
        assert Origin.FROM_END.value == "From end"

    def test_all_origins_exist(self) -> None:
        """Test that all origins are defined."""
        origins = list(Origin)
        assert len(origins) == 2


class TestCoordinateDefinitionEnum:
    """Tests for CoordinateDefinition enum."""

    def test_absolute_definition(self) -> None:
        """Test ABSOLUTE coordinate definition."""
        assert CoordinateDefinition.ABSOLUTE.value == "Absolute"

    def test_relative_definition(self) -> None:
        """Test RELATIVE coordinate definition."""
        assert CoordinateDefinition.RELATIVE.value == "Relative"

    def test_all_definitions_exist(self) -> None:
        """Test that all coordinate definitions are defined."""
        definitions = list(CoordinateDefinition)
        assert len(definitions) == 2


class TestStructuralPointMomentEdgeCases:
    """Tests for StructuralPointMoment edge cases."""

    def test_very_large_moment_value(self) -> None:
        """Test moment with very large value."""
        moment = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=1e10,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        assert moment.value == 1e10

    def test_very_small_moment_value(self) -> None:
        """Test moment with very small value."""
        moment = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.IN_NODE,
            value=1e-10,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_node="N1",
        )
        assert moment.value == 1e-10

    def test_fractional_position_on_beam(self) -> None:
        """Test moment on beam with fractional position."""
        moment = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.ON_BEAM,
            value=15.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B1",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=2.75,
        )
        assert moment.position == 2.75

    def test_zero_position_on_beam(self) -> None:
        """Test moment on beam at zero position."""
        moment = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.ON_BEAM,
            value=15.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B1",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position=0.0,
        )
        assert moment.position == 0.0

    def test_relative_position_at_1_0(self) -> None:
        """Test moment on beam with relative position at 1.0 (end)."""
        moment = StructuralPointMoment(
            name="M1",
            direction=MomentDirection.MZ,
            force_action=ForceAction.ON_BEAM,
            value=15.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            reference_member="B1",
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            position=1.0,
        )
        assert moment.position == 1.0
