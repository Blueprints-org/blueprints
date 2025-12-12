"""Tests for RelConnectsRigidCross SAF class."""

import pytest

from blueprints.saf.supports_and_hinges.rel_connects_rigid_cross import (
    ConnectionType,
    Constraint,
    RelConnectsRigidCross,
)


class TestRelConnectsRigidCrossValidInitialization:
    """Test valid initialization of RelConnectsRigidCross."""

    def test_fixed_rigid_cross(self) -> None:
        """Test fully fixed rigid cross connection."""
        cross = RelConnectsRigidCross(
            name="RC1",
            member1="B1",
            member2="B3",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
        )
        assert cross.name == "RC1"
        assert cross.member1 == "B1"
        assert cross.member2 == "B3"
        assert cross.u1 == Constraint.RIGID

    def test_flexible_cross_with_stiffness(self) -> None:
        """Test flexible cross with required stiffness values."""
        cross = RelConnectsRigidCross(
            name="RC2",
            member1="B2",
            member2="B4",
            u1=Constraint.FLEXIBLE,
            u2=Constraint.RIGID,
            u=Constraint.FLEXIBLE,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
            u1_stiffness=1000.0,
            u_stiffness=500.0,
        )
        assert cross.u1 == Constraint.FLEXIBLE
        assert cross.u1_stiffness == 1000.0

    def test_with_flexible_rotation_constraints(self) -> None:
        """Test with flexible rotation constraints."""
        cross = RelConnectsRigidCross(
            name="RC3",
            member1="B5",
            member2="B6",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.FLEXIBLE,
            fi2=Constraint.FLEXIBLE,
            fi=Constraint.FLEXIBLE,
            fi1_stiffness=100.0,
            fi2_stiffness=100.0,
            fi_stiffness=50.0,
        )
        assert cross.fi1 == Constraint.FLEXIBLE
        assert cross.fi1_stiffness == 100.0

    def test_with_compression_only_constraint(self) -> None:
        """Test with compression only constraint."""
        cross = RelConnectsRigidCross(
            name="RC4",
            member1="B7",
            member2="B8",
            u1=Constraint.COMPRESSION_ONLY,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
        )
        assert cross.u1 == Constraint.COMPRESSION_ONLY

    def test_with_tension_only_constraint(self) -> None:
        """Test with tension only constraint."""
        cross = RelConnectsRigidCross(
            name="RC5",
            member1="B9",
            member2="B10",
            u1=Constraint.TENSION_ONLY,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
        )
        assert cross.u1 == Constraint.TENSION_ONLY

    def test_with_flexible_compression_only(self) -> None:
        """Test with flexible compression only constraint."""
        cross = RelConnectsRigidCross(
            name="RC6",
            member1="B11",
            member2="B12",
            u1=Constraint.FLEXIBLE_COMPRESSION_ONLY,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
            u1_stiffness=2000.0,
        )
        assert cross.u1 == Constraint.FLEXIBLE_COMPRESSION_ONLY
        assert cross.u1_stiffness == 2000.0

    def test_with_flexible_tension_only(self) -> None:
        """Test with flexible tension only constraint."""
        cross = RelConnectsRigidCross(
            name="RC7",
            member1="B13",
            member2="B14",
            u2=Constraint.FLEXIBLE_TENSION_ONLY,
            u1=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
            u2_stiffness=1500.0,
        )
        assert cross.u2 == Constraint.FLEXIBLE_TENSION_ONLY

    def test_with_nonlinear_constraint_and_resistance(self) -> None:
        """Test with non-linear constraint and required resistance."""
        cross = RelConnectsRigidCross(
            name="RC8",
            member1="B15",
            member2="B16",
            u1=Constraint.NON_LINEAR,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
            u1_stiffness=1000.0,
            u1_resistance=100.0,
        )
        assert cross.u1 == Constraint.NON_LINEAR
        assert cross.u1_stiffness == 1000.0
        assert cross.u1_resistance == 100.0

    def test_with_all_constraints_flexible(self) -> None:
        """Test with all constraints flexible."""
        cross = RelConnectsRigidCross(
            name="RC9",
            member1="B17",
            member2="B18",
            u1=Constraint.FLEXIBLE,
            u2=Constraint.FLEXIBLE,
            u=Constraint.FLEXIBLE,
            fi1=Constraint.FLEXIBLE,
            fi2=Constraint.FLEXIBLE,
            fi=Constraint.FLEXIBLE,
            u1_stiffness=1000.0,
            u2_stiffness=1000.0,
            u_stiffness=500.0,
            fi1_stiffness=100.0,
            fi2_stiffness=100.0,
            fi_stiffness=50.0,
        )
        assert all(getattr(cross, attr) == Constraint.FLEXIBLE for attr in ["u1", "u2", "u", "fi1", "fi2", "fi"])

    def test_with_connection_type(self) -> None:
        """Test with connection type specified."""
        cross = RelConnectsRigidCross(
            name="RC10",
            member1="B19",
            member2="B20",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
            connection_type=ConnectionType.FIXED,
        )
        assert cross.connection_type == ConnectionType.FIXED

    def test_with_all_optional_attributes(self) -> None:
        """Test with all optional attributes."""
        cross = RelConnectsRigidCross(
            name="RC11",
            member1="B21",
            member2="B22",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
            connection_type=ConnectionType.CUSTOM,
            parent_id="parent-uuid",
            id="cross-uuid",
        )
        assert cross.connection_type == ConnectionType.CUSTOM
        assert cross.parent_id == "parent-uuid"
        assert cross.id == "cross-uuid"


