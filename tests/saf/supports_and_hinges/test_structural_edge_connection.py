"""Tests for StructuralEdgeConnection SAF class."""

import pytest

from blueprints.saf import (
    StructuralEdgeConnection,
)
from blueprints.saf.supports_and_hinges.structural_edge_connection import (
    BoundaryCondition,
    CoordinateDefinition,
    CoordinateSystem,
    Origin,
    RotationConstraint,
    SupportType,
    TranslationConstraint,
)


class TestStructuralEdgeConnectionValidInitialization:
    """Test valid initialization of StructuralEdgeConnection."""

    def test_on_edge_with_required_attributes(self):
        """Test creation with ON_EDGE boundary condition and required two_d_member."""
        connection = StructuralEdgeConnection(
            name="Se1",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        assert connection.name == "Se1"
        assert connection.boundary_condition == BoundaryCondition.ON_EDGE
        assert connection.two_d_member == "M1"
        assert connection.ux == TranslationConstraint.RIGID

    def test_on_subregion_edge_with_required_attributes(self):
        """Test creation with ON_SUBREGION_EDGE and required two_d_member_region."""
        connection = StructuralEdgeConnection(
            name="Se2",
            boundary_condition=BoundaryCondition.ON_SUBREGION_EDGE,
            two_d_member_region="R1",
            ux=TranslationConstraint.FREE,
            uy=TranslationConstraint.FREE,
            uz=TranslationConstraint.FREE,
            fix=RotationConstraint.FREE,
            fiy=RotationConstraint.FREE,
            fiz=RotationConstraint.FREE,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        assert connection.name == "Se2"
        assert connection.boundary_condition == BoundaryCondition.ON_SUBREGION_EDGE
        assert connection.two_d_member_region == "R1"

    def test_on_opening_edge_with_required_attributes(self):
        """Test creation with ON_OPENING_EDGE and required two_d_member_opening."""
        connection = StructuralEdgeConnection(
            name="Se3",
            boundary_condition=BoundaryCondition.ON_OPENING_EDGE,
            two_d_member_opening="O1",
            ux=TranslationConstraint.FLEXIBLE,
            uy=TranslationConstraint.FLEXIBLE,
            uz=TranslationConstraint.FLEXIBLE,
            fix=RotationConstraint.FLEXIBLE,
            fiy=RotationConstraint.FLEXIBLE,
            fiz=RotationConstraint.FLEXIBLE,
            coordinate_system=CoordinateSystem.LOCAL,
            origin=Origin.FROM_END,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            start_point=0.0,
            end_point=100.0,
        )
        assert connection.name == "Se3"
        assert connection.boundary_condition == BoundaryCondition.ON_OPENING_EDGE
        assert connection.two_d_member_opening == "O1"

    def test_on_internal_edge_with_required_attributes(self):
        """Test creation with ON_INTERNAL_EDGE and required internal_edge."""
        connection = StructuralEdgeConnection(
            name="Se4",
            boundary_condition=BoundaryCondition.ON_INTERNAL_EDGE,
            internal_edge="IE1",
            ux=TranslationConstraint.COMPRESSION_ONLY,
            uy=TranslationConstraint.TENSION_ONLY,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.FREE,
            fiz=RotationConstraint.FLEXIBLE,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=5.0,
        )
        assert connection.name == "Se4"
        assert connection.boundary_condition == BoundaryCondition.ON_INTERNAL_EDGE
        assert connection.internal_edge == "IE1"

    def test_with_all_optional_attributes(self):
        """Test creation with all optional attributes specified."""
        connection = StructuralEdgeConnection(
            name="Se5",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=10.0,
            edge_index=1,
            support_type=SupportType.FIXED,
            parent_id="parent-uuid",
            id="edge-uuid",
        )
        assert connection.edge_index == 1
        assert connection.support_type == SupportType.FIXED
        assert connection.parent_id == "parent-uuid"
        assert connection.id == "edge-uuid"

    def test_with_edge_index(self):
        """Test with edge_index specified."""
        connection = StructuralEdgeConnection(
            name="Se6",
            boundary_condition=BoundaryCondition.ON_SUBREGION_EDGE,
            two_d_member_region="R1",
            ux=TranslationConstraint.FREE,
            uy=TranslationConstraint.FREE,
            uz=TranslationConstraint.FREE,
            fix=RotationConstraint.FREE,
            fiy=RotationConstraint.FREE,
            fiz=RotationConstraint.FREE,
            coordinate_system=CoordinateSystem.LOCAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            start_point=0.0,
            end_point=100.0,
            edge_index=3,
        )
        assert connection.edge_index == 3

    def test_with_different_support_types(self):
        """Test with different support type classifications."""
        for support_type in [
            SupportType.FIXED,
            SupportType.HINGED,
            SupportType.SLIDING,
            SupportType.CUSTOM,
        ]:
            connection = StructuralEdgeConnection(
                name="Se7",
                boundary_condition=BoundaryCondition.ON_EDGE,
                two_d_member="M1",
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                coordinate_system=CoordinateSystem.GLOBAL,
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                start_point=0.0,
                end_point=1.0,
                support_type=support_type,
            )
            assert connection.support_type == support_type

    def test_with_different_coordinate_systems(self):
        """Test with both global and local coordinate systems."""
        for coord_system in [CoordinateSystem.GLOBAL, CoordinateSystem.LOCAL]:
            connection = StructuralEdgeConnection(
                name="Se8",
                boundary_condition=BoundaryCondition.ON_EDGE,
                two_d_member="M1",
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                coordinate_system=coord_system,
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                start_point=0.0,
                end_point=1.0,
            )
            assert connection.coordinate_system == coord_system

    def test_with_different_origins(self):
        """Test with both FROM_START and FROM_END origins."""
        for origin in [Origin.FROM_START, Origin.FROM_END]:
            connection = StructuralEdgeConnection(
                name="Se9",
                boundary_condition=BoundaryCondition.ON_EDGE,
                two_d_member="M1",
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                coordinate_system=CoordinateSystem.GLOBAL,
                origin=origin,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                start_point=0.0,
                end_point=1.0,
            )
            assert connection.origin == origin

    def test_with_zero_length_support(self):
        """Test with start_point equal to end_point."""
        connection = StructuralEdgeConnection(
            name="Se10",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=5.0,
            end_point=5.0,
        )
        assert connection.start_point == connection.end_point

    def test_with_negative_positions(self):
        """Test with negative position values."""
        connection = StructuralEdgeConnection(
            name="Se11",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=-5.0,
            end_point=-1.0,
        )
        assert connection.start_point == -5.0
        assert connection.end_point == -1.0

    def test_with_large_position_values(self):
        """Test with large position values."""
        connection = StructuralEdgeConnection(
            name="Se12",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1000.5,
        )
        assert connection.end_point == 1000.5

    def test_with_relative_coordinate_definition(self):
        """Test with relative percentage coordinates."""
        connection = StructuralEdgeConnection(
            name="Se13",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            start_point=0.0,
            end_point=50.0,
        )
        assert connection.coordinate_definition == CoordinateDefinition.RELATIVE


class TestStructuralEdgeConnectionValidation:
    """Test validation of conditional requirements."""

    def test_on_edge_without_two_d_member_raises_error(self):
        """Test that ON_EDGE without two_d_member raises ValueError."""
        with pytest.raises(ValueError, match="two_d_member must be specified"):
            StructuralEdgeConnection(
                name="Se1",
                boundary_condition=BoundaryCondition.ON_EDGE,
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                coordinate_system=CoordinateSystem.GLOBAL,
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                start_point=0.0,
                end_point=1.0,
            )

    def test_on_subregion_edge_without_two_d_member_region_raises_error(self):
        """Test that ON_SUBREGION_EDGE without two_d_member_region raises ValueError."""
        with pytest.raises(ValueError, match="two_d_member_region must be specified"):
            StructuralEdgeConnection(
                name="Se2",
                boundary_condition=BoundaryCondition.ON_SUBREGION_EDGE,
                ux=TranslationConstraint.FREE,
                uy=TranslationConstraint.FREE,
                uz=TranslationConstraint.FREE,
                fix=RotationConstraint.FREE,
                fiy=RotationConstraint.FREE,
                fiz=RotationConstraint.FREE,
                coordinate_system=CoordinateSystem.GLOBAL,
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                start_point=0.0,
                end_point=1.0,
            )

    def test_on_opening_edge_without_two_d_member_opening_raises_error(self):
        """Test that ON_OPENING_EDGE without two_d_member_opening raises ValueError."""
        with pytest.raises(ValueError, match="two_d_member_opening must be specified"):
            StructuralEdgeConnection(
                name="Se3",
                boundary_condition=BoundaryCondition.ON_OPENING_EDGE,
                ux=TranslationConstraint.FLEXIBLE,
                uy=TranslationConstraint.FLEXIBLE,
                uz=TranslationConstraint.FLEXIBLE,
                fix=RotationConstraint.FLEXIBLE,
                fiy=RotationConstraint.FLEXIBLE,
                fiz=RotationConstraint.FLEXIBLE,
                coordinate_system=CoordinateSystem.LOCAL,
                origin=Origin.FROM_END,
                coordinate_definition=CoordinateDefinition.RELATIVE,
                start_point=0.0,
                end_point=100.0,
            )

    def test_on_internal_edge_without_internal_edge_raises_error(self):
        """Test that ON_INTERNAL_EDGE without internal_edge raises ValueError."""
        with pytest.raises(ValueError, match="internal_edge must be specified"):
            StructuralEdgeConnection(
                name="Se4",
                boundary_condition=BoundaryCondition.ON_INTERNAL_EDGE,
                ux=TranslationConstraint.COMPRESSION_ONLY,
                uy=TranslationConstraint.TENSION_ONLY,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.FREE,
                fiz=RotationConstraint.FLEXIBLE,
                coordinate_system=CoordinateSystem.GLOBAL,
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                start_point=0.0,
                end_point=5.0,
            )


class TestStructuralEdgeConnectionTranslationConstraints:
    """Test all translation constraint types."""

    def test_all_translation_constraint_types(self):
        """Test with all translation constraint type combinations."""
        for ux in TranslationConstraint:
            for uy in TranslationConstraint:
                for uz in TranslationConstraint:
                    connection = StructuralEdgeConnection(
                        name="Se",
                        boundary_condition=BoundaryCondition.ON_EDGE,
                        two_d_member="M1",
                        ux=ux,
                        uy=uy,
                        uz=uz,
                        fix=RotationConstraint.RIGID,
                        fiy=RotationConstraint.RIGID,
                        fiz=RotationConstraint.RIGID,
                        coordinate_system=CoordinateSystem.GLOBAL,
                        origin=Origin.FROM_START,
                        coordinate_definition=CoordinateDefinition.ABSOLUTE,
                        start_point=0.0,
                        end_point=1.0,
                    )
                    assert connection.ux == ux
                    assert connection.uy == uy
                    assert connection.uz == uz


class TestStructuralEdgeConnectionRotationConstraints:
    """Test all rotation constraint types."""

    def test_all_rotation_constraint_types(self):
        """Test with all rotation constraint type combinations."""
        for fix in RotationConstraint:
            for fiy in RotationConstraint:
                for fiz in RotationConstraint:
                    connection = StructuralEdgeConnection(
                        name="Se",
                        boundary_condition=BoundaryCondition.ON_EDGE,
                        two_d_member="M1",
                        ux=TranslationConstraint.RIGID,
                        uy=TranslationConstraint.RIGID,
                        uz=TranslationConstraint.RIGID,
                        fix=fix,
                        fiy=fiy,
                        fiz=fiz,
                        coordinate_system=CoordinateSystem.GLOBAL,
                        origin=Origin.FROM_START,
                        coordinate_definition=CoordinateDefinition.ABSOLUTE,
                        start_point=0.0,
                        end_point=1.0,
                    )
                    assert connection.fix == fix
                    assert connection.fiy == fiy
                    assert connection.fiz == fiz


class TestStructuralEdgeConnectionImmutability:
    """Test that StructuralEdgeConnection is immutable."""

    def test_frozen_dataclass(self):
        """Test that dataclass is frozen and cannot be modified."""
        connection = StructuralEdgeConnection(
            name="Se1",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        with pytest.raises(Exception):
            connection.name = "Se2"  # type: ignore

    def test_hashable(self):
        """Test that connection can be used in sets and dicts."""
        connection1 = StructuralEdgeConnection(
            name="Se1",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        connection_set = {connection1}
        assert connection1 in connection_set


class TestStructuralEdgeConnectionEquality:
    """Test equality and comparison of StructuralEdgeConnection."""

    def test_equal_connections(self):
        """Test that identical connections are equal."""
        connection1 = StructuralEdgeConnection(
            name="Se1",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        connection2 = StructuralEdgeConnection(
            name="Se1",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        assert connection1 == connection2

    def test_unequal_connections_different_name(self):
        """Test that connections with different names are not equal."""
        connection1 = StructuralEdgeConnection(
            name="Se1",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        connection2 = StructuralEdgeConnection(
            name="Se2",
            boundary_condition=BoundaryCondition.ON_EDGE,
            two_d_member="M1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        assert connection1 != connection2


class TestBoundaryConditionEnum:
    """Test BoundaryCondition enum."""

    def test_all_boundary_conditions(self):
        """Test all boundary condition enum values."""
        assert BoundaryCondition.ON_EDGE.value == "On edge"
        assert BoundaryCondition.ON_SUBREGION_EDGE.value == "On subregion edge"
        assert BoundaryCondition.ON_OPENING_EDGE.value == "On opening edge"
        assert BoundaryCondition.ON_INTERNAL_EDGE.value == "On internal edge"


class TestEnumValues:
    """Test enum value strings match SAF specification."""

    def test_translation_constraint_values(self):
        """Test TranslationConstraint enum values."""
        assert TranslationConstraint.FREE.value == "Free"
        assert TranslationConstraint.RIGID.value == "Rigid"
        assert TranslationConstraint.FLEXIBLE.value == "Flexible"
        assert TranslationConstraint.COMPRESSION_ONLY.value == "Compression only"
        assert TranslationConstraint.TENSION_ONLY.value == "Tension only"

    def test_rotation_constraint_values(self):
        """Test RotationConstraint enum values."""
        assert RotationConstraint.FREE.value == "Free"
        assert RotationConstraint.RIGID.value == "Rigid"
        assert RotationConstraint.FLEXIBLE.value == "Flexible"

    def test_coordinate_system_values(self):
        """Test CoordinateSystem enum values."""
        assert CoordinateSystem.GLOBAL.value == "Global"
        assert CoordinateSystem.LOCAL.value == "Local"

    def test_origin_values(self):
        """Test Origin enum values."""
        assert Origin.FROM_START.value == "From start"
        assert Origin.FROM_END.value == "From end"

    def test_coordinate_definition_values(self):
        """Test CoordinateDefinition enum values."""
        assert CoordinateDefinition.ABSOLUTE.value == "Absolute"
        assert CoordinateDefinition.RELATIVE.value == "Relative"

    def test_support_type_values(self):
        """Test SupportType enum values."""
        assert SupportType.FIXED.value == "Fixed"
        assert SupportType.HINGED.value == "Hinged"
        assert SupportType.SLIDING.value == "Sliding"
        assert SupportType.CUSTOM.value == "Custom"
