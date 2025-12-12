"""Tests for RelConnectsRigidMember SAF class."""

import pytest

from blueprints.saf.supports_and_hinges.rel_connects_rigid_member import (
    RelConnectsRigidMember,
    RigidType,
    RotationConstraint,
    TranslationConstraint,
)


class TestRelConnectsRigidMemberValidInitialization:
    """Test valid initialization of RelConnectsRigidMember."""

    def test_fixed_rigid_member(self) -> None:
        """Test fixed rigid member connection."""
        member = RelConnectsRigidMember(
            name="RM1",
            connection_type=RigidType.FIXED,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert member.name == "RM1"
        assert member.connection_type == RigidType.FIXED

    def test_custom_flexible_member(self) -> None:
        """Test custom rigid member with flexible constraints."""
        member = RelConnectsRigidMember(
            name="RM2",
            connection_type=RigidType.CUSTOM,
            ux=TranslationConstraint.FLEXIBLE,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.FLEXIBLE,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            ux_stiffness=1000.0,
            fix_stiffness=500.0,
        )
        assert member.connection_type == RigidType.CUSTOM
        assert member.ux == TranslationConstraint.FLEXIBLE

    def test_with_compression_only(self) -> None:
        """Test with compression only constraint."""
        member = RelConnectsRigidMember(
            name="RM3",
            connection_type=RigidType.CUSTOM,
            ux=TranslationConstraint.COMPRESSION_ONLY,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert member.ux == TranslationConstraint.COMPRESSION_ONLY

    def test_with_nonlinear_translation(self) -> None:
        """Test with non-linear translation constraint."""
        member = RelConnectsRigidMember(
            name="RM4",
            connection_type=RigidType.CUSTOM,
            ux=TranslationConstraint.NON_LINEAR,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            ux_stiffness=1000.0,
            ux_resistance=100.0,
        )
        assert member.ux == TranslationConstraint.NON_LINEAR
        assert member.ux_resistance == 100.0

    def test_with_nonlinear_rotation(self) -> None:
        """Test with non-linear rotation constraint."""
        member = RelConnectsRigidMember(
            name="RM5",
            connection_type=RigidType.CUSTOM,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.NON_LINEAR,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            fix_stiffness=100.0,
            fix_resistance=50.0,
        )
        assert member.fix == RotationConstraint.NON_LINEAR
        assert member.fix_resistance == 50.0

    def test_with_all_flexible(self) -> None:
        """Test with all constraints flexible."""
        member = RelConnectsRigidMember(
            name="RM6",
            connection_type=RigidType.CUSTOM,
            ux=TranslationConstraint.FLEXIBLE,
            uy=TranslationConstraint.FLEXIBLE,
            uz=TranslationConstraint.FLEXIBLE,
            fix=RotationConstraint.FLEXIBLE,
            fiy=RotationConstraint.FLEXIBLE,
            fiz=RotationConstraint.FLEXIBLE,
            ux_stiffness=1000.0,
            uy_stiffness=1000.0,
            uz_stiffness=1000.0,
            fix_stiffness=100.0,
            fiy_stiffness=100.0,
            fiz_stiffness=50.0,
        )
        assert member.connection_type == RigidType.CUSTOM

    def test_with_id(self) -> None:
        """Test with UUID identifier."""
        member = RelConnectsRigidMember(
            name="RM7",
            connection_type=RigidType.FIXED,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            id="member-uuid",
        )
        assert member.id == "member-uuid"

    def test_with_flexible_compression_only(self) -> None:
        """Test with flexible compression only constraint."""
        member = RelConnectsRigidMember(
            name="RM8",
            connection_type=RigidType.CUSTOM,
            ux=TranslationConstraint.FLEXIBLE_COMPRESSION_ONLY,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            ux_stiffness=1500.0,
        )
        assert member.ux == TranslationConstraint.FLEXIBLE_COMPRESSION_ONLY

    def test_with_free_constraints(self) -> None:
        """Test with free constraints."""
        member = RelConnectsRigidMember(
            name="RM9",
            connection_type=RigidType.CUSTOM,
            ux=TranslationConstraint.FREE,
            uy=TranslationConstraint.FREE,
            uz=TranslationConstraint.FREE,
            fix=RotationConstraint.FREE,
            fiy=RotationConstraint.FREE,
            fiz=RotationConstraint.FREE,
        )
        assert member.ux == TranslationConstraint.FREE


class TestRelConnectsRigidMemberValidation:
    """Test validation of stiffness and resistance requirements."""

    def test_flexible_translation_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE translation without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="ux_stiffness must be specified"):
            RelConnectsRigidMember(
                name="RM1",
                connection_type=RigidType.CUSTOM,
                ux=TranslationConstraint.FLEXIBLE,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
            )

    def test_flexible_rotation_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE rotation without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fix_stiffness must be specified"):
            RelConnectsRigidMember(
                name="RM2",
                connection_type=RigidType.CUSTOM,
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.FLEXIBLE,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
            )

    def test_nonlinear_translation_without_resistance_raises_error(self) -> None:
        """Test that NON_LINEAR translation without resistance raises ValueError."""
        with pytest.raises(ValueError, match="ux_resistance must be specified"):
            RelConnectsRigidMember(
                name="RM3",
                connection_type=RigidType.CUSTOM,
                ux=TranslationConstraint.NON_LINEAR,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                ux_stiffness=1000.0,
            )

    def test_nonlinear_rotation_without_resistance_raises_error(self) -> None:
        """Test that NON_LINEAR rotation without resistance raises ValueError."""
        with pytest.raises(ValueError, match="fix_resistance must be specified"):
            RelConnectsRigidMember(
                name="RM4",
                connection_type=RigidType.CUSTOM,
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.NON_LINEAR,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                fix_stiffness=100.0,
            )

    def test_flexible_tension_only_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE_TENSION_ONLY without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="uy_stiffness must be specified"):
            RelConnectsRigidMember(
                name="RM5",
                connection_type=RigidType.CUSTOM,
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.FLEXIBLE_TENSION_ONLY,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
            )