class TestRelConnectsRigidCrossValidation:
    """Test validation of stiffness and resistance requirements."""

    def test_flexible_u1_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE u1 without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="u1_stiffness must be specified"):
            RelConnectsRigidCross(
                name="RC1",
                member1="B1",
                member2="B2",
                u1=Constraint.FLEXIBLE,
                u2=Constraint.RIGID,
                u=Constraint.RIGID,
                fi1=Constraint.RIGID,
                fi2=Constraint.RIGID,
                fi=Constraint.RIGID,
            )

    def test_flexible_u2_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE u2 without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="u2_stiffness must be specified"):
            RelConnectsRigidCross(
                name="RC2",
                member1="B1",
                member2="B2",
                u1=Constraint.RIGID,
                u2=Constraint.FLEXIBLE,
                u=Constraint.RIGID,
                fi1=Constraint.RIGID,
                fi2=Constraint.RIGID,
                fi=Constraint.RIGID,
            )

    def test_flexible_u_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE u without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="u_stiffness must be specified"):
            RelConnectsRigidCross(
                name="RC3",
                member1="B1",
                member2="B2",
                u1=Constraint.RIGID,
                u2=Constraint.RIGID,
                u=Constraint.FLEXIBLE,
                fi1=Constraint.RIGID,
                fi2=Constraint.RIGID,
                fi=Constraint.RIGID,
            )

    def test_flexible_fi1_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE fi1 without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fi1_stiffness must be specified"):
            RelConnectsRigidCross(
                name="RC4",
                member1="B1",
                member2="B2",
                u1=Constraint.RIGID,
                u2=Constraint.RIGID,
                u=Constraint.RIGID,
                fi1=Constraint.FLEXIBLE,
                fi2=Constraint.RIGID,
                fi=Constraint.RIGID,
            )

    def test_flexible_fi2_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE fi2 without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fi2_stiffness must be specified"):
            RelConnectsRigidCross(
                name="RC5",
                member1="B1",
                member2="B2",
                u1=Constraint.RIGID,
                u2=Constraint.RIGID,
                u=Constraint.RIGID,
                fi1=Constraint.RIGID,
                fi2=Constraint.FLEXIBLE,
                fi=Constraint.RIGID,
            )

    def test_flexible_fi_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE fi without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fi_stiffness must be specified"):
            RelConnectsRigidCross(
                name="RC6",
                member1="B1",
                member2="B2",
                u1=Constraint.RIGID,
                u2=Constraint.RIGID,
                u=Constraint.RIGID,
                fi1=Constraint.RIGID,
                fi2=Constraint.RIGID,
                fi=Constraint.FLEXIBLE,
            )

    def test_nonlinear_u1_without_resistance_raises_error(self) -> None:
        """Test that NON_LINEAR u1 without resistance raises ValueError."""
        with pytest.raises(ValueError, match="u1_resistance must be specified"):
            RelConnectsRigidCross(
                name="RC7",
                member1="B1",
                member2="B2",
                u1=Constraint.NON_LINEAR,
                u2=Constraint.RIGID,
                u=Constraint.RIGID,
                fi1=Constraint.RIGID,
                fi2=Constraint.RIGID,
                fi=Constraint.RIGID,
                u1_stiffness=1000.0,
            )

    def test_nonlinear_u2_without_resistance_raises_error(self) -> None:
        """Test that NON_LINEAR u2 without resistance raises ValueError."""
        with pytest.raises(ValueError, match="u2_resistance must be specified"):
            RelConnectsRigidCross(
                name="RC8",
                member1="B1",
                member2="B2",
                u1=Constraint.RIGID,
                u2=Constraint.NON_LINEAR,
                u=Constraint.RIGID,
                fi1=Constraint.RIGID,
                fi2=Constraint.RIGID,
                fi=Constraint.RIGID,
                u2_stiffness=1000.0,
            )

    def test_nonlinear_u_without_resistance_raises_error(self) -> None:
        """Test that NON_LINEAR u without resistance raises ValueError."""
        with pytest.raises(ValueError, match="u_resistance must be specified"):
            RelConnectsRigidCross(
                name="RC9",
                member1="B1",
                member2="B2",
                u1=Constraint.RIGID,
                u2=Constraint.RIGID,
                u=Constraint.NON_LINEAR,
                fi1=Constraint.RIGID,
                fi2=Constraint.RIGID,
                fi=Constraint.RIGID,
                u_stiffness=1000.0,
            )

    def test_nonlinear_fi1_without_resistance_raises_error(self) -> None:
        """Test that NON_LINEAR fi1 without resistance raises ValueError."""
        with pytest.raises(ValueError, match="fi1_resistance must be specified"):
            RelConnectsRigidCross(
                name="RC10",
                member1="B1",
                member2="B2",
                u1=Constraint.RIGID,
                u2=Constraint.RIGID,
                u=Constraint.RIGID,
                fi1=Constraint.NON_LINEAR,
                fi2=Constraint.RIGID,
                fi=Constraint.RIGID,
                fi1_stiffness=100.0,
            )

    def test_flexible_compression_only_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE_COMPRESSION_ONLY without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="u1_stiffness must be specified"):
            RelConnectsRigidCross(
                name="RC11",
                member1="B1",
                member2="B2",
                u1=Constraint.FLEXIBLE_COMPRESSION_ONLY,
                u2=Constraint.RIGID,
                u=Constraint.RIGID,
                fi1=Constraint.RIGID,
                fi2=Constraint.RIGID,
                fi=Constraint.RIGID,
            )


