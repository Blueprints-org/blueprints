"""Tests for RelConnectsSurfaceEdge SAF class."""

import pytest

from blueprints.saf.supports_and_hinges.rel_connects_surface_edge import (
    Constraint,
    CoordinateDefinition,
    Origin,
    RelConnectsSurfaceEdge,
)


class TestRelConnectsSurfaceEdgeValidInitialization:
    """Test valid initialization of RelConnectsSurfaceEdge."""

    def test_hinged_edge_basic(self) -> None:
        """Test basic hinged edge (free rotations, rigid translations)."""
        hinge = RelConnectsSurfaceEdge(
            name="H1",
            two_d_member="M1",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
        )
        assert hinge.name == "H1"
        assert hinge.two_d_member == "M1"
        assert hinge.edge == 0
        assert hinge.fix == Constraint.FREE

    def test_with_different_edge_indices(self) -> None:
        """Test with different edge indices (0-based)."""
        for edge_index in [0, 1, 2, 3, 4]:
            hinge = RelConnectsSurfaceEdge(
                name="H",
                two_d_member="M1",
                edge=edge_index,
                ux=Constraint.RIGID,
                uy=Constraint.RIGID,
                uz=Constraint.RIGID,
                fix=Constraint.FREE,
                fiy=Constraint.FREE,
                fiz=Constraint.FREE,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=1.0,
            )
            assert hinge.edge == edge_index

    def test_with_single_flexible_constraint(self) -> None:
        """Test with one flexible constraint and required stiffness."""
        hinge = RelConnectsSurfaceEdge(
            name="H2",
            two_d_member="M2",
            edge=1,
            ux=Constraint.RIGID,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
            uy_stiffness=500.0,
        )
        assert hinge.uy == Constraint.FLEXIBLE
        assert hinge.uy_stiffness == 500.0

    def test_with_multiple_flexible_constraints(self) -> None:
        """Test with multiple flexible constraints and required stiffnesses."""
        hinge = RelConnectsSurfaceEdge(
            name="H3",
            two_d_member="M3",
            edge=2,
            ux=Constraint.RIGID,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.FLEXIBLE,
            fix=Constraint.RIGID,
            fiy=Constraint.FLEXIBLE,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            origin=Origin.FROM_END,
            start_point=0.0,
            end_point=100.0,
            uy_stiffness=500.0,
            uz_stiffness=750.0,
            fiy_stiffness=250.0,
        )
        assert hinge.uy_stiffness == 500.0
        assert hinge.uz_stiffness == 750.0
        assert hinge.fiy_stiffness == 250.0

    def test_all_flexible_constraints(self) -> None:
        """Test with all constraints flexible."""
        hinge = RelConnectsSurfaceEdge(
            name="H4",
            two_d_member="M4",
            edge=0,
            ux=Constraint.FLEXIBLE,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.FLEXIBLE,
            fix=Constraint.FLEXIBLE,
            fiy=Constraint.FLEXIBLE,
            fiz=Constraint.FLEXIBLE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=5.0,
            ux_stiffness=500.0,
            uy_stiffness=500.0,
            uz_stiffness=500.0,
            fix_stiffness=250.0,
            fiy_stiffness=250.0,
            fiz_stiffness=250.0,
        )
        assert all(getattr(hinge, attr) == Constraint.FLEXIBLE for attr in ["ux", "uy", "uz", "fix", "fiy", "fiz"])

    def test_with_id_attribute(self) -> None:
        """Test with UUID identifier."""
        hinge = RelConnectsSurfaceEdge(
            name="H5",
            two_d_member="M5",
            edge=1,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
            id="edge-hinge-uuid-12345",
        )
        assert hinge.id == "edge-hinge-uuid-12345"

    def test_with_zero_stiffness(self) -> None:
        """Test with zero stiffness values (should be allowed)."""
        hinge = RelConnectsSurfaceEdge(
            name="H6",
            two_d_member="M6",
            edge=2,
            ux=Constraint.FLEXIBLE,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
            ux_stiffness=0.0,
        )
        assert hinge.ux_stiffness == 0.0

    def test_with_large_stiffness_values(self) -> None:
        """Test with large stiffness values."""
        hinge = RelConnectsSurfaceEdge(
            name="H7",
            two_d_member="M7",
            edge=0,
            ux=Constraint.FLEXIBLE,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=10.0,
            ux_stiffness=1000000.0,
            uy_stiffness=999999.99,
        )
        assert hinge.ux_stiffness == 1000000.0
        assert hinge.uy_stiffness == 999999.99

    def test_with_negative_stiffness_values(self) -> None:
        """Test with negative stiffness values (should be allowed)."""
        hinge = RelConnectsSurfaceEdge(
            name="H8",
            two_d_member="M8",
            edge=3,
            ux=Constraint.FLEXIBLE,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
            ux_stiffness=-100.0,
        )
        assert hinge.ux_stiffness == -100.0

    def test_all_rigid_constraints(self) -> None:
        """Test with all constraints rigid (fixed connection)."""
        hinge = RelConnectsSurfaceEdge(
            name="H9",
            two_d_member="M9",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
        )
        assert all(getattr(hinge, attr) == Constraint.RIGID for attr in ["ux", "uy", "uz", "fix", "fiy", "fiz"])

    def test_all_free_constraints(self) -> None:
        """Test with all constraints free (released connection)."""
        hinge = RelConnectsSurfaceEdge(
            name="H10",
            two_d_member="M10",
            edge=1,
            ux=Constraint.FREE,
            uy=Constraint.FREE,
            uz=Constraint.FREE,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
        )
        assert all(getattr(hinge, attr) == Constraint.FREE for attr in ["ux", "uy", "uz", "fix", "fiy", "fiz"])

    def test_with_relative_coordinates(self) -> None:
        """Test with relative coordinate definition (percentage)."""
        hinge = RelConnectsSurfaceEdge(
            name="H11",
            two_d_member="M11",
            edge=2,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=50.0,
        )
        assert hinge.coordinate_definition == CoordinateDefinition.RELATIVE

    def test_with_from_end_origin(self) -> None:
        """Test with FROM_END origin."""
        hinge = RelConnectsSurfaceEdge(
            name="H12",
            two_d_member="M12",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_END,
            start_point=0.0,
            end_point=1.0,
        )
        assert hinge.origin == Origin.FROM_END

    def test_with_zero_length_hinge(self) -> None:
        """Test with start_point equal to end_point."""
        hinge = RelConnectsSurfaceEdge(
            name="H13",
            two_d_member="M13",
            edge=1,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=5.0,
            end_point=5.0,
        )
        assert hinge.start_point == hinge.end_point

    def test_with_negative_positions(self) -> None:
        """Test with negative position values."""
        hinge = RelConnectsSurfaceEdge(
            name="H14",
            two_d_member="M14",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=-5.0,
            end_point=-1.0,
        )
        assert hinge.start_point == -5.0
        assert hinge.end_point == -1.0

    def test_with_large_position_values(self) -> None:
        """Test with large position values."""
        hinge = RelConnectsSurfaceEdge(
            name="H15",
            two_d_member="M15",
            edge=3,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.RIGID,
            fiy=Constraint.RIGID,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1000.5,
        )
        assert hinge.end_point == 1000.5

    def test_mixed_constraints_with_partial_stiffness(self) -> None:
        """Test mixed constraints with some flexible (with stiffness) and some rigid/free."""
        hinge = RelConnectsSurfaceEdge(
            name="H16",
            two_d_member="M16",
            edge=1,
            ux=Constraint.FREE,
            uy=Constraint.FLEXIBLE,
            uz=Constraint.RIGID,
            fix=Constraint.FLEXIBLE,
            fiy=Constraint.FREE,
            fiz=Constraint.RIGID,
            coordinate_definition=CoordinateDefinition.RELATIVE,
            origin=Origin.FROM_END,
            start_point=0.0,
            end_point=100.0,
            uy_stiffness=1000.0,
            fix_stiffness=500.0,
        )
        assert hinge.uy == Constraint.FLEXIBLE
        assert hinge.uy_stiffness == 1000.0
        assert hinge.fix == Constraint.FLEXIBLE
        assert hinge.fix_stiffness == 500.0


