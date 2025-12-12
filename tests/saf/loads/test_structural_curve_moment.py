"""Tests for StructuralCurveMoment dataclass.

Comprehensive test suite covering initialization, validation, and immutability
of the StructuralCurveMoment class following SAF specification.
"""

import pytest

from blueprints.saf.loads.structural_curve_moment import (
    CoordinateDefinition,
    CoordinateSystem,
    Distribution,
    Extent,
    ForceAction,
    Location,
    MomentDirection,
    Origin,
    StructuralCurveMoment,
)


class TestStructuralCurveMomentValidInitialization:
    """Tests for valid StructuralCurveMoment initialization."""

    def test_uniform_moment_on_beam_mx(self) -> None:
        """Test uniform line moment on beam in Mx direction."""
        moment = StructuralCurveMoment(
            name="LM1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MX,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=10.0,
            member="B1",
        )
        assert moment.name == "LM1"
        assert moment.direction == MomentDirection.MX
        assert moment.value_1 == 10.0

    def test_uniform_moment_on_beam_my(self) -> None:
        """Test uniform line moment on beam in My direction."""
        moment = StructuralCurveMoment(
            name="LM2",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MY,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=15.0,
            member="B1",
        )
        assert moment.direction == MomentDirection.MY

    def test_uniform_moment_on_beam_mz(self) -> None:
        """Test uniform line moment on beam in Mz direction."""
        moment = StructuralCurveMoment(
            name="LM3",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=20.0,
            member="B1",
        )
        assert moment.direction == MomentDirection.MZ

    def test_trapezoidal_moment_on_beam(self) -> None:
        """Test trapezoidal line moment on beam."""
        moment = StructuralCurveMoment(
            name="LM4",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.TRAPEZ,
            direction=MomentDirection.MY,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=4.0,
            value_1=10.0,
            value_2=20.0,
            member="B1",
        )
        assert moment.value_1 == 10.0
        assert moment.value_2 == 20.0

    def test_moment_on_2d_edge(self) -> None:
        """Test moment on 2D member edge."""
        moment = StructuralCurveMoment(
            name="LM5",
            force_action=ForceAction.ON_EDGE,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=12.0,
            two_d_member="S1",
            edge=1,
        )
        assert moment.two_d_member == "S1"
        assert moment.edge == 1

    def test_moment_on_rib(self) -> None:
        """Test moment on rib."""
        moment = StructuralCurveMoment(
            name="LM6",
            force_action=ForceAction.ON_RIB,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MX,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=3.0,
            value_1=8.0,
            member_rib="R1",
        )
        assert moment.member_rib == "R1"

    def test_moment_on_subregion_edge(self) -> None:
        """Test moment on subregion edge."""
        moment = StructuralCurveMoment(
            name="LM7",
            force_action=ForceAction.ON_SUBREGION_EDGE,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MY,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=14.0,
            two_d_member="S1",
            two_d_member_region="R1",
            edge=2,
        )
        assert moment.two_d_member_region == "R1"

    def test_moment_on_opening_edge(self) -> None:
        """Test moment on opening edge."""
        moment = StructuralCurveMoment(
            name="LM8",
            force_action=ForceAction.ON_OPENING_EDGE,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=3.0,
            value_1=9.0,
            two_d_member="S1",
            two_d_member_opening="O1",
            edge=1,
        )
        assert moment.two_d_member_opening == "O1"

    def test_moment_on_internal_edge(self) -> None:
        """Test moment on internal edge."""
        moment = StructuralCurveMoment(
            name="LM9",
            force_action=ForceAction.ON_INTERNAL_EDGE,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MY,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=4.0,
            value_1=11.0,
            internal_edge="IE1",
        )
        assert moment.internal_edge == "IE1"

    def test_relative_positions(self) -> None:
        """Test moment with relative positions."""
        moment = StructuralCurveMoment(
            name="LM10",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.2,
            end_point=0.8,
            value_1=15.0,
            member="B1",
        )
        assert moment.start_point == 0.2
        assert moment.end_point == 0.8

    def test_local_coordinate_system(self) -> None:
        """Test moment with local coordinate system."""
        moment = StructuralCurveMoment(
            name="LM11",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MX,
            load_case="LC1",
            coordinate_system=CoordinateSystem.LOCAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=10.0,
            member="B1",
        )
        assert moment.coordinate_system == CoordinateSystem.LOCAL

    def test_from_end_origin(self) -> None:
        """Test moment with FROM_END origin."""
        moment = StructuralCurveMoment(
            name="LM12",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MY,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_END,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=2.5,
            value_1=12.0,
            member="B1",
        )
        assert moment.origin == Origin.FROM_END

    def test_with_action_type(self) -> None:
        """Test moment with action type."""
        moment = StructuralCurveMoment(
            name="LM13",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=10.0,
            member="B1",
            action_type="Wind",
        )
        assert moment.action_type == "Wind"


