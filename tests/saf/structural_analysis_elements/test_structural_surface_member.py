"""Tests for StructuralSurfaceMember SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_surface_member import (
    BehaviourType,
    LCSType,
    StructuralSurfaceMember,
    SurfaceEdgeType,
    SystemPlaneType,
    ThicknessType,
)


class TestValidInitialization:
    """Test valid initialization of StructuralSurfaceMember."""

    def test_simple_slab_constant_thickness(self) -> None:
        """Test simple slab with constant thickness."""
        member = StructuralSurfaceMember(
            name="S1",
            material="M1",
            thickness_type=ThicknessType.CONSTANT,
            thickness="200",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
        )
        assert member.name == "S1"
        assert member.thickness == "200"
        assert len(member.nodes) == 4

    def test_wall_variable_thickness(self) -> None:
        """Test wall with variable thickness."""
        member = StructuralSurfaceMember(
            name="W1",
            material="M2",
            thickness_type=ThicknessType.VARIABLE_Y,
            thickness="N1:250; N2:300",
            system_plane_at=SystemPlaneType.BOTTOM,
            nodes=("N1", "N2", "N3", "N4"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.Y_BY_VECTOR,
            lcs_x=0.0,
            lcs_y=1.0,
            lcs_z=0.0,
            lcs_rotation=45.0,
            behaviour=BehaviourType.ORTHOTROPIC,
        )
        assert member.type == ""
        assert member.lcs_rotation == 45.0

    def test_shell_with_curved_edges(self) -> None:
        """Test shell with curved edges."""
        member = StructuralSurfaceMember(
            name="SH1",
            material="M3",
            thickness_type=ThicknessType.CONSTANT,
            thickness="150",
            system_plane_at=SystemPlaneType.TOP,
            nodes=("N1", "N2", "N3"),
            edges=(
                SurfaceEdgeType.CIRCULAR_ARC,
                SurfaceEdgeType.PARABOLIC_ARC,
                SurfaceEdgeType.BEZIER,
            ),
            lcs_type=LCSType.TILT_OF_VECTOR_BY_POINT,
            lcs_x=0.5,
            lcs_y=0.5,
            lcs_z=0.5,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
        )
        assert len(member.edges) == 3

    def test_membrane_member(self) -> None:
        """Test membrane member."""
        member = StructuralSurfaceMember(
            name="MEM1",
            material="M4",
            thickness_type=ThicknessType.CONSTANT,
            thickness="10",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4", "N5"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.MEMBRANE,
        )
        assert member.behaviour == BehaviourType.MEMBRANE

    def test_press_only_member(self) -> None:
        """Test press only member."""
        member = StructuralSurfaceMember(
            name="P1",
            material="M5",
            thickness_type=ThicknessType.VARIABLE_RADIAL,
            thickness="100",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3"),
            edges=(SurfaceEdgeType.CIRCLE, SurfaceEdgeType.CIRCLE, SurfaceEdgeType.CIRCLE),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.PRESS_ONLY,
        )
        assert member.behaviour == BehaviourType.PRESS_ONLY

    def test_with_optional_properties(self) -> None:
        """Test member with all optional properties."""
        member = StructuralSurfaceMember(
            name="S2",
            material="M1",
            thickness_type=ThicknessType.CONSTANT,
            thickness="200",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
            type="Plate",
            internal_nodes=("I1", "I2"),
            area=25.0,
            layer="Slabs",
            structural_z_eccentricity=50.0,
            shape="Flat",
            color="#FFFF0000",
        )
        assert member.type == "Plate"
        assert member.area == 25.0
        assert member.structural_z_eccentricity == 50.0

    def test_with_different_thickness_types(self) -> None:
        """Test with different thickness variation types."""
        thickness_types = [
            ThicknessType.CONSTANT,
            ThicknessType.VARIABLE_X,
            ThicknessType.VARIABLE_Y,
            ThicknessType.VARIABLE_Z,
            ThicknessType.VARIABLE_LOCAL_X,
            ThicknessType.VARIABLE_LOCAL_Y,
            ThicknessType.VARIABLE_XY,
            ThicknessType.VARIABLE_RADIAL,
        ]
        for thickness_type in thickness_types:
            member = StructuralSurfaceMember(
                name="S",
                material="M",
                thickness_type=thickness_type,
                thickness="200",
                system_plane_at=SystemPlaneType.CENTRE,
                nodes=("N1", "N2", "N3", "N4"),
                edges=(
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                ),
                lcs_type=LCSType.X_BY_VECTOR,
                lcs_x=1.0,
                lcs_y=0.0,
                lcs_z=0.0,
                lcs_rotation=0.0,
                behaviour=BehaviourType.ISOTROPIC,
            )
            assert member.thickness_type == thickness_type

    def test_with_different_edge_types(self) -> None:
        """Test with different edge types."""
        member = StructuralSurfaceMember(
            name="S3",
            material="M1",
            thickness_type=ThicknessType.CONSTANT,
            thickness="200",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4", "N5", "N6"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.CIRCULAR_ARC,
                SurfaceEdgeType.CIRCLE_BY_3_POINTS,
                SurfaceEdgeType.PARABOLIC_ARC,
                SurfaceEdgeType.BEZIER,
                SurfaceEdgeType.SPLINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
        )
        assert len(member.edges) == 6


class TestValidation:
    """Test validation of StructuralSurfaceMember."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralSurfaceMember(
                name="",
                material="M1",
                thickness_type=ThicknessType.CONSTANT,
                thickness="200",
                system_plane_at=SystemPlaneType.CENTRE,
                nodes=("N1", "N2", "N3", "N4"),
                edges=(
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                ),
                lcs_type=LCSType.X_BY_VECTOR,
                lcs_x=1.0,
                lcs_y=0.0,
                lcs_z=0.0,
                lcs_rotation=0.0,
                behaviour=BehaviourType.ISOTROPIC,
            )

    def test_empty_material_raises_error(self) -> None:
        """Test that empty material raises ValueError."""
        with pytest.raises(ValueError, match="material cannot be empty"):
            StructuralSurfaceMember(
                name="S1",
                material="",
                thickness_type=ThicknessType.CONSTANT,
                thickness="200",
                system_plane_at=SystemPlaneType.CENTRE,
                nodes=("N1", "N2", "N3", "N4"),
                edges=(
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                ),
                lcs_type=LCSType.X_BY_VECTOR,
                lcs_x=1.0,
                lcs_y=0.0,
                lcs_z=0.0,
                lcs_rotation=0.0,
                behaviour=BehaviourType.ISOTROPIC,
            )

    def test_fewer_than_three_nodes_raises_error(self) -> None:
        """Test that fewer than 3 nodes raises ValueError."""
        with pytest.raises(ValueError, match="at least 3 nodes"):
            StructuralSurfaceMember(
                name="S1",
                material="M1",
                thickness_type=ThicknessType.CONSTANT,
                thickness="200",
                system_plane_at=SystemPlaneType.CENTRE,
                nodes=("N1", "N2"),
                edges=(SurfaceEdgeType.LINE, SurfaceEdgeType.LINE),
                lcs_type=LCSType.X_BY_VECTOR,
                lcs_x=1.0,
                lcs_y=0.0,
                lcs_z=0.0,
                lcs_rotation=0.0,
                behaviour=BehaviourType.ISOTROPIC,
            )

    def test_edges_length_mismatch_raises_error(self) -> None:
        """Test that edges length not matching nodes length raises ValueError."""
        with pytest.raises(ValueError, match="edges length"):
            StructuralSurfaceMember(
                name="S1",
                material="M1",
                thickness_type=ThicknessType.CONSTANT,
                thickness="200",
                system_plane_at=SystemPlaneType.CENTRE,
                nodes=("N1", "N2", "N3", "N4"),
                edges=(SurfaceEdgeType.LINE, SurfaceEdgeType.LINE, SurfaceEdgeType.LINE),
                lcs_type=LCSType.X_BY_VECTOR,
                lcs_x=1.0,
                lcs_y=0.0,
                lcs_z=0.0,
                lcs_rotation=0.0,
                behaviour=BehaviourType.ISOTROPIC,
            )

    def test_empty_node_name_raises_error(self) -> None:
        """Test that empty node name raises ValueError."""
        with pytest.raises(ValueError, match="Node name at index"):
            StructuralSurfaceMember(
                name="S1",
                material="M1",
                thickness_type=ThicknessType.CONSTANT,
                thickness="200",
                system_plane_at=SystemPlaneType.CENTRE,
                nodes=("N1", "", "N3", "N4"),
                edges=(
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                ),
                lcs_type=LCSType.X_BY_VECTOR,
                lcs_x=1.0,
                lcs_y=0.0,
                lcs_z=0.0,
                lcs_rotation=0.0,
                behaviour=BehaviourType.ISOTROPIC,
            )

    def test_empty_internal_node_name_raises_error(self) -> None:
        """Test that empty internal node name raises ValueError."""
        with pytest.raises(ValueError, match="Internal node name at index"):
            StructuralSurfaceMember(
                name="S1",
                material="M1",
                thickness_type=ThicknessType.CONSTANT,
                thickness="200",
                system_plane_at=SystemPlaneType.CENTRE,
                nodes=("N1", "N2", "N3", "N4"),
                edges=(
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                    SurfaceEdgeType.LINE,
                ),
                lcs_type=LCSType.X_BY_VECTOR,
                lcs_x=1.0,
                lcs_y=0.0,
                lcs_z=0.0,
                lcs_rotation=0.0,
                behaviour=BehaviourType.ISOTROPIC,
                internal_nodes=("I1", ""),
            )


