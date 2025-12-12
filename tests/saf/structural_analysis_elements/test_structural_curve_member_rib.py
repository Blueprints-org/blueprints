"""Tests for StructuralCurveMemberRib SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_curve_member_rib import (
    RibAlignmentType,
    RibBehaviourType,
    RibConnectionType,
    RibEffectiveWidthType,
    RibShapeType,
    SegmentType,
    StructuralCurveMemberRib,
)


class TestValidInitialization:
    """Test valid initialization of StructuralCurveMemberRib."""

    def test_simple_rib_line_element(self) -> None:
        """Test simple rib with line segment."""
        rib = StructuralCurveMemberRib(
            name="R1",
            two_d_member="S1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            geometrical_shape="Line",
            alignment=RibAlignmentType.CENTRE,
            eccentricity_z=0.0,
            connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
            shape_of_rib=RibShapeType.T_SYMMETRIC,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.WIDTH,
            width_left=500.0,
            width_right=500.0,
        )
        assert rib.name == "R1"
        assert rib.two_d_member == "S1"
        assert len(rib.nodes) == 2

    def test_rib_with_multiple_segments(self) -> None:
        """Test rib with multiple segments."""
        rib = StructuralCurveMemberRib(
            name="R2",
            two_d_member="S2",
            cross_section="CS2",
            nodes=("N1", "N2", "N3"),
            segments=(SegmentType.CIRCULAR_ARC, SegmentType.LINE),
            geometrical_shape="Circular Arc",
            alignment=RibAlignmentType.TOP,
            eccentricity_z=25.0,
            connection_type=RibConnectionType.PARTIAL_SHEAR_CONNECTION,
            shape_of_rib=RibShapeType.RIGHT,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.NUMBER_OF_THICKNESS,
            width_left=3.0,
            width_right=3.0,
        )
        assert len(rib.segments) == 2

    def test_rib_with_internal_nodes(self) -> None:
        """Test rib with internal analysis nodes."""
        rib = StructuralCurveMemberRib(
            name="R3",
            two_d_member="S3",
            cross_section="CS3",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            geometrical_shape="Line",
            alignment=RibAlignmentType.BOTTOM,
            eccentricity_z=0.0,
            connection_type=RibConnectionType.WITHOUT_COMPOSITE_ACTION,
            shape_of_rib=RibShapeType.LEFT,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.WIDTH,
            width_left=400.0,
            width_right=400.0,
            internal_nodes=("I1", "I2"),
        )
        assert len(rib.internal_nodes) == 2

    def test_rib_with_optional_properties(self) -> None:
        """Test rib with optional properties."""
        rib = StructuralCurveMemberRib(
            name="R4",
            two_d_member="S4",
            cross_section="CS4",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            geometrical_shape="Line",
            alignment=RibAlignmentType.CENTRE,
            eccentricity_z=0.0,
            connection_type=RibConnectionType.USER_DEFINED_ECCENTRICITY,
            shape_of_rib=RibShapeType.T_NON_SYMMETRIC,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.WIDTH,
            width_left=500.0,
            width_right=600.0,
            length=10.5,
            layer="Ribs",
            color="#FFFF0000",
        )
        assert rib.length == 10.5
        assert rib.layer == "Ribs"
        assert rib.color == "#FFFF0000"

    def test_rib_with_all_connection_types(self) -> None:
        """Test rib with different connection types."""
        connection_types = [
            RibConnectionType.FULL_SHEAR_CONNECTION,
            RibConnectionType.PARTIAL_SHEAR_CONNECTION,
            RibConnectionType.WITHOUT_COMPOSITE_ACTION,
            RibConnectionType.USER_DEFINED_ECCENTRICITY,
        ]
        for conn_type in connection_types:
            rib = StructuralCurveMemberRib(
                name="R",
                two_d_member="S",
                cross_section="CS",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
                geometrical_shape="Line",
                alignment=RibAlignmentType.CENTRE,
                eccentricity_z=0.0,
                connection_type=conn_type,
                shape_of_rib=RibShapeType.T_SYMMETRIC,
                behaviour=RibBehaviourType.STANDARD,
                effective_width_type=RibEffectiveWidthType.WIDTH,
                width_left=500.0,
                width_right=500.0,
            )
            assert rib.connection_type == conn_type

    def test_rib_with_all_shape_types(self) -> None:
        """Test rib with different shape types."""
        shapes = [
            RibShapeType.T_SYMMETRIC,
            RibShapeType.RIGHT,
            RibShapeType.LEFT,
            RibShapeType.T_NON_SYMMETRIC,
        ]
        for shape in shapes:
            rib = StructuralCurveMemberRib(
                name="R",
                two_d_member="S",
                cross_section="CS",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
                geometrical_shape="Line",
                alignment=RibAlignmentType.CENTRE,
                eccentricity_z=0.0,
                connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
                shape_of_rib=shape,
                behaviour=RibBehaviourType.STANDARD,
                effective_width_type=RibEffectiveWidthType.WIDTH,
                width_left=500.0,
                width_right=500.0,
            )
            assert rib.shape_of_rib == shape


class TestValidation:
    """Test validation of StructuralCurveMemberRib."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralCurveMemberRib(
                name="",
                two_d_member="S1",
                cross_section="CS1",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
                geometrical_shape="Line",
                alignment=RibAlignmentType.CENTRE,
                eccentricity_z=0.0,
                connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
                shape_of_rib=RibShapeType.T_SYMMETRIC,
                behaviour=RibBehaviourType.STANDARD,
                effective_width_type=RibEffectiveWidthType.WIDTH,
                width_left=500.0,
                width_right=500.0,
            )

    def test_empty_two_d_member_raises_error(self) -> None:
        """Test that empty two_d_member raises ValueError."""
        with pytest.raises(ValueError, match="two_d_member cannot be empty"):
            StructuralCurveMemberRib(
                name="R1",
                two_d_member="",
                cross_section="CS1",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
                geometrical_shape="Line",
                alignment=RibAlignmentType.CENTRE,
                eccentricity_z=0.0,
                connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
                shape_of_rib=RibShapeType.T_SYMMETRIC,
                behaviour=RibBehaviourType.STANDARD,
                effective_width_type=RibEffectiveWidthType.WIDTH,
                width_left=500.0,
                width_right=500.0,
            )

    def test_empty_cross_section_raises_error(self) -> None:
        """Test that empty cross_section raises ValueError."""
        with pytest.raises(ValueError, match="cross_section cannot be empty"):
            StructuralCurveMemberRib(
                name="R1",
                two_d_member="S1",
                cross_section="",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
                geometrical_shape="Line",
                alignment=RibAlignmentType.CENTRE,
                eccentricity_z=0.0,
                connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
                shape_of_rib=RibShapeType.T_SYMMETRIC,
                behaviour=RibBehaviourType.STANDARD,
                effective_width_type=RibEffectiveWidthType.WIDTH,
                width_left=500.0,
                width_right=500.0,
            )

    def test_fewer_than_two_nodes_raises_error(self) -> None:
        """Test that fewer than 2 nodes raises ValueError."""
        with pytest.raises(ValueError, match="at least 2 nodes"):
            StructuralCurveMemberRib(
                name="R1",
                two_d_member="S1",
                cross_section="CS1",
                nodes=("N1",),
                segments=(SegmentType.LINE,),
                geometrical_shape="Line",
                alignment=RibAlignmentType.CENTRE,
                eccentricity_z=0.0,
                connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
                shape_of_rib=RibShapeType.T_SYMMETRIC,
                behaviour=RibBehaviourType.STANDARD,
                effective_width_type=RibEffectiveWidthType.WIDTH,
                width_left=500.0,
                width_right=500.0,
            )

    def test_segment_count_mismatch_raises_error(self) -> None:
        """Test that segment count not matching nodes - 1 raises ValueError."""
        with pytest.raises(ValueError, match="segments length"):
            StructuralCurveMemberRib(
                name="R1",
                two_d_member="S1",
                cross_section="CS1",
                nodes=("N1", "N2", "N3"),
                segments=(SegmentType.LINE,),
                geometrical_shape="Line",
                alignment=RibAlignmentType.CENTRE,
                eccentricity_z=0.0,
                connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
                shape_of_rib=RibShapeType.T_SYMMETRIC,
                behaviour=RibBehaviourType.STANDARD,
                effective_width_type=RibEffectiveWidthType.WIDTH,
                width_left=500.0,
                width_right=500.0,
            )

    def test_empty_node_name_raises_error(self) -> None:
        """Test that empty node name raises ValueError."""
        with pytest.raises(ValueError, match="Node name at index"):
            StructuralCurveMemberRib(
                name="R1",
                two_d_member="S1",
                cross_section="CS1",
                nodes=("N1", ""),
                segments=(SegmentType.LINE,),
                geometrical_shape="Line",
                alignment=RibAlignmentType.CENTRE,
                eccentricity_z=0.0,
                connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
                shape_of_rib=RibShapeType.T_SYMMETRIC,
                behaviour=RibBehaviourType.STANDARD,
                effective_width_type=RibEffectiveWidthType.WIDTH,
                width_left=500.0,
                width_right=500.0,
            )

    def test_empty_internal_node_name_raises_error(self) -> None:
        """Test that empty internal node name raises ValueError."""
        with pytest.raises(ValueError, match="Internal node name at index"):
            StructuralCurveMemberRib(
                name="R1",
                two_d_member="S1",
                cross_section="CS1",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
                geometrical_shape="Line",
                alignment=RibAlignmentType.CENTRE,
                eccentricity_z=0.0,
                connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
                shape_of_rib=RibShapeType.T_SYMMETRIC,
                behaviour=RibBehaviourType.STANDARD,
                effective_width_type=RibEffectiveWidthType.WIDTH,
                width_left=500.0,
                width_right=500.0,
                internal_nodes=("I1", ""),
            )