class TestStructuralCurveMomentValidation:
    """Tests for StructuralCurveMoment validation."""

    def test_on_beam_requires_member(self) -> None:
        """Test that ON_BEAM force action requires member."""
        with pytest.raises(ValueError, match="member must be specified"):
            StructuralCurveMoment(
                name="LM1",
                force_action=ForceAction.ON_BEAM,
                distribution=Distribution.UNIFORM,
                direction=MomentDirection.MZ,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=10.0,
            )

    def test_on_rib_requires_member_rib(self) -> None:
        """Test that ON_RIB force action requires member_rib."""
        with pytest.raises(ValueError, match="member_rib must be specified"):
            StructuralCurveMoment(
                name="LM1",
                force_action=ForceAction.ON_RIB,
                distribution=Distribution.UNIFORM,
                direction=MomentDirection.MZ,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=10.0,
            )

    def test_on_edge_requires_two_d_member(self) -> None:
        """Test that ON_EDGE requires two_d_member."""
        with pytest.raises(ValueError, match="two_d_member must be specified"):
            StructuralCurveMoment(
                name="LM1",
                force_action=ForceAction.ON_EDGE,
                distribution=Distribution.UNIFORM,
                direction=MomentDirection.MZ,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=10.0,
                edge=1,
            )

    def test_on_edge_requires_edge(self) -> None:
        """Test that ON_EDGE requires edge index."""
        with pytest.raises(ValueError, match="edge must be specified"):
            StructuralCurveMoment(
                name="LM1",
                force_action=ForceAction.ON_EDGE,
                distribution=Distribution.UNIFORM,
                direction=MomentDirection.MZ,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=10.0,
                two_d_member="S1",
            )

    def test_on_subregion_edge_requires_region(self) -> None:
        """Test that ON_SUBREGION_EDGE requires two_d_member_region."""
        with pytest.raises(ValueError, match="two_d_member_region must be specified"):
            StructuralCurveMoment(
                name="LM1",
                force_action=ForceAction.ON_SUBREGION_EDGE,
                distribution=Distribution.UNIFORM,
                direction=MomentDirection.MZ,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=10.0,
                two_d_member="S1",
                edge=1,
            )

    def test_on_opening_edge_requires_opening(self) -> None:
        """Test that ON_OPENING_EDGE requires two_d_member_opening."""
        with pytest.raises(ValueError, match="two_d_member_opening must be specified"):
            StructuralCurveMoment(
                name="LM1",
                force_action=ForceAction.ON_OPENING_EDGE,
                distribution=Distribution.UNIFORM,
                direction=MomentDirection.MZ,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=10.0,
                two_d_member="S1",
                edge=1,
            )

    def test_on_internal_edge_requires_internal_edge(self) -> None:
        """Test that ON_INTERNAL_EDGE requires internal_edge."""
        with pytest.raises(ValueError, match="internal_edge must be specified"):
            StructuralCurveMoment(
                name="LM1",
                force_action=ForceAction.ON_INTERNAL_EDGE,
                distribution=Distribution.UNIFORM,
                direction=MomentDirection.MZ,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=10.0,
            )

    def test_trapez_requires_value_2(self) -> None:
        """Test that TRAPEZ distribution requires value_2."""
        with pytest.raises(ValueError, match="value_2 must be specified"):
            StructuralCurveMoment(
                name="LM1",
                force_action=ForceAction.ON_BEAM,
                distribution=Distribution.TRAPEZ,
                direction=MomentDirection.MZ,
                load_case="LC1",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                extent=Extent.FULL,
                start_point=0.0,
                end_point=5.0,
                value_1=10.0,
                member="B1",
            )


class TestStructuralCurveMomentEquality:
    """Tests for StructuralCurveMoment equality."""

    def test_equal_moments_with_same_attributes(self) -> None:
        """Test that moments with same attributes are equal."""
        m1 = StructuralCurveMoment(
            name="LM1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=10.0,
            member="B1",
        )
        m2 = StructuralCurveMoment(
            name="LM1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=10.0,
            member="B1",
        )
        assert m1 == m2

    def test_unequal_moments_different_values(self) -> None:
        """Test that moments with different values are not equal."""
        m1 = StructuralCurveMoment(
            name="LM1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=10.0,
            member="B1",
        )
        m2 = StructuralCurveMoment(
            name="LM1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=20.0,
            member="B1",
        )
        assert m1 != m2

    def test_frozen_immutability(self) -> None:
        """Test that moment instances are frozen (immutable)."""
        moment = StructuralCurveMoment(
            name="LM1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=10.0,
            member="B1",
        )
        with pytest.raises(AttributeError):
            moment.value_1 = 20.0  # type: ignore[misc]


class TestStructuralCurveMomentEdgeCases:
    """Tests for StructuralCurveMoment edge cases."""

    def test_very_large_moment_value(self) -> None:
        """Test moment with very large value."""
        moment = StructuralCurveMoment(
            name="LM1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
            load_case="LC1",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            extent=Extent.FULL,
            start_point=0.0,
            end_point=5.0,
            value_1=1e10,
            member="B1",
        )
        assert moment.value_1 == 1e10

    def test_negative_moment_value(self) -> None:
        """Test moment with negative value."""
        moment = StructuralCurveMoment(
            name="LM1",
            force_action=ForceAction.ON_BEAM,
            distribution=Distribution.UNIFORM,
            direction=MomentDirection.MZ,
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
        assert moment.value_1 == -50.0

    def test_all_moment_direction_values(self) -> None:
        """Test all moment direction enum values."""
        directions = list(MomentDirection)
        assert len(directions) == 3
        assert MomentDirection.MX in directions
        assert MomentDirection.MY in directions
        assert MomentDirection.MZ in directions

    def test_all_force_action_values(self) -> None:
        """Test all force action enum values."""
        actions = list(ForceAction)
        assert len(actions) == 6

    def test_all_distribution_values(self) -> None:
        """Test all distribution enum values."""
        distributions = list(Distribution)
        assert len(distributions) == 2
