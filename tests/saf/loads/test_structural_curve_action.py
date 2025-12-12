"""Tests for StructuralCurveAction dataclass.

Comprehensive test suite covering initialization, validation, and immutability
of the StructuralCurveAction class following SAF specification.
"""

import pytest

from blueprints.saf.loads.structural_curve_action import (
    CoordinateDefinition,
    CoordinateSystem,
    Direction,
    Distribution,
    Extent,
    ForceAction,
    Location,
    Origin,
    StructuralCurveAction,
)


class TestStructuralCurveActionValidInitialization:
    """Tests for valid StructuralCurveAction initialization."""

    def test_uniform_load_on_beam(self) -> None:
        """Test uniform line load on beam."""
        load = StructuralCurveAction(
            name="F1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-50.0,
            member="B1",
        )
        assert load.name == "F1"
        assert load.force_action == ForceAction.ON_BEAM
        assert load.distribution == Distribution.UNIFORM
        assert load.direction == Direction.Z
        assert load.value_1 == -50.0

    def test_trapezoidal_load_on_beam(self) -> None:
        """Test trapezoidal line load on beam."""
        load = StructuralCurveAction(
            name="F2",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.TRAPEZ,
            direction=Direction.X,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=4.0,
            value_1=-100.0,
            value_2=-150.0,
            member="B2",
        )
        assert load.value_1 == -100.0
        assert load.value_2 == -150.0

    def test_load_on_2d_edge(self) -> None:
        """Test load on 2D member edge."""
        load = StructuralCurveAction(
            name="F3",
            force_action=ForceAction.ON_EDGE,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-75.0,
            two_d_member="S1",
            edge=1,
        )
        assert load.two_d_member == "S1"
        assert load.edge == 1

    def test_load_on_rib(self) -> None:
        """Test load on rib."""
        load = StructuralCurveAction(
            name="F4",
            force_action=ForceAction.ON_RIB,
            distribution=Distribution.UNIFORM,
            direction=Direction.Y,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=3.0,
            value_1=-40.0,
            member_rib="R1",
        )
        assert load.member_rib == "R1"

    def test_load_on_subregion_edge(self) -> None:
        """Test load on subregion edge."""
        load = StructuralCurveAction(
            name="F5",
            force_action=ForceAction.ON_SUBREGION_EDGE,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-60.0,
            two_d_member="S1",
            two_d_member_region="R1",
            edge=2,
        )
        assert load.two_d_member_region == "R1"

    def test_load_on_opening_edge(self) -> None:
        """Test load on opening edge."""
        load = StructuralCurveAction(
            name="F6",
            force_action=ForceAction.ON_OPENING_EDGE,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=3.0,
            value_1=-80.0,
            two_d_member="S1",
            two_d_member_opening="O1",
            edge=1,
        )
        assert load.two_d_member_opening == "O1"

    def test_load_on_internal_edge(self) -> None:
        """Test load on internal edge."""
        load = StructuralCurveAction(
            name="F7",
            force_action=ForceAction.ON_INTERNAL_EDGE,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=4.0,
            value_1=-70.0,
            internal_edge="IE1",
        )
        assert load.internal_edge == "IE1"

    def test_vector_direction_uniform(self) -> None:
        """Test vector direction with uniform distribution."""
        load = StructuralCurveAction(
            name="F8",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.VECTOR,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            vector_1="10;20;-50",
            member="B1",
        )
        assert load.vector_1 == "10;20;-50"

    def test_vector_direction_trapezoidal(self) -> None:
        """Test vector direction with trapezoidal distribution."""
        load = StructuralCurveAction(
            name="F9",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.TRAPEZ,
            direction=Direction.VECTOR,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            vector_1="10;20;-50",
            vector_2="15;25;-75",
            member="B1",
        )
        assert load.vector_1 == "10;20;-50"
        assert load.vector_2 == "15;25;-75"

    def test_relative_positions(self) -> None:
        """Test load with relative positions."""
        load = StructuralCurveAction(
            name="F10",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.2,
            end_point=0.8,
            value_1=-50.0,
            member="B1",
        )
        assert load.start_point == 0.2
        assert load.end_point == 0.8

    def test_with_eccentricity(self) -> None:
        """Test load with eccentricity offsets."""
        load = StructuralCurveAction(
            name="F11",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-50.0,
            member="B1",
            eccentricity_ey=-150.0,
            eccentricity_ez=75.0,
        )
        assert load.eccentricity_ey == -150.0
        assert load.eccentricity_ez == 75.0

    def test_with_action_type(self) -> None:
        """Test load with action type."""
        load = StructuralCurveAction(
            name="F12",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-50.0,
            member="B1",
            action_type="Wind",
        )
        assert load.action_type == "Wind"

    def test_local_coordinate_system(self) -> None:
        """Test load with local coordinate system."""
        load = StructuralCurveAction(
            name="F13",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.LOCAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-50.0,
            member="B1",
        )
        assert load.coordinate_system == CoordinateSystem.LOCAL

    def test_from_end_origin(self) -> None:
        """Test load with FROM_END origin."""
        load = StructuralCurveAction(
            name="F14",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_END,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=2.5,
            value_1=-50.0,
            member="B1",
        )
        assert load.origin == Origin.FROM_END