class TestEnums:
    """Test enum values."""

    def test_thickness_type_values(self) -> None:
        """Test ThicknessType enum values."""
        assert ThicknessType.CONSTANT.value == "Constant"
        assert ThicknessType.VARIABLE_X.value == "Variable in global X"
        assert ThicknessType.VARIABLE_RADIAL.value == "Variable radially"

    def test_system_plane_type_values(self) -> None:
        """Test SystemPlaneType enum values."""
        assert SystemPlaneType.BOTTOM.value == "Bottom"
        assert SystemPlaneType.CENTRE.value == "Centre"
        assert SystemPlaneType.TOP.value == "Top"

    def test_behaviour_type_values(self) -> None:
        """Test BehaviourType enum values."""
        assert BehaviourType.ISOTROPIC.value == "Isotropic"
        assert BehaviourType.ORTHOTROPIC.value == "Orthotropic"
        assert BehaviourType.MEMBRANE.value == "Membrane"
        assert BehaviourType.PRESS_ONLY.value == "Press only"


class TestImmutability:
    """Test immutability of StructuralSurfaceMember."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        member = StructuralSurfaceMember(
            name="S1",
            material="M1",
            thickness_type=ThicknessType.CONSTANT,
            thickness="200",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
        )
        with pytest.raises(Exception):
            member.name = "S2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that member can be used in sets."""
        member = StructuralSurfaceMember(
            name="S1",
            material="M1",
            thickness_type=ThicknessType.CONSTANT,
            thickness="200",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
        )
        member_set = {member}
        assert member in member_set


