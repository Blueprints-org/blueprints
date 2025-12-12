"""Tests for RelConnectsStructuralMember SAF class."""

import pytest

from blueprints.saf.supports_and_hinges.rel_connects_structural_member import (
    Constraint,
    Position,
    RelConnectsStructuralMember,
)


class TestRelConnectsStructuralMemberValidInitialization:
    """Test valid initialization of RelConnectsStructuralMember."""

    def test_hinged_end_basic(self) -> None:
        """Test basic hinged end (free rotations, rigid translations)."""
        hinge = RelConnectsStructuralMember(
            name="H1",
            member="B1",
            position=Position.END,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        assert hinge.name == "H1"
        assert hinge.member == "B1"
        assert hinge.position == Position.END
        assert hinge.fix == Constraint.FREE

    def test_hinged_begin(self) -> None:
        """Test hinge at beginning of member."""
        hinge = RelConnectsStructuralMember(
            name="H2",
            member="B2",
            position=Position.BEGIN,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        assert hinge.position == Position.BEGIN

    def test_hinge_at_both_ends(self) -> None:
        """Test hinge applied to both ends."""
        hinge = RelConnectsStructuralMember(
            name="H3",
            member="B3",
            position=Position.BOTH,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        assert hinge.position == Position.BOTH

    def test_with_single_flexible_constraint(self) -> None:
        """Test with one flexible constraint and required stiffness."""
        hinge = RelConnectsStructuralMember(
            name="H4",
            member="B4",
            position=Position.END,
            ux=Constraint.RIGID,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            uy_stiffness=1000.0,
        )
        assert hinge.uy == Constraint.FLEXIBLE
        assert hinge.uy_stiffness == 1000.0

    def test_with_multiple_flexible_constraints(self) -> None:
        """Test with multiple flexible constraints and required stiffnesses."""
        hinge = RelConnectsStructuralMember(
            name="H5",
            member="B5",
            position=Position.BOTH,
            ux=Constraint.RIGID,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.FLEXIBLE,
            fix=Constraint.RIGID,
            fiy=Constraint.FLEXIBLE,
            fiz=Constraint.RIGID,
            uy_stiffness=1000.0,
            uz_stiffness=1500.0,
            fiy_stiffness=500.0,
        )
        assert hinge.uy_stiffness == 1000.0
        assert hinge.uz_stiffness == 1500.0
        assert hinge.fiy_stiffness == 500.0

    def test_all_flexible_constraints(self) -> None:
        """Test with all constraints flexible."""
        hinge = RelConnectsStructuralMember(
            name="H6",
            member="B6",
            position=Position.END,
            ux=Constraint.FLEXIBLE,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.FLEXIBLE,
            fix=Constraint.FLEXIBLE,
            fiy=Constraint.FLEXIBLE,
            fiz=Constraint.FLEXIBLE,
            ux_stiffness=1000.0,
            uy_stiffness=1000.0,
            uz_stiffness=1000.0,
            fix_stiffness=500.0,
            fiy_stiffness=500.0,
            fiz_stiffness=500.0,
        )
        assert all(getattr(hinge, attr) == Constraint.FLEXIBLE for attr in ["ux", "uy", "uz", "fix", "fiy", "fiz"])

    def test_with_id_attribute(self) -> None:
        """Test with UUID identifier."""
        hinge = RelConnectsStructuralMember(
            name="H7",
            member="B7",
            position=Position.END,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            id="hinge-uuid-12345",
        )
        assert hinge.id == "hinge-uuid-12345"

    def test_with_zero_stiffness(self) -> None:
        """Test with zero stiffness values (should be allowed)."""
        hinge = RelConnectsStructuralMember(
            name="H8",
            member="B8",
            position=Position.END,
            ux=Constraint.FLEXIBLE,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            ux_stiffness=0.0,
        )
        assert hinge.ux_stiffness == 0.0

    def test_with_large_stiffness_values(self) -> None:
        """Test with large stiffness values."""
        hinge = RelConnectsStructuralMember(
            name="H9",
            member="B9",
            position=Position.BEGIN,
            ux=Constraint.FLEXIBLE,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            ux_stiffness=1000000.0,
            uy_stiffness=999999.99,
        )
        assert hinge.ux_stiffness == 1000000.0
        assert hinge.uy_stiffness == 999999.99

    def test_with_negative_stiffness_values(self) -> None:
        """Test with negative stiffness values (should be allowed)."""
        hinge = RelConnectsStructuralMember(
            name="H10",
            member="B10",
            position=Position.END,
            ux=Constraint.FLEXIBLE,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            ux_stiffness=-100.0,
        )
        assert hinge.ux_stiffness == -100.0

    def test_all_rigid_constraints(self) -> None:
        """Test with all constraints rigid (fixed connection)."""
        hinge = RelConnectsStructuralMember(
            name="H11",
            member="B11",
            position=Position.BOTH,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
        )
        assert all(getattr(hinge, attr) == Constraint.RIGID for attr in ["ux", "uy", "uz", "fix", "fiy", "fiz"])

    def test_all_free_constraints(self) -> None:
        """Test with all constraints free (released connection)."""
        hinge = RelConnectsStructuralMember(
            name="H12",
            member="B12",
            position=Position.END,
            ux=Constraint.FREE,
            uy=Constraint.FREE,
            uz=Constraint.FREE,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        assert all(getattr(hinge, attr) == Constraint.FREE for attr in ["ux", "uy", "uz", "fix", "fiy", "fiz"])

    def test_mixed_constraints_with_partial_stiffness(self) -> None:
        """Test mixed constraints with some flexible (with stiffness) and some rigid/free."""
        hinge = RelConnectsStructuralMember(
            name="H13",
            member="B13",
            position=Position.BOTH,
            ux=Constraint.FREE,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.RIGID,
            fix=Constraint.FLEXIBLE,
            fiy=Constraint.FREE,
            fiz=Constraint.RIGID,
            uy_stiffness=2000.0,
            fix_stiffness=1000.0,
        )
        assert hinge.uy == Constraint.FLEXIBLE
        assert hinge.uy_stiffness == 2000.0
        assert hinge.fix == Constraint.FLEXIBLE
        assert hinge.fix_stiffness == 1000.0


class TestRelConnectsStructuralMemberValidation:
    """Test validation of stiffness requirements."""

    def test_flexible_ux_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE ux without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="ux_stiffness must be specified"):
            RelConnectsStructuralMember(
                name="H1",
                member="B1",
                position=Position.END,
                ux=Constraint.FLEXIBLE,
                uy=Constraint.RIGID,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
            )

    def test_flexible_uy_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE uy without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="uy_stiffness must be specified"):
            RelConnectsStructuralMember(
                name="H2",
                member="B2",
                position=Position.BEGIN,
                ux=Constraint.RIGID,
                uy=Constraint.FLEXIBLE,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
            )

    def test_flexible_uz_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE uz without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="uz_stiffness must be specified"):
            RelConnectsStructuralMember(
                name="H3",
                member="B3",
                position=Position.BOTH,
                ux=Constraint.RIGID,
                uy=Constraint.RIGID,
                uz=Constraint.FLEXIBLE,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
            )

    def test_flexible_fix_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE fix without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fix_stiffness must be specified"):
            RelConnectsStructuralMember(
                name="H4",
                member="B4",
                position=Position.END,
                ux=Constraint.RIGID,
                uy=Constraint.RIGID,
                uz=Constraint.RIGID,
                fix=Constraint.FLEXIBLE,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
            )

    def test_flexible_fiy_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE fiy without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fiy_stiffness must be specified"):
            RelConnectsStructuralMember(
                name="H5",
                member="B5",
                position=Position.BEGIN,
                ux=Constraint.RIGID,
                uy=Constraint.RIGID,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.FLEXIBLE,
                fiz=Constraint.RIGID,
            )

    def test_flexible_fiz_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE fiz without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fiz_stiffness must be specified"):
            RelConnectsStructuralMember(
                name="H6",
                member="B6",
                position=Position.BOTH,
                ux=Constraint.RIGID,
                uy=Constraint.RIGID,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.FLEXIBLE,
            )

    def test_multiple_flexible_missing_stiffness_raises_error(self) -> None:
        """Test that multiple flexible constraints without stiffness raise error."""
        with pytest.raises(ValueError, match="uy_stiffness must be specified"):
            RelConnectsStructuralMember(
                name="H7",
                member="B7",
                position=Position.END,
                ux=Constraint.FLEXIBLE,
                uy=Constraint.FLEXIBLE,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
                ux_stiffness=1000.0,
            )


class TestPositionEnum:
    """Test Position enum values."""

    def test_position_values(self) -> None:
        """Test Position enum values match SAF specification."""
        assert Position.BEGIN.value == "Begin"
        assert Position.END.value == "End"
        assert Position.BOTH.value == "Both"


class TestConstraintEnum:
    """Test Constraint enum values."""

    def test_constraint_values(self) -> None:
        """Test Constraint enum values match SAF specification."""
        assert Constraint.FREE.value == "Free"
        assert Constraint.RIGID.value == "Rigid"
        assert Constraint.FLEXIBLE.value == "Flexible"


class TestRelConnectsStructuralMemberImmutability:
    """Test that RelConnectsStructuralMember is immutable."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen and cannot be modified."""
        hinge = RelConnectsStructuralMember(
            name="H1",
            member="B1",
            position=Position.END,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        with pytest.raises(Exception):
            hinge.name = "H2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that hinge can be used in sets and dicts."""
        hinge1 = RelConnectsStructuralMember(
            name="H1",
            member="B1",
            position=Position.END,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        hinge_set = {hinge1}
        assert hinge1 in hinge_set


class TestRelConnectsStructuralMemberEquality:
    """Test equality and comparison of RelConnectsStructuralMember."""

    def test_equal_hinges(self) -> None:
        """Test that identical hinges are equal."""
        hinge1 = RelConnectsStructuralMember(
            name="H1",
            member="B1",
            position=Position.END,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        hinge2 = RelConnectsStructuralMember(
            name="H1",
            member="B1",
            position=Position.END,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        assert hinge1 == hinge2

    def test_unequal_hinges_different_name(self) -> None:
        """Test that hinges with different names are not equal."""
        hinge1 = RelConnectsStructuralMember(
            name="H1",
            member="B1",
            position=Position.END,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        hinge2 = RelConnectsStructuralMember(
            name="H2",
            member="B1",
            position=Position.END,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
        )
        assert hinge1 != hinge2


class TestRelConnectsStructuralMemberAllConstraintCombinations:
    """Test various constraint type combinations."""

    def test_all_constraint_type_combinations_with_required_stiffness(self) -> None:
        """Test that all combinations work when stiffness is provided where needed."""
        constraint_types = [Constraint.FREE, Constraint.RIGID, Constraint.FLEXIBLE]
        count = 0
        for ux in constraint_types:
            for uy in constraint_types:
                for uz in constraint_types:
                    # Build kwargs with stiffness values for flexible constraints
                    kwargs = {
                        "name": "H",
                        "member": "B1",
                        "position": Position.END,
                        "ux": ux,
                        "uy": uy,
                        "uz": uz,
                        "fix": Constraint.RIGID,
                        "fiy": Constraint.RIGID,
                        "fiz": Constraint.RIGID,
                    }
                    if ux == Constraint.FLEXIBLE:
                        kwargs["ux_stiffness"] = 1000.0  # type: ignore[assignment]
                    if uy == Constraint.FLEXIBLE:
                        kwargs["uy_stiffness"] = 1000.0  # type: ignore[assignment]
                    if uz == Constraint.FLEXIBLE:
                        kwargs["uz_stiffness"] = 1000.0  # type: ignore[assignment]

                    hinge = RelConnectsStructuralMember(**kwargs)  # type: ignore[arg-type]
                    assert hinge.ux == ux
                    assert hinge.uy == uy
                    assert hinge.uz == uz
                    count += 1

        # Verify we tested 27 combinations (3^3)
        assert count == 27
