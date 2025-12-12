"""Tests for StructuralCurveConnection class."""

import pytest

from blueprints.saf.supports_and_hinges.structural_curve_connection import (
    CoordinateDefinition,
    CoordinateSystem,
    Origin,
    RotationConstraint,
    StructuralCurveConnection,
    SupportType,
    TranslationConstraint,
)


class TestStructuralCurveConnectionValidInitialization:
    """Test valid initialization of StructuralCurveConnection."""

    def test_basic_curve_connection_on_member(self) -> None:
        """Test basic curve connection on member."""
        connection = StructuralCurveConnection(
            name="Sc1",
            member="B1",
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
        assert connection.name == "Sc1"
        assert connection.member == "B1"
        assert connection.member_rib is None

    def test_basic_curve_connection_on_rib(self) -> None:
        """Test basic curve connection on rib."""
        connection = StructuralCurveConnection(
            name="Sc2",
            member_rib="R1",
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
        assert connection.member_rib == "R1"
        assert connection.member is None

    def test_fully_fixed_connection(self) -> None:
        """Test fully fixed curve connection."""
        connection = StructuralCurveConnection(
            name="Sc1",
            member="B1",
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
        assert connection.ux == TranslationConstraint.RIGID

    def test_flexible_connection(self) -> None:
        """Test flexible curve connection."""
        connection = StructuralCurveConnection(
            name="Sc3",
            member="B2",
            ux=TranslationConstraint.FLEXIBLE,
            uy=TranslationConstraint.FLEXIBLE,
            uz=TranslationConstraint.FLEXIBLE,
            fix=RotationConstraint.FLEXIBLE,
            fiy=RotationConstraint.FLEXIBLE,
            fiz=RotationConstraint.FLEXIBLE,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.5,
            end_point=1.5,
        )
        assert connection.ux == TranslationConstraint.FLEXIBLE

    def test_mixed_constraint_connection(self) -> None:
        """Test curve connection with mixed constraints."""
        connection = StructuralCurveConnection(
            name="Sc4",
            member="B3",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.FREE,
            uz=TranslationConstraint.FLEXIBLE,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.FLEXIBLE,
            fiz=RotationConstraint.FREE,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        assert connection.uy == TranslationConstraint.FREE

    def test_compression_only_constraint(self) -> None:
        """Test compression only constraint."""
        connection = StructuralCurveConnection(
            name="Sc5",
            member="B4",
            ux=TranslationConstraint.COMPRESSION_ONLY,
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
        assert connection.ux == TranslationConstraint.COMPRESSION_ONLY

    def test_tension_only_constraint(self) -> None:
        """Test tension only constraint."""
        connection = StructuralCurveConnection(
            name="Sc6",
            member="B5",
            ux=TranslationConstraint.TENSION_ONLY,
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
        assert connection.ux == TranslationConstraint.TENSION_ONLY

    def test_local_coordinate_system(self) -> None:
        """Test curve connection with local coordinate system."""
        connection = StructuralCurveConnection(
            name="Sc7",
            member="B6",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.LOCAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=0.0,
            end_point=1.0,
        )
        assert connection.coordinate_system == CoordinateSystem.LOCAL

    def test_from_end_origin(self) -> None:
        """Test curve connection with from end origin."""
        connection = StructuralCurveConnection(
            name="Sc8",
            member="B7",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_END,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=1.0,
            end_point=2.0,
        )
        assert connection.origin == Origin.FROM_END

    def test_relative_coordinate_definition(self) -> None:
        """Test curve connection with relative coordinate definition."""
        connection = StructuralCurveConnection(
            name="Sc9",
            member="B8",
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
            end_point=0.5,
        )
        assert connection.coordinate_definition == CoordinateDefinition.RELATIVE

    def test_decimal_start_end_points(self) -> None:
        """Test with decimal start and end points."""
        connection = StructuralCurveConnection(
            name="Sc10",
            member="B9",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=1.5,
            end_point=3.7,
        )
        assert connection.start_point == 1.5
        assert connection.end_point == 3.7

    def test_with_optional_fields(self) -> None:
        """Test curve connection with optional fields."""
        connection = StructuralCurveConnection(
            name="Sc1",
            member="B1",
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
            support_type=SupportType.FIXED,
            parent_id="parent-uuid",
            id="uuid-1234",
        )
        assert connection.support_type == SupportType.FIXED
        assert connection.parent_id == "parent-uuid"


class TestStructuralCurveConnectionValidation:
    """Test validation of StructuralCurveConnection."""

    def test_no_member_and_no_member_rib_raises_error(self) -> None:
        """Test that neither member nor member_rib raises ValueError."""
        with pytest.raises(ValueError, match="Either member or member_rib must be specified"):
            StructuralCurveConnection(
                name="Sc1",
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

    def test_both_member_and_member_rib_raises_error(self) -> None:
        """Test that both member and member_rib raises ValueError."""
        with pytest.raises(ValueError, match="Cannot specify both member and member_rib"):
            StructuralCurveConnection(
                name="Sc1",
                member="B1",
                member_rib="R1",
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


class TestStructuralCurveConnectionEnums:
    """Test enum values."""

    def test_translation_constraint_values(self) -> None:
        """Test TranslationConstraint enum values."""
        assert TranslationConstraint.FREE.value == "Free"
        assert TranslationConstraint.RIGID.value == "Rigid"
        assert TranslationConstraint.FLEXIBLE.value == "Flexible"
        assert TranslationConstraint.COMPRESSION_ONLY.value == "Compression only"
        assert TranslationConstraint.TENSION_ONLY.value == "Tension only"

    def test_rotation_constraint_values(self) -> None:
        """Test RotationConstraint enum values."""
        assert RotationConstraint.FREE.value == "Free"
        assert RotationConstraint.RIGID.value == "Rigid"
        assert RotationConstraint.FLEXIBLE.value == "Flexible"

    def test_support_type_values(self) -> None:
        """Test SupportType enum values."""
        assert SupportType.FIXED.value == "Fixed"
        assert SupportType.HINGED.value == "Hinged"
        assert SupportType.SLIDING.value == "Sliding"
        assert SupportType.CUSTOM.value == "Custom"


class TestStructuralCurveConnectionImmutability:
    """Test immutability of StructuralCurveConnection."""

    def test_frozen_dataclass(self) -> None:
        """Test that instances are frozen and immutable."""
        connection = StructuralCurveConnection(
            name="Sc1",
            member="B1",
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
        with pytest.raises(AttributeError):
            connection.name = "Sc2"  # type: ignore[misc]

    def test_hash_support(self) -> None:
        """Test that frozen instances are hashable."""
        connection1 = StructuralCurveConnection(
            name="Sc1",
            member="B1",
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
        connection_dict = {connection1: "first"}
        assert connection_dict[connection1] == "first"


class TestStructuralCurveConnectionEquality:
    """Test equality of StructuralCurveConnection."""

    def test_equal_instances(self) -> None:
        """Test that identical instances are equal."""
        conn1 = StructuralCurveConnection(
            name="Sc1",
            member="B1",
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
        conn2 = StructuralCurveConnection(
            name="Sc1",
            member="B1",
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
        assert conn1 == conn2

    def test_unequal_instances_different_name(self) -> None:
        """Test that instances with different names are not equal."""
        conn1 = StructuralCurveConnection(
            name="Sc1",
            member="B1",
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
        conn2 = StructuralCurveConnection(
            name="Sc2",
            member="B1",
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
        assert conn1 != conn2


class TestStructuralCurveConnectionEdgeCases:
    """Test edge cases and special scenarios."""

    def test_zero_length_support(self) -> None:
        """Test curve connection with zero length (start == end)."""
        connection = StructuralCurveConnection(
            name="Sc1",
            member="B1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=1.0,
            end_point=1.0,
        )
        assert connection.start_point == connection.end_point

    def test_negative_positions(self) -> None:
        """Test curve connection with negative positions."""
        connection = StructuralCurveConnection(
            name="Sc1",
            member="B1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=-1.0,
            end_point=-0.5,
        )
        assert connection.start_point == -1.0

    def test_large_position_values(self) -> None:
        """Test with large position values."""
        connection = StructuralCurveConnection(
            name="Sc1",
            member="B1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=1000.0,
            end_point=2000.0,
        )
        assert connection.end_point == 2000.0

    def test_empty_optional_id(self) -> None:
        """Test that empty id is default."""
        connection = StructuralCurveConnection(
            name="Sc1",
            member="B1",
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
        assert connection.id == ""

    def test_scientific_notation_positions(self) -> None:
        """Test with positions in scientific notation."""
        connection = StructuralCurveConnection(
            name="Sc1",
            member="B1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            start_point=1e-3,
            end_point=2e-3,
        )
        assert connection.start_point == 0.001