class TestEnums:
    """Test enum values."""

    def test_rib_alignment_type_values(self) -> None:
        """Test RibAlignmentType enum values."""
        assert RibAlignmentType.BOTTOM.value == "Bottom"
        assert RibAlignmentType.CENTRE.value == "Centre"
        assert RibAlignmentType.TOP.value == "Top"

    def test_rib_shape_type_values(self) -> None:
        """Test RibShapeType enum values."""
        assert RibShapeType.T_SYMMETRIC.value == "T Symmetric"
        assert RibShapeType.RIGHT.value == "Right"
        assert RibShapeType.LEFT.value == "Left"
        assert RibShapeType.T_NON_SYMMETRIC.value == "T Non-symmetric"

    def test_segment_type_values(self) -> None:
        """Test SegmentType enum values."""
        assert SegmentType.LINE.value == "Line"
        assert SegmentType.CIRCULAR_ARC.value == "Circular Arc"
        assert SegmentType.BEZIER.value == "Bezier"
        assert SegmentType.PARABOLIC_ARC.value == "Parabolic arc"
        assert SegmentType.SPLINE.value == "Spline"


class TestImmutability:
    """Test immutability of StructuralCurveMemberRib."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        rib = StructuralCurveMemberRib(
            name="R1",
            two_d_member="S1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            geometrical_shape="Line",
            alignment=RibAlignmentType.CENTRE,
            eccentricity_z=0.0,
            connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
            shape_of_rib=RibShapeType.T_SYMMETRIC,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.WIDTH,
            width_left=500.0,
            width_right=500.0,
        )
        with pytest.raises(Exception):
            rib.name = "R2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that rib can be used in sets."""
        rib = StructuralCurveMemberRib(
            name="R1",
            two_d_member="S1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            geometrical_shape="Line",
            alignment=RibAlignmentType.CENTRE,
            eccentricity_z=0.0,
            connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
            shape_of_rib=RibShapeType.T_SYMMETRIC,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.WIDTH,
            width_left=500.0,
            width_right=500.0,
        )
        rib_set = {rib}
        assert rib in rib_set