class TestEquality:
    """Test equality of StructuralSurfaceMember."""

    def test_equal_members(self) -> None:
        """Test that identical members are equal."""
        member1 = StructuralSurfaceMember(
            name="S1",
            material="M1",
            thickness_type=ThicknessType.CONSTANT,
            thickness="200",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
        )
        member2 = StructuralSurfaceMember(
            name="S1",
            material="M1",
            thickness_type=ThicknessType.CONSTANT,
            thickness="200",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
        )
        assert member1 == member2

    def test_unequal_members_different_names(self) -> None:
        """Test that members with different names are not equal."""
        member1 = StructuralSurfaceMember(
            name="S1",
            material="M1",
            thickness_type=ThicknessType.CONSTANT,
            thickness="200",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
        )
        member2 = StructuralSurfaceMember(
            name="S2",
            material="M1",
            thickness_type=ThicknessType.CONSTANT,
            thickness="200",
            system_plane_at=SystemPlaneType.CENTRE,
            nodes=("N1", "N2", "N3", "N4"),
            edges=(
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
                SurfaceEdgeType.LINE,
            ),
            lcs_type=LCSType.X_BY_VECTOR,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            lcs_rotation=0.0,
            behaviour=BehaviourType.ISOTROPIC,
        )
        assert member1 != member2
