"""Tests for StructuralSurfaceMemberRegion SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_surface_member_region import (
    EdgeType,
    StructuralSurfaceMemberRegion,
    SystemPlaneType,
)


class TestValidInitialization:
    """Test valid initialization of StructuralSurfaceMemberRegion."""

    def test_simple_rectangular_region(self) -> None:
        """Test simple rectangular region."""
        region = StructuralSurfaceMemberRegion(
            name="R1",
            material="M1",
            thickness=200.0,
            system_plane_at=SystemPlaneType.CENTRE,
            two_d_member="S1",
            nodes=("N1", "N2", "N3", "N4"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            eccentricity_z=0.0,
        )
        assert region.name == "R1"
        assert region.thickness == 200.0
        assert len(region.nodes) == 4

    def test_region_with_curved_edges(self) -> None:
        """Test region with curved edges."""
        region = StructuralSurfaceMemberRegion(
            name="R2",
            material="M2",
            thickness=250.0,
            system_plane_at=SystemPlaneType.TOP,
            two_d_member="S2",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.CIRCULAR_ARC, EdgeType.BEZIER, EdgeType.LINE),
            eccentricity_z=-50.0,
        )
        assert region.eccentricity_z == -50.0
        assert len(region.edges) == 3

    def test_region_with_area(self) -> None:
        """Test region with area property."""
        region = StructuralSurfaceMemberRegion(
            name="R3",
            material="M3",
            thickness=200.0,
            system_plane_at=SystemPlaneType.BOTTOM,
            two_d_member="S3",
            nodes=("N1", "N2", "N3", "N4"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            eccentricity_z=0.0,
            area=5.5,
        )
        assert region.area == 5.5

    def test_region_with_all_edge_types(self) -> None:
        """Test region with different edge types."""
        edges = [
            EdgeType.LINE,
            EdgeType.BEZIER,
            EdgeType.CIRCULAR_ARC,
            EdgeType.PARABOLIC_ARC,
            EdgeType.SPLINE,
            EdgeType.CIRCLE,
            EdgeType.CIRCLE_BY_3_POINTS,
        ]
        region = StructuralSurfaceMemberRegion(
            name="R4",
            material="M4",
            thickness=200.0,
            system_plane_at=SystemPlaneType.CENTRE,
            two_d_member="S4",
            nodes=tuple(f"N{i}" for i in range(len(edges))),
            edges=tuple(edges),
            eccentricity_z=0.0,
        )
        assert len(region.edges) == len(edges)

    def test_region_with_uuid(self) -> None:
        """Test region with UUID identifier."""
        region = StructuralSurfaceMemberRegion(
            name="R5",
            material="M5",
            thickness=200.0,
            system_plane_at=SystemPlaneType.CENTRE,
            two_d_member="S5",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            eccentricity_z=0.0,
            id="39f238a5-01d0-45cf-a2eb-958170fd4f39",
        )
        assert region.id == "39f238a5-01d0-45cf-a2eb-958170fd4f39"

    def test_region_with_negative_eccentricity(self) -> None:
        """Test region with negative eccentricity."""
        region = StructuralSurfaceMemberRegion(
            name="R6",
            material="M6",
            thickness=150.0,
            system_plane_at=SystemPlaneType.TOP,
            two_d_member="S6",
            nodes=("N1", "N2", "N3", "N4", "N5"),
            edges=(
                EdgeType.LINE,
                EdgeType.LINE,
                EdgeType.LINE,
                EdgeType.LINE,
                EdgeType.LINE,
            ),
            eccentricity_z=-125.0,
        )
        assert region.eccentricity_z == -125.0

    def test_region_with_all_system_planes(self) -> None:
        """Test region with all system plane types."""
        for system_plane in [
            SystemPlaneType.BOTTOM,
            SystemPlaneType.CENTRE,
            SystemPlaneType.TOP,
        ]:
            region = StructuralSurfaceMemberRegion(
                name="R",
                material="M",
                thickness=200.0,
                system_plane_at=system_plane,
                two_d_member="S",
                nodes=("N1", "N2", "N3"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
                eccentricity_z=0.0,
            )
            assert region.system_plane_at == system_plane


class TestValidation:
    """Test validation of StructuralSurfaceMemberRegion."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralSurfaceMemberRegion(
                name="",
                material="M1",
                thickness=200.0,
                system_plane_at=SystemPlaneType.CENTRE,
                two_d_member="S1",
                nodes=("N1", "N2", "N3"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
                eccentricity_z=0.0,
            )

    def test_empty_material_raises_error(self) -> None:
        """Test that empty material raises ValueError."""
        with pytest.raises(ValueError, match="material cannot be empty"):
            StructuralSurfaceMemberRegion(
                name="R1",
                material="",
                thickness=200.0,
                system_plane_at=SystemPlaneType.CENTRE,
                two_d_member="S1",
                nodes=("N1", "N2", "N3"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
                eccentricity_z=0.0,
            )

    def test_empty_two_d_member_raises_error(self) -> None:
        """Test that empty two_d_member raises ValueError."""
        with pytest.raises(ValueError, match="two_d_member cannot be empty"):
            StructuralSurfaceMemberRegion(
                name="R1",
                material="M1",
                thickness=200.0,
                system_plane_at=SystemPlaneType.CENTRE,
                two_d_member="",
                nodes=("N1", "N2", "N3"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
                eccentricity_z=0.0,
            )

    def test_fewer_than_three_nodes_raises_error(self) -> None:
        """Test that fewer than 3 nodes raises ValueError."""
        with pytest.raises(ValueError, match="at least 3 nodes"):
            StructuralSurfaceMemberRegion(
                name="R1",
                material="M1",
                thickness=200.0,
                system_plane_at=SystemPlaneType.CENTRE,
                two_d_member="S1",
                nodes=("N1", "N2"),
                edges=(EdgeType.LINE, EdgeType.LINE),
                eccentricity_z=0.0,
            )

    def test_edges_count_mismatch_raises_error(self) -> None:
        """Test that edges count not matching nodes raises ValueError."""
        with pytest.raises(ValueError, match="edges length"):
            StructuralSurfaceMemberRegion(
                name="R1",
                material="M1",
                thickness=200.0,
                system_plane_at=SystemPlaneType.CENTRE,
                two_d_member="S1",
                nodes=("N1", "N2", "N3", "N4"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
                eccentricity_z=0.0,
            )

    def test_empty_node_name_raises_error(self) -> None:
        """Test that empty node name raises ValueError."""
        with pytest.raises(ValueError, match="Node name at index"):
            StructuralSurfaceMemberRegion(
                name="R1",
                material="M1",
                thickness=200.0,
                system_plane_at=SystemPlaneType.CENTRE,
                two_d_member="S1",
                nodes=("N1", "", "N3"),
                edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
                eccentricity_z=0.0,
            )


class TestEnums:
    """Test enum values."""

    def test_system_plane_type_values(self) -> None:
        """Test SystemPlaneType enum values."""
        assert SystemPlaneType.BOTTOM.value == "Bottom"
        assert SystemPlaneType.CENTRE.value == "Centre"
        assert SystemPlaneType.TOP.value == "Top"

    def test_edge_type_values(self) -> None:
        """Test EdgeType enum values."""
        assert EdgeType.LINE.value == "Line"
        assert EdgeType.BEZIER.value == "Bezier"
        assert EdgeType.CIRCULAR_ARC.value == "Circular Arc"
        assert EdgeType.PARABOLIC_ARC.value == "Parabolic arc"
        assert EdgeType.SPLINE.value == "Spline"
        assert EdgeType.CIRCLE.value == "Circle"
        assert EdgeType.CIRCLE_BY_3_POINTS.value == "Circle by 3 points"
        assert EdgeType.POINT.value == "Point"


class TestImmutability:
    """Test immutability of StructuralSurfaceMemberRegion."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        region = StructuralSurfaceMemberRegion(
            name="R1",
            material="M1",
            thickness=200.0,
            system_plane_at=SystemPlaneType.CENTRE,
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            eccentricity_z=0.0,
        )
        with pytest.raises(Exception):
            region.name = "R2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that region can be used in sets."""
        region = StructuralSurfaceMemberRegion(
            name="R1",
            material="M1",
            thickness=200.0,
            system_plane_at=SystemPlaneType.CENTRE,
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            eccentricity_z=0.0,
        )
        region_set = {region}
        assert region in region_set


class TestEquality:
    """Test equality of StructuralSurfaceMemberRegion."""

    def test_equal_regions(self) -> None:
        """Test that identical regions are equal."""
        region1 = StructuralSurfaceMemberRegion(
            name="R1",
            material="M1",
            thickness=200.0,
            system_plane_at=SystemPlaneType.CENTRE,
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            eccentricity_z=0.0,
        )
        region2 = StructuralSurfaceMemberRegion(
            name="R1",
            material="M1",
            thickness=200.0,
            system_plane_at=SystemPlaneType.CENTRE,
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            eccentricity_z=0.0,
        )
        assert region1 == region2

    def test_unequal_regions_different_names(self) -> None:
        """Test that regions with different names are not equal."""
        region1 = StructuralSurfaceMemberRegion(
            name="R1",
            material="M1",
            thickness=200.0,
            system_plane_at=SystemPlaneType.CENTRE,
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            eccentricity_z=0.0,
        )
        region2 = StructuralSurfaceMemberRegion(
            name="R2",
            material="M1",
            thickness=200.0,
            system_plane_at=SystemPlaneType.CENTRE,
            two_d_member="S1",
            nodes=("N1", "N2", "N3"),
            edges=(EdgeType.LINE, EdgeType.LINE, EdgeType.LINE),
            eccentricity_z=0.0,
        )
        assert region1 != region2
