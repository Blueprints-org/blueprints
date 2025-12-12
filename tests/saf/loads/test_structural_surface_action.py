"""Tests for StructuralSurfaceAction dataclass.

Comprehensive test suite covering initialization, validation, and immutability
of the StructuralSurfaceAction class following SAF specification.
"""

import pytest

from blueprints.saf.loads.structural_surface_action import (
    CoordinateSystem,
    Direction,
    ForceAction,
    Location,
    StructuralSurfaceAction,
)


class TestStructuralSurfaceActionValidInitialization:
    """Tests for valid StructuralSurfaceAction initialization."""

    def test_load_on_2d_member_z_direction(self) -> None:
        """Test surface load on 2D member in Z direction."""
        load = StructuralSurfaceAction(
            name="PF1",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        assert load.name == "PF1"
        assert load.direction == Direction.Z
        assert load.force_action == ForceAction.ON_2D_MEMBER
        assert load.value == -10.0
        assert load.two_d_member == "S1"

    def test_load_on_2d_member_x_direction(self) -> None:
        """Test surface load on 2D member in X direction."""
        load = StructuralSurfaceAction(
            name="PF2",
            direction=Direction.X,
            force_action=ForceAction.ON_2D_MEMBER,
            value=5.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S2",
        )
        assert load.direction == Direction.X
        assert load.value == 5.0

    def test_load_on_2d_member_y_direction(self) -> None:
        """Test surface load on 2D member in Y direction."""
        load = StructuralSurfaceAction(
            name="PF3",
            direction=Direction.Y,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-8.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S3",
        )
        assert load.direction == Direction.Y

    def test_load_on_2d_member_region(self) -> None:
        """Test surface load on 2D member region."""
        load = StructuralSurfaceAction(
            name="PF4",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER_REGION,
            value=-15.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member_region="R1",
        )
        assert load.force_action == ForceAction.ON_2D_MEMBER_REGION
        assert load.two_d_member_region == "R1"

    def test_load_on_2d_member_distribution(self) -> None:
        """Test surface load on 2D member distribution."""
        load = StructuralSurfaceAction(
            name="PF5",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER_DISTRIBUTION,
            value=-12.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member_distribution="D1",
        )
        assert load.force_action == ForceAction.ON_2D_MEMBER_DISTRIBUTION
        assert load.two_d_member_distribution == "D1"

    def test_load_with_projection_location(self) -> None:
        """Test surface load with PROJECTION location (for inclined surfaces)."""
        load = StructuralSurfaceAction(
            name="PF6",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.PROJECTION,
            two_d_member="S1",
        )
        assert load.location == Location.PROJECTION

    def test_load_with_local_coordinate_system(self) -> None:
        """Test surface load with local coordinate system."""
        load = StructuralSurfaceAction(
            name="PF7",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.LOCAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        assert load.coordinate_system == CoordinateSystem.LOCAL

    def test_load_with_action_type(self) -> None:
        """Test surface load with action type."""
        load = StructuralSurfaceAction(
            name="PF8",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
            action_type="Wind",
        )
        assert load.action_type == "Wind"

    def test_load_with_uuid(self) -> None:
        """Test surface load with UUID identifier."""
        load = StructuralSurfaceAction(
            name="PF9",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
            id="550e8400-e29b-41d4-a716-446655440000",
        )
        assert load.id == "550e8400-e29b-41d4-a716-446655440000"

    def test_positive_load_value(self) -> None:
        """Test surface load with positive value."""
        load = StructuralSurfaceAction(
            name="PF10",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=25.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        assert load.value == 25.0

    def test_zero_load_value(self) -> None:
        """Test surface load with zero value."""
        load = StructuralSurfaceAction(
            name="PF11",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=0.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        assert load.value == 0.0


class TestStructuralSurfaceActionValidation:
    """Tests for StructuralSurfaceAction validation."""

    def test_on_2d_member_requires_two_d_member(self) -> None:
        """Test that ON_2D_MEMBER requires two_d_member."""
        with pytest.raises(ValueError, match="two_d_member must be specified"):
            StructuralSurfaceAction(
                name="PF1",
                direction=Direction.Z,
                force_action=ForceAction.ON_2D_MEMBER,
                value=-10.0,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
            )

    def test_on_2d_member_region_requires_region(self) -> None:
        """Test that ON_2D_MEMBER_REGION requires two_d_member_region."""
        with pytest.raises(ValueError, match="two_d_member_region must be specified"):
            StructuralSurfaceAction(
                name="PF1",
                direction=Direction.Z,
                force_action=ForceAction.ON_2D_MEMBER_REGION,
                value=-10.0,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
            )

    def test_on_2d_member_distribution_requires_distribution(self) -> None:
        """Test that ON_2D_MEMBER_DISTRIBUTION requires two_d_member_distribution."""
        with pytest.raises(ValueError, match="two_d_member_distribution must be specified"):
            StructuralSurfaceAction(
                name="PF1",
                direction=Direction.Z,
                force_action=ForceAction.ON_2D_MEMBER_DISTRIBUTION,
                value=-10.0,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
            )


class TestStructuralSurfaceActionEquality:
    """Tests for StructuralSurfaceAction equality."""

    def test_equal_loads_with_same_attributes(self) -> None:
        """Test that loads with same attributes are equal."""
        load1 = StructuralSurfaceAction(
            name="PF1",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        load2 = StructuralSurfaceAction(
            name="PF1",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        assert load1 == load2

    def test_unequal_loads_different_values(self) -> None:
        """Test that loads with different values are not equal."""
        load1 = StructuralSurfaceAction(
            name="PF1",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        load2 = StructuralSurfaceAction(
            name="PF1",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-20.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        assert load1 != load2

    def test_hashable_loads(self) -> None:
        """Test that loads are hashable (can be used in sets/dicts)."""
        load = StructuralSurfaceAction(
            name="PF1",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        load_set = {load}
        assert load in load_set

    def test_frozen_immutability(self) -> None:
        """Test that load instances are frozen (immutable)."""
        load = StructuralSurfaceAction(
            name="PF1",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=-10.0,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        with pytest.raises(AttributeError):
            load.value = -20.0  # type: ignore


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

    def test_all_directions_exist(self) -> None:
        """Test that all directions are defined."""
        directions = list(Direction)
        assert len(directions) == 3


class TestForceActionEnum:
    """Tests for ForceAction enum."""

    def test_on_2d_member_action(self) -> None:
        """Test ON_2D_MEMBER action."""
        assert ForceAction.ON_2D_MEMBER.value == "On 2D member"

    def test_on_2d_member_region_action(self) -> None:
        """Test ON_2D_MEMBER_REGION action."""
        assert ForceAction.ON_2D_MEMBER_REGION.value == "On 2D member region"

    def test_on_2d_member_distribution_action(self) -> None:
        """Test ON_2D_MEMBER_DISTRIBUTION action."""
        assert ForceAction.ON_2D_MEMBER_DISTRIBUTION.value == "On 2D member distribution"

    def test_all_force_actions_exist(self) -> None:
        """Test that all force actions are defined."""
        actions = list(ForceAction)
        assert len(actions) == 3


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


class TestLocationEnum:
    """Tests for Location enum."""

    def test_length_location(self) -> None:
        """Test LENGTH location."""
        assert Location.LENGTH.value == "Length"

    def test_projection_location(self) -> None:
        """Test PROJECTION location."""
        assert Location.PROJECTION.value == "Projection"

    def test_all_locations_exist(self) -> None:
        """Test that all locations are defined."""
        locations = list(Location)
        assert len(locations) == 2


class TestStructuralSurfaceActionEdgeCases:
    """Tests for StructuralSurfaceAction edge cases."""

    def test_very_large_load_value(self) -> None:
        """Test load with very large value."""
        load = StructuralSurfaceAction(
            name="PF1",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=1e10,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        assert load.value == 1e10

    def test_very_small_load_value(self) -> None:
        """Test load with very small value."""
        load = StructuralSurfaceAction(
            name="PF1",
            direction=Direction.Z,
            force_action=ForceAction.ON_2D_MEMBER,
            value=1e-10,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            two_d_member="S1",
        )
        assert load.value == 1e-10

    def test_all_directions_with_all_force_actions(self) -> None:
        """Test all direction and force action combinations."""
        for direction in Direction:
            for force_action in ForceAction:
                if force_action == ForceAction.ON_2D_MEMBER:
                    load = StructuralSurfaceAction(
                        name="PF1",
                        direction=direction,
                        force_action=force_action,
                        value=-10.0,
                        load_case="LC1",
                        coordinate_system=CoordinateSystem.GLOBAL,
                        location=Location.LENGTH,
                        two_d_member="S1",
                    )
                    assert load.direction == direction
                    assert load.force_action == force_action