class TestConstraintEnum:
    """Test Constraint enum."""

    def test_all_constraint_values(self) -> None:
        """Test all Constraint enum values."""
        assert Constraint.FREE.value == "Free"
        assert Constraint.RIGID.value == "Rigid"
        assert Constraint.FLEXIBLE.value == "Flexible"
        assert Constraint.COMPRESSION_ONLY.value == "Compression only"
        assert Constraint.TENSION_ONLY.value == "Tension only"
        assert Constraint.FLEXIBLE_COMPRESSION_ONLY.value == "Flexible compression only"
        assert Constraint.FLEXIBLE_TENSION_ONLY.value == "Flexible tension only"
        assert Constraint.NON_LINEAR.value == "Non linear"


class TestConnectionTypeEnum:
    """Test ConnectionType enum."""

    def test_all_connection_type_values(self) -> None:
        """Test all ConnectionType enum values."""
        assert ConnectionType.FIXED.value == "Fixed"
        assert ConnectionType.HINGED.value == "Hinged"
        assert ConnectionType.CUSTOM.value == "Custom"


class TestRelConnectsRigidCrossImmutability:
    """Test immutability of RelConnectsRigidCross."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        cross = RelConnectsRigidCross(
            name="RC1",
            member1="B1",
            member2="B2",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
        )
        with pytest.raises(Exception):
            cross.name = "RC2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that cross can be used in sets and dicts."""
        cross = RelConnectsRigidCross(
            name="RC1",
            member1="B1",
            member2="B2",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
        )
        cross_set = {cross}
        assert cross in cross_set


class TestRelConnectsRigidCrossEquality:
    """Test equality of RelConnectsRigidCross."""

    def test_equal_crosses(self) -> None:
        """Test that identical crosses are equal."""
        cross1 = RelConnectsRigidCross(
            name="RC1",
            member1="B1",
            member2="B2",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
        )
        cross2 = RelConnectsRigidCross(
            name="RC1",
            member1="B1",
            member2="B2",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
        )
        assert cross1 == cross2

    def test_unequal_crosses_different_names(self) -> None:
        """Test that crosses with different names are not equal."""
        cross1 = RelConnectsRigidCross(
            name="RC1",
            member1="B1",
            member2="B2",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
        )
        cross2 = RelConnectsRigidCross(
            name="RC2",
            member1="B1",
            member2="B2",
            u1=Constraint.RIGID,
            u2=Constraint.RIGID,
            u=Constraint.RIGID,
            fi1=Constraint.RIGID,
            fi2=Constraint.RIGID,
            fi=Constraint.RIGID,
        )
        assert cross1 != cross2