class TestRelConnectsSurfaceEdgeValidation:
    """Test validation of stiffness requirements."""

    def test_flexible_ux_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE ux without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="ux_stiffness must be specified"):
            RelConnectsSurfaceEdge(
                name="H1",
                two_d_member="M1",
                edge=0,
                ux=Constraint.FLEXIBLE,
                uy=Constraint.RIGID,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=1.0,
            )

    def test_flexible_uy_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE uy without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="uy_stiffness must be specified"):
            RelConnectsSurfaceEdge(
                name="H2",
                two_d_member="M2",
                edge=1,
                ux=Constraint.RIGID,
                uy=Constraint.FLEXIBLE,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=1.0,
            )

    def test_flexible_uz_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE uz without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="uz_stiffness must be specified"):
            RelConnectsSurfaceEdge(
                name="H3",
                two_d_member="M3",
                edge=2,
                ux=Constraint.RIGID,
                uy=Constraint.RIGID,
                uz=Constraint.FLEXIBLE,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=1.0,
            )

    def test_flexible_fix_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE fix without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fix_stiffness must be specified"):
            RelConnectsSurfaceEdge(
                name="H4",
                two_d_member="M4",
                edge=0,
                ux=Constraint.RIGID,
                uy=Constraint.RIGID,
                uz=Constraint.RIGID,
                fix=Constraint.FLEXIBLE,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=1.0,
            )

    def test_flexible_fiy_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE fiy without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fiy_stiffness must be specified"):
            RelConnectsSurfaceEdge(
                name="H5",
                two_d_member="M5",
                edge=1,
                ux=Constraint.RIGID,
                uy=Constraint.RIGID,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.FLEXIBLE,
                fiz=Constraint.RIGID,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=1.0,
            )

    def test_flexible_fiz_without_stiffness_raises_error(self) -> None:
        """Test that FLEXIBLE fiz without stiffness raises ValueError."""
        with pytest.raises(ValueError, match="fiz_stiffness must be specified"):
            RelConnectsSurfaceEdge(
                name="H6",
                two_d_member="M6",
                edge=2,
                ux=Constraint.RIGID,
                uy=Constraint.RIGID,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.FLEXIBLE,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=1.0,
            )

    def test_multiple_flexible_missing_stiffness_raises_error(self) -> None:
        """Test that multiple flexible constraints without stiffness raise error."""
        with pytest.raises(ValueError, match="uy_stiffness must be specified"):
            RelConnectsSurfaceEdge(
                name="H7",
                two_d_member="M7",
                edge=0,
                ux=Constraint.FLEXIBLE,
                uy=Constraint.FLEXIBLE,
                uz=Constraint.RIGID,
                fix=Constraint.RIGID,
                fiy=Constraint.RIGID,
                fiz=Constraint.RIGID,
                coordinate_definition=CoordinateDefinition.ABSOLUTE,
                origin=Origin.FROM_START,
                start_point=0.0,
                end_point=1.0,
                ux_stiffness=500.0,
            )


