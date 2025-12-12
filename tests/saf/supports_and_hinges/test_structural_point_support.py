"""Tests for StructuralPointSupport class."""

import pytest

from blueprints.saf.supports_and_hinges.structural_point_support import (
    BoundaryCondition,
    CoordinateDefinition,
    CoordinateSystem,
    Origin,
    RotationConstraint,
    StructuralPointSupport,
    SupportType,
    TranslationConstraint,
)


class TestStructuralPointSupportNodeSupport:
    """Test node support initialization."""

    def test_fully_fixed_node_support(self) -> None:
        """Test fully fixed node support."""
        support = StructuralPointSupport(
            name="Sn6",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert support.name == "Sn6"
        assert support.boundary_condition == BoundaryCondition.IN_NODE
        assert support.node == "N1"
        assert support.ux == TranslationConstraint.RIGID

    def test_hinged_node_support(self) -> None:
        """Test hinged node support (fixed translation, free rotation)."""
        support = StructuralPointSupport(
            name="Sn7",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N2",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.FREE,
            fiy=RotationConstraint.FREE,
            fiz=RotationConstraint.FREE,
        )
        assert support.fix == RotationConstraint.FREE

    def test_flexible_node_support(self) -> None:
        """Test flexible node support."""
        support = StructuralPointSupport(
            name="Sn8",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N3",
            ux=TranslationConstraint.FLEXIBLE,
            uy=TranslationConstraint.FLEXIBLE,
            uz=TranslationConstraint.FLEXIBLE,
            fix=RotationConstraint.FLEXIBLE,
            fiy=RotationConstraint.FLEXIBLE,
            fiz=RotationConstraint.FLEXIBLE,
        )
        assert support.ux == TranslationConstraint.FLEXIBLE

    def test_mixed_constraint_support(self) -> None:
        """Test support with mixed constraint types."""
        support = StructuralPointSupport(
            name="Sn9",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N4",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.FREE,
            uz=TranslationConstraint.FLEXIBLE,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.FLEXIBLE,
            fiz=RotationConstraint.FREE,
        )
        assert support.uy == TranslationConstraint.FREE

    def test_compression_only_constraint(self) -> None:
        """Test compression only constraint."""
        support = StructuralPointSupport(
            name="Sn10",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N5",
            ux=TranslationConstraint.COMPRESSION_ONLY,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert support.ux == TranslationConstraint.COMPRESSION_ONLY

    def test_tension_only_constraint(self) -> None:
        """Test tension only constraint."""
        support = StructuralPointSupport(
            name="Sn11",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N6",
            ux=TranslationConstraint.TENSION_ONLY,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert support.ux == TranslationConstraint.TENSION_ONLY

    def test_flexible_compression_only(self) -> None:
        """Test flexible compression only constraint."""
        support = StructuralPointSupport(
            name="Sn12",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N7",
            ux=TranslationConstraint.FLEXIBLE_COMPRESSION_ONLY,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert support.ux == TranslationConstraint.FLEXIBLE_COMPRESSION_ONLY

    def test_flexible_tension_only(self) -> None:
        """Test flexible tension only constraint."""
        support = StructuralPointSupport(
            name="Sn13",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N8",
            ux=TranslationConstraint.FLEXIBLE_TENSION_ONLY,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert support.ux == TranslationConstraint.FLEXIBLE_TENSION_ONLY

    def test_non_linear_constraint(self) -> None:
        """Test non-linear constraint."""
        support = StructuralPointSupport(
            name="Sn14",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N9",
            ux=TranslationConstraint.NON_LINEAR,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.NON_LINEAR,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert support.ux == TranslationConstraint.NON_LINEAR

    def test_node_support_with_optional_fields(self) -> None:
        """Test node support with optional fields."""
        support = StructuralPointSupport(
            name="Sn6",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            support_type=SupportType.FIXED,
            id="uuid-1234",
        )
        assert support.support_type == SupportType.FIXED
        assert support.id == "uuid-1234"


class TestStructuralPointSupportBeamSupport:
    """Test beam support initialization."""

    def test_basic_beam_support(self) -> None:
        """Test basic beam support."""
        support = StructuralPointSupport(
            name="Sb1",
            boundary_condition=BoundaryCondition.ON_BEAM,
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
            position_x=0.0,
        )
        assert support.boundary_condition == BoundaryCondition.ON_BEAM
        assert support.member == "B1"
        assert support.position_x == 0.0

    def test_beam_support_from_end(self) -> None:
        """Test beam support measured from end."""
        support = StructuralPointSupport(
            name="Sb2",
            boundary_condition=BoundaryCondition.ON_BEAM,
            member="B2",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_END,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position_x=2.5,
        )
        assert support.origin == Origin.FROM_END

    def test_beam_support_local_coordinate_system(self) -> None:
        """Test beam support with local coordinate system."""
        support = StructuralPointSupport(
            name="Sb3",
            boundary_condition=BoundaryCondition.ON_BEAM,
            member="B3",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.LOCAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            position_x=1.5,
        )
        assert support.coordinate_system == CoordinateSystem.LOCAL

    def test_beam_support_relative_position(self) -> None:
        """Test beam support with relative position."""
        support = StructuralPointSupport(
            name="Sb4",
            boundary_condition=BoundaryCondition.ON_BEAM,
            member="B4",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            coordinate_system=CoordinateSystem.GLOBAL,
            origin=Origin.FROM_START,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            position_x=0.5,
        )
        assert support.coordinate_definition == CoordinateDefinition.RELATIVE

    def test_beam_support_with_optional_fields(self) -> None:
        """Test beam support with optional fields."""
        support = StructuralPointSupport(
            name="Sb1",
            boundary_condition=BoundaryCondition.ON_BEAM,
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
            position_x=0.0,
            support_type=SupportType.HINGED,
            id="uuid-5678",
        )
        assert support.support_type == SupportType.HINGED


class TestStructuralPointSupportValidation:
    """Test validation of StructuralPointSupport."""

    def test_in_node_without_node_raises_error(self) -> None:
        """Test that IN_NODE without node raises ValueError."""
        with pytest.raises(ValueError, match="node must be specified when boundary_condition = IN_NODE"):
            StructuralPointSupport(
                name="Sn6",
                boundary_condition=BoundaryCondition.IN_NODE,
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
            )

    def test_on_beam_without_member_raises_error(self) -> None:
        """Test that ON_BEAM without member raises ValueError."""
        with pytest.raises(ValueError, match="member must be specified when boundary_condition = ON_BEAM"):
            StructuralPointSupport(
                name="Sb1",
                boundary_condition=BoundaryCondition.ON_BEAM,
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                coordinate_system=CoordinateSystem.GLOBAL,
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                position_x=0.0,
            )

    def test_on_beam_without_coordinate_system_raises_error(self) -> None:
        """Test that ON_BEAM without coordinate_system raises ValueError."""
        with pytest.raises(ValueError, match="coordinate_system must be specified when boundary_condition = ON_BEAM"):
            StructuralPointSupport(
                name="Sb1",
                boundary_condition=BoundaryCondition.ON_BEAM,
                member="B1",
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                origin=Origin.FROM_START,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                position_x=0.0,
            )

    def test_on_beam_without_origin_raises_error(self) -> None:
        """Test that ON_BEAM without origin raises ValueError."""
        with pytest.raises(ValueError, match="origin must be specified when boundary_condition = ON_BEAM"):
            StructuralPointSupport(
                name="Sb1",
                boundary_condition=BoundaryCondition.ON_BEAM,
                member="B1",
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                coordinate_system=CoordinateSystem.GLOBAL,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                position_x=0.0,
            )

    def test_on_beam_without_coordinate_definition_raises_error(self) -> None:
        """Test that ON_BEAM without coordinate_definition raises ValueError."""
        with pytest.raises(ValueError, match="coordinate_definition must be specified when boundary_condition = ON_BEAM"):
            StructuralPointSupport(
                name="Sb1",
                boundary_condition=BoundaryCondition.ON_BEAM,
                member="B1",
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                coordinate_system=CoordinateSystem.GLOBAL,
                origin=Origin.FROM_START,
                position_x=0.0,
            )

    def test_on_beam_without_position_x_raises_error(self) -> None:
        """Test that ON_BEAM without position_x raises ValueError."""
        with pytest.raises(ValueError, match="position_x must be specified when boundary_condition = ON_BEAM"):
            StructuralPointSupport(
                name="Sb1",
                boundary_condition=BoundaryCondition.ON_BEAM,
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
            )


class TestStructuralPointSupportEnums:
    """Test enum values."""

    def test_boundary_condition_values(self) -> None:
        """Test BoundaryCondition enum values."""
        assert BoundaryCondition.IN_NODE.value == "In node"
        assert BoundaryCondition.ON_BEAM.value == "On beam"

    def test_translation_constraint_values(self) -> None:
        """Test all TranslationConstraint enum values."""
        assert TranslationConstraint.RIGID.value == "Rigid"
        assert TranslationConstraint.FREE.value == "Free"
        assert TranslationConstraint.FLEXIBLE.value == "Flexible"
        assert TranslationConstraint.COMPRESSION_ONLY.value == "Compression only"
        assert TranslationConstraint.TENSION_ONLY.value == "Tension only"
        assert TranslationConstraint.FLEXIBLE_COMPRESSION_ONLY.value == "Flexible compression only"
        assert TranslationConstraint.FLEXIBLE_TENSION_ONLY.value == "Flexible tension only"
        assert TranslationConstraint.NON_LINEAR.value == "Non linear"

    def test_rotation_constraint_values(self) -> None:
        """Test RotationConstraint enum values."""
        assert RotationConstraint.FREE.value == "Free"
        assert RotationConstraint.RIGID.value == "Rigid"
        assert RotationConstraint.FLEXIBLE.value == "Flexible"
        assert RotationConstraint.NON_LINEAR.value == "Non linear"

    def test_support_type_values(self) -> None:
        """Test SupportType enum values."""
        assert SupportType.FIXED.value == "Fixed"
        assert SupportType.HINGED.value == "Hinged"
        assert SupportType.SLIDING.value == "Sliding"
        assert SupportType.CUSTOM.value == "Custom"


class TestStructuralPointSupportImmutability:
    """Test immutability of StructuralPointSupport."""

    def test_frozen_dataclass(self) -> None:
        """Test that instances are frozen and immutable."""
        support = StructuralPointSupport(
            name="Sn6",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        with pytest.raises(AttributeError):
            support.name = "Sn7"  # type: ignore[misc]

    def test_hash_support(self) -> None:
        """Test that frozen instances are hashable."""
        support1 = StructuralPointSupport(
            name="Sn6",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        support_dict = {support1: "first"}
        assert support_dict[support1] == "first"


class TestStructuralPointSupportEquality:
    """Test equality of StructuralPointSupport."""

    def test_equal_instances(self) -> None:
        """Test that identical instances are equal."""
        support1 = StructuralPointSupport(
            name="Sn6",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        support2 = StructuralPointSupport(
            name="Sn6",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert support1 == support2

    def test_unequal_instances(self) -> None:
        """Test that instances with different names are not equal."""
        support1 = StructuralPointSupport(
            name="Sn6",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        support2 = StructuralPointSupport(
            name="Sn7",
            boundary_condition=BoundaryCondition.IN_NODE,
            node="N1",
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert support1 != support2
