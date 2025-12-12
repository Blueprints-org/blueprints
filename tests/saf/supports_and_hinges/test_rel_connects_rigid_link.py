"""Tests for RelConnectsRigidLink SAF class."""

import pytest

from blueprints.saf.supports_and_hinges.rel_connects_rigid_link import (
    HingePosition,
    RelConnectsRigidLink,
    RotationConstraint,
    TranslationConstraint,
)


class TestRelConnectsRigidLinkValidInitialization:
    """Test valid initialization of RelConnectsRigidLink."""

    def test_rigid_link_no_hinge(self):
        """Test fully rigid link with no hinge."""
        link = RelConnectsRigidLink(
            name="RL1",
            node1="N1",
            node2="N2",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert link.name == "RL1"
        assert link.node1 == "N1"
        assert link.node2 == "N2"
        assert link.hinge_position == HingePosition.NONE

    def test_flexible_link_with_stiffness(self):
        """Test flexible link with required stiffness."""
        link = RelConnectsRigidLink(
            name="RL2",
            node1="N3",
            node2="N4",
            hinge_position=HingePosition.BEGIN,
            ux=TranslationConstraint.FLEXIBLE,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=TranslationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            ux_stiffness=2000.0,
        )
        assert link.ux == TranslationConstraint.FLEXIBLE
        assert link.ux_stiffness == 2000.0

    def test_hinge_at_end(self):
        """Test link with hinge at end."""
        link = RelConnectsRigidLink(
            name="RL3",
            node1="N5",
            node2="N6",
            hinge_position=HingePosition.END,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.FREE,
            fiy=RotationConstraint.FREE,
            fiz=RotationConstraint.FREE,
        )
        assert link.hinge_position == HingePosition.END

    def test_hinge_at_both_ends(self):
        """Test link with hinge at both ends."""
        link = RelConnectsRigidLink(
            name="RL4",
            node1="N7",
            node2="N8",
            hinge_position=HingePosition.BOTH,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.FREE,
            fiy=RotationConstraint.FREE,
            fiz=RotationConstraint.FREE,
        )
        assert link.hinge_position == HingePosition.BOTH

    def test_with_compression_only_constraint(self):
        """Test with compression only constraint."""
        link = RelConnectsRigidLink(
            name="RL5",
            node1="N9",
            node2="N10",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.COMPRESSION_ONLY,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert link.ux == TranslationConstraint.COMPRESSION_ONLY

    def test_with_nonlinear_constraint(self):
        """Test with non-linear constraint and required resistance."""
        link = RelConnectsRigidLink(
            name="RL6",
            node1="N11",
            node2="N12",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.NON_LINEAR,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            ux_stiffness=1000.0,
            ux_resistance=100.0,
        )
        assert link.ux == TranslationConstraint.NON_LINEAR
        assert link.ux_stiffness == 1000.0
        assert link.ux_resistance == 100.0

    def test_with_flexible_rotation(self):
        """Test with flexible rotation constraints."""
        link = RelConnectsRigidLink(
            name="RL7",
            node1="N13",
            node2="N14",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.FLEXIBLE,
            fiy=RotationConstraint.FLEXIBLE,
            fiz=RotationConstraint.FLEXIBLE,
            fix_stiffness=100.0,
            fiy_stiffness=100.0,
            fiz_stiffness=50.0,
        )
        assert link.fix == RotationConstraint.FLEXIBLE

    def test_with_all_flexible_constraints(self):
        """Test with all flexible constraints."""
        link = RelConnectsRigidLink(
            name="RL8",
            node1="N15",
            node2="N16",
            hinge_position=HingePosition.NONE,
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
        assert all(getattr(link, attr) == TranslationConstraint.FLEXIBLE for attr in ["ux", "uy", "uz"])

    def test_with_id(self):
        """Test with UUID identifier."""
        link = RelConnectsRigidLink(
            name="RL9",
            node1="N17",
            node2="N18",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
            id="link-uuid",
        )
        assert link.id == "link-uuid"


class TestRelConnectsRigidLinkValidation:
    """Test validation of stiffness and resistance requirements."""

    def test_flexible_ux_without_stiffness_raises_error(self):
        """Test that FLEXIBLE ux without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="ux_stiffness must be specified"):
            RelConnectsRigidLink(
                name="RL1",
                node1="N1",
                node2="N2",
                hinge_position=HingePosition.NONE,
                ux=TranslationConstraint.FLEXIBLE,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
            )

    def test_flexible_rotation_without_stiffness_raises_error(self):
        """Test that FLEXIBLE rotation without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fix_stiffness must be specified"):
            RelConnectsRigidLink(
                name="RL2",
                node1="N1",
                node2="N2",
                hinge_position=HingePosition.NONE,
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.FLEXIBLE,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
            )

    def test_nonlinear_translation_without_resistance_raises_error(self):
        """Test that NON_LINEAR translation without resistance raises ValueError."""
        with pytest.raises(ValueError, match="ux_resistance must be specified"):
            RelConnectsRigidLink(
                name="RL3",
                node1="N1",
                node2="N2",
                hinge_position=HingePosition.NONE,
                ux=TranslationConstraint.NON_LINEAR,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                ux_stiffness=1000.0,
            )

    def test_nonlinear_rotation_without_resistance_raises_error(self):
        """Test that NON_LINEAR rotation without resistance raises ValueError."""
        with pytest.raises(ValueError, match="fix_resistance must be specified"):
            RelConnectsRigidLink(
                name="RL4",
                node1="N1",
                node2="N2",
                hinge_position=HingePosition.NONE,
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.RIGID,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.NON_LINEAR,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
                fix_stiffness=100.0,
            )

    def test_flexible_compression_without_stiffness_raises_error(self):
        """Test that FLEXIBLE_COMPRESSION_ONLY without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="uy_stiffness must be specified"):
            RelConnectsRigidLink(
                name="RL5",
                node1="N1",
                node2="N2",
                hinge_position=HingePosition.NONE,
                ux=TranslationConstraint.RIGID,
                uy=TranslationConstraint.FLEXIBLE_COMPRESSION_ONLY,
                uz=TranslationConstraint.RIGID,
                fix=RotationConstraint.RIGID,
                fiy=RotationConstraint.RIGID,
                fiz=RotationConstraint.RIGID,
            )


class TestEnums:
    """Test enum values."""

    def test_hinge_position_values(self):
        """Test HingePosition enum values."""
        assert HingePosition.NONE.value == "None"
        assert HingePosition.BEGIN.value == "Begin"
        assert HingePosition.END.value == "End"
        assert HingePosition.BOTH.value == "Both"

    def test_translation_constraint_values(self):
        """Test TranslationConstraint enum values."""
        assert TranslationConstraint.FREE.value == "Free"
        assert TranslationConstraint.RIGID.value == "Rigid"
        assert TranslationConstraint.FLEXIBLE.value == "Flexible"
        assert TranslationConstraint.NON_LINEAR.value == "Non linear"

    def test_rotation_constraint_values(self):
        """Test RotationConstraint enum values."""
        assert RotationConstraint.FREE.value == "Free"
        assert RotationConstraint.RIGID.value == "Rigid"
        assert RotationConstraint.FLEXIBLE.value == "Flexible"
        assert RotationConstraint.NON_LINEAR.value == "Non linear"


class TestRelConnectsRigidLinkImmutability:
    """Test immutability of RelConnectsRigidLink."""

    def test_frozen_dataclass(self):
        """Test that dataclass is frozen."""
        link = RelConnectsRigidLink(
            name="RL1",
            node1="N1",
            node2="N2",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        with pytest.raises(Exception):
            link.name = "RL2"  # type: ignore

    def test_hashable(self):
        """Test that link can be used in sets."""
        link = RelConnectsRigidLink(
            name="RL1",
            node1="N1",
            node2="N2",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        link_set = {link}
        assert link in link_set


class TestRelConnectsRigidLinkEquality:
    """Test equality of RelConnectsRigidLink."""

    def test_equal_links(self):
        """Test that identical links are equal."""
        link1 = RelConnectsRigidLink(
            name="RL1",
            node1="N1",
            node2="N2",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        link2 = RelConnectsRigidLink(
            name="RL1",
            node1="N1",
            node2="N2",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert link1 == link2

    def test_unequal_links(self):
        """Test that links with different names are not equal."""
        link1 = RelConnectsRigidLink(
            name="RL1",
            node1="N1",
            node2="N2",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        link2 = RelConnectsRigidLink(
            name="RL2",
            node1="N1",
            node2="N2",
            hinge_position=HingePosition.NONE,
            ux=TranslationConstraint.RIGID,
            uy=TranslationConstraint.RIGID,
            uz=TranslationConstraint.RIGID,
            fix=RotationConstraint.RIGID,
            fiy=RotationConstraint.RIGID,
            fiz=RotationConstraint.RIGID,
        )
        assert link1 != link2