class TestEnums:
    """Test enum values."""

    def test_rigid_type_values(self) -> None:
        """Test RigidType enum values."""
        assert RigidType.FIXED.value == "Fixed"
        assert RigidType.CUSTOM.value == "Custom"

    def test_translation_constraint_values(self) -> None:
        """Test TranslationConstraint enum values."""
        assert TranslationConstraint.FREE.value == "Free"
        assert TranslationConstraint.RIGID.value == "Rigid"
        assert TranslationConstraint.FLEXIBLE.value == "Flexible"
        assert TranslationConstraint.NON_LINEAR.value == "Non linear"

    def test_rotation_constraint_values(self) -> None:
        """Test RotationConstraint enum values."""
        assert RotationConstraint.FREE.value == "Free"
        assert RotationConstraint.RIGID.value == "Rigid"
        assert RotationConstraint.FLEXIBLE.value == "Flexible"
        assert RotationConstraint.NON_LINEAR.value == "Non linear"


class TestRelConnectsRigidMemberImmutability:
    """Test immutability of RelConnectsRigidMember."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        member = RelConnectsRigidMember(
            name="RM1",
            connection_type=RigidType.FIXED,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        with pytest.raises(Exception):
            member.name = "RM2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that member can be used in sets."""
        member = RelConnectsRigidMember(
            name="RM1",
            connection_type=RigidType.FIXED,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        member_set = {member}
        assert member in member_set


class TestRelConnectsRigidMemberEquality:
    """Test equality of RelConnectsRigidMember."""

    def test_equal_members(self) -> None:
        """Test that identical members are equal."""
        member1 = RelConnectsRigidMember(
            name="RM1",
            connection_type=RigidType.FIXED,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        member2 = RelConnectsRigidMember(
            name="RM1",
            connection_type=RigidType.FIXED,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert member1 == member2

    def test_unequal_members_different_types(self) -> None:
        """Test that members with different types are not equal."""
        member1 = RelConnectsRigidMember(
            name="RM1",
            connection_type=RigidType.FIXED,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        member2 = RelConnectsRigidMember(
            name="RM1",
            connection_type=RigidType.CUSTOM,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert member1 != member2