class TestEquality:
    """Test equality of StructuralCurveMemberRib."""

    def test_equal_ribs(self) -> None:
        """Test that identical ribs are equal."""
        rib1 = StructuralCurveMemberRib(
            name="R1",
            two_d_member="S1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            geometrical_shape="Line",
            alignment=RibAlignmentType.CENTRE,
            eccentricity_z=0.0,
            connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
            shape_of_rib=RibShapeType.T_SYMMETRIC,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.WIDTH,
            width_left=500.0,
            width_right=500.0,
        )
        rib2 = StructuralCurveMemberRib(
            name="R1",
            two_d_member="S1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            geometrical_shape="Line",
            alignment=RibAlignmentType.CENTRE,
            eccentricity_z=0.0,
            connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
            shape_of_rib=RibShapeType.T_SYMMETRIC,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.WIDTH,
            width_left=500.0,
            width_right=500.0,
        )
        assert rib1 == rib2

    def test_unequal_ribs_different_names(self) -> None:
        """Test that ribs with different names are not equal."""
        rib1 = StructuralCurveMemberRib(
            name="R1",
            two_d_member="S1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            geometrical_shape="Line",
            alignment=RibAlignmentType.CENTRE,
            eccentricity_z=0.0,
            connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
            shape_of_rib=RibShapeType.T_SYMMETRIC,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.WIDTH,
            width_left=500.0,
            width_right=500.0,
        )
        rib2 = StructuralCurveMemberRib(
            name="R2",
            two_d_member="S1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            geometrical_shape="Line",
            alignment=RibAlignmentType.CENTRE,
            eccentricity_z=0.0,
            connection_type=RibConnectionType.FULL_SHEAR_CONNECTION,
            shape_of_rib=RibShapeType.T_SYMMETRIC,
            behaviour=RibBehaviourType.STANDARD,
            effective_width_type=RibEffectiveWidthType.WIDTH,
            width_left=500.0,
            width_right=500.0,
        )
        assert rib1 != rib2