class TestStructuralCurveActionValidation:
    """Tests for StructuralCurveAction validation."""

    def test_vector_direction_requires_vector_1(self) -> None:
        """Test that VECTOR direction requires vector_1."""
        with pytest.raises(ValueError, match="vector_1 must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_BEAM,
                distribution=Distribution.UNIFORM,
                direction=Direction.VECTOR,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                member="B1",
            )

    def test_vector_format_validation(self) -> None:
        """Test that vector format must contain semicolons."""
        with pytest.raises(ValueError, match="must be in 'X;Y;Z' format"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_BEAM,
                distribution=Distribution.UNIFORM,
                direction=Direction.VECTOR,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                vector_1="10,20,-50",  # Wrong format
                member="B1",
            )

    def test_single_axis_direction_requires_value_1(self) -> None:
        """Test that single-axis directions require value_1."""
        with pytest.raises(ValueError, match="value_1 must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_BEAM,
                distribution=Distribution.UNIFORM,
                direction=Direction.X,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                member="B1",
            )

    def test_on_beam_requires_member(self) -> None:
        """Test that ON_BEAM force action requires member."""
        with pytest.raises(ValueError, match="member must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_BEAM,
                distribution=Distribution.UNIFORM,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=-50.0,
            )

    def test_on_rib_requires_member_rib(self) -> None:
        """Test that ON_RIB force action requires member_rib."""
        with pytest.raises(ValueError, match="member_rib must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_RIB,
                distribution=Distribution.UNIFORM,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=-50.0,
            )

    def test_on_edge_requires_two_d_member(self) -> None:
        """Test that ON_EDGE requires two_d_member."""
        with pytest.raises(ValueError, match="two_d_member must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_EDGE,
                distribution=Distribution.UNIFORM,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=-50.0,
                edge=1,
            )

    def test_on_edge_requires_edge(self) -> None:
        """Test that ON_EDGE requires edge index."""
        with pytest.raises(ValueError, match="edge must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_EDGE,
                distribution=Distribution.UNIFORM,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=-50.0,
                two_d_member="S1",
            )

    def test_on_subregion_edge_requires_region(self) -> None:
        """Test that ON_SUBREGION_EDGE requires two_d_member_region."""
        with pytest.raises(ValueError, match="two_d_member_region must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_SUBREGION_EDGE,
                distribution=Distribution.UNIFORM,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=-50.0,
                two_d_member="S1",
                edge=1,
            )

    def test_on_opening_edge_requires_opening(self) -> None:
        """Test that ON_OPENING_EDGE requires two_d_member_opening."""
        with pytest.raises(ValueError, match="two_d_member_opening must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_OPENING_EDGE,
                distribution=Distribution.UNIFORM,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=-50.0,
                two_d_member="S1",
                edge=1,
            )

    def test_on_internal_edge_requires_internal_edge(self) -> None:
        """Test that ON_INTERNAL_EDGE requires internal_edge."""
        with pytest.raises(ValueError, match="internal_edge must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_INTERNAL_EDGE,
                distribution=Distribution.UNIFORM,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=-50.0,
            )

    def test_trapez_requires_value_2_for_single_axis(self) -> None:
        """Test that TRAPEZ distribution requires value_2 for single-axis directions."""
        with pytest.raises(ValueError, match="value_2 must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_BEAM,
                distribution=Distribution.TRAPEZ,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=-50.0,
                member="B1",
            )

    def test_trapez_requires_vector_2_for_vector(self) -> None:
        """Test that TRAPEZ distribution requires vector_2 for vector direction."""
        with pytest.raises(ValueError, match="vector_2 must be specified"):
            StructuralCurveAction(
                name="F1",
                force_action=ForceAction.ON_BEAM,
                distribution=Distribution.TRAPEZ,
                direction=Direction.VECTOR,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                vector_1="10;20;-50",
                member="B1",
            )


class TestStructuralCurveActionEquality:
    """Tests for StructuralCurveAction equality."""

    def test_equal_loads_with_same_attributes(self) -> None:
        """Test that loads with same attributes are equal."""
        load1 = StructuralCurveAction(
            name="F1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-50.0,
            member="B1",
        )
        load2 = StructuralCurveAction(
            name="F1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-50.0,
            member="B1",
        )
        assert load1 == load2

    def test_unequal_loads_different_values(self) -> None:
        """Test that loads with different values are not equal."""
        load1 = StructuralCurveAction(
            name="F1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-50.0,
            member="B1",
        )
        load2 = StructuralCurveAction(
            name="F1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-75.0,
            member="B1",
        )
        assert load1 != load2

    def test_frozen_immutability(self) -> None:
        """Test that load instances are frozen (immutable)."""
        load = StructuralCurveAction(
            name="F1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-50.0,
            member="B1",
        )
        with pytest.raises(AttributeError):
            load.value_1 = -75.0  # type: ignore


class TestStructuralCurveActionEdgeCases:
    """Tests for StructuralCurveAction edge cases."""

    def test_very_large_load_value(self) -> None:
        """Test load with very large value."""
        load = StructuralCurveAction(
            name="F1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=-1e10,
            member="B1",
        )
        assert load.value_1 == -1e10

    def test_fractional_positions(self) -> None:
        """Test load with fractional positions."""
        load = StructuralCurveAction(
            name="F1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=1.25,
            end_point=3.75,
            value_1=-50.0,
            member="B1",
        )
        assert load.start_point == 1.25
        assert load.end_point == 3.75

    def test_all_direction_values(self) -> None:
        """Test all direction enum values."""
        directions = list(Direction)
        assert len(directions) == 4
        assert Direction.X in directions
        assert Direction.Y in directions
        assert Direction.Z in directions
        assert Direction.VECTOR in directions

    def test_all_force_action_values(self) -> None:
        """Test all force action enum values."""
        actions = list(ForceAction)
        assert len(actions) == 6

    def test_all_distribution_values(self) -> None:
        """Test all distribution enum values."""
        distributions = list(Distribution)
        assert len(distributions) == 2
        assert Distribution.UNIFORM in distributions
        assert Distribution.TRAPEZ in distributions