class TestConstraintEnum:
    """Test Constraint enum values."""

    def test_constraint_values(self) -> None:
        """Test Constraint enum values match SAF specification."""
        assert Constraint.FREE.value == "Free"
        assert Constraint.RIGID.value == "Rigid"
        assert Constraint.FLEXIBLE.value == "Flexible"


class TestCoordinateDefinitionEnum:
    """Test CoordinateDefinition enum values."""

    def test_coordinate_definition_values(self) -> None:
        """Test CoordinateDefinition enum values."""
        assert CoordinateDefinition.ABSOLUTE.value == "Absolute"
        assert CoordinateDefinition.RELATIVE.value == "Relative"


class TestOriginEnum:
    """Test Origin enum values."""

    def test_origin_values(self) -> None:
        """Test Origin enum values."""
        assert Origin.FROM_START.value == "From start"
        assert Origin.FROM_END.value == "From end"


class TestRelConnectsSurfaceEdgeImmutability:
    """Test that RelConnectsSurfaceEdge is immutable."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen and cannot be modified."""
        hinge = RelConnectsSurfaceEdge(
            name="H1",
            two_d_member="M1",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
        )
        with pytest.raises(Exception):
            hinge.name = "H2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that hinge can be used in sets and dicts."""
        hinge1 = RelConnectsSurfaceEdge(
            name="H1",
            two_d_member="M1",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
        )
        hinge_set = {hinge1}
        assert hinge1 in hinge_set


class TestRelConnectsSurfaceEdgeEquality:
    """Test equality and comparison of RelConnectsSurfaceEdge."""

    def test_equal_hinges(self) -> None:
        """Test that identical hinges are equal."""
        hinge1 = RelConnectsSurfaceEdge(
            name="H1",
            two_d_member="M1",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
        )
        hinge2 = RelConnectsSurfaceEdge(
            name="H1",
            two_d_member="M1",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
        )
        assert hinge1 == hinge2

    def test_unequal_hinges_different_name(self) -> None:
        """Test that hinges with different names are not equal."""
        hinge1 = RelConnectsSurfaceEdge(
            name="H1",
            two_d_member="M1",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
        )
        hinge2 = RelConnectsSurfaceEdge(
            name="H2",
            two_d_member="M1",
            edge=0,
            ux=Constraint.RIGID,
            uy=Constraint.RIGID,
            uz=Constraint.RIGID,
            fix=Constraint.FREE,
            fiy=Constraint.FREE,
            fiz=Constraint.FREE,
            coordinate_definition=CoordinateDefinition.ABSOLUTE,
            origin=Origin.FROM_START,
            start_point=0.0,
            end_point=1.0,
        )
        assert hinge1 != hinge2


class TestRelConnectsSurfaceEdgeAllConstraintCombinations:
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
                        "two_d_member": "M1",
                        "edge": 0,
                        "ux": ux,
                        "uy": uy,
                        "uz": uz,
                        "fix": Constraint.RIGID,
                        "fiy": Constraint.RIGID,
                        "fiz": Constraint.RIGID,
                        "coordinate_definition": CoordinateDefinition.ABSOLUTE,
                        "origin": Origin.FROM_START,
                        "start_point": 0.0,
                        "end_point": 1.0,
                    }
                    if ux == Constraint.FLEXIBLE:
                        kwargs["ux_stiffness"] = 500.0
                    if uy == Constraint.FLEXIBLE:
                        kwargs["uy_stiffness"] = 500.0
                    if uz == Constraint.FLEXIBLE:
                        kwargs["uz_stiffness"] = 500.0

                    hinge = RelConnectsSurfaceEdge(**kwargs)  # type: ignore[arg-type]
                    assert hinge.ux == ux
                    assert hinge.uy == uy
                    assert hinge.uz == uz
                    count += 1

        # Verify we tested 27 combinations (3^3)
        assert count == 27
