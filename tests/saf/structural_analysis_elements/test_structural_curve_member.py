"""Tests for StructuralCurveMember SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_curve_member import (
    BehaviourType,
    GeometricalShapeType,
    LCSType,
    SegmentType,
    StructuralCurveMember,
    SystemLineType,
)


class TestStructuralCurveMemberValidInitialization:
    """Test valid initialization of StructuralCurveMember."""

    def test_simple_beam(self) -> None:
        """Test simple beam with minimal properties."""
        beam = StructuralCurveMember(
            name="B1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam.name == "B1"
        assert beam.cross_section == "CS1"
        assert len(beam.nodes) == 2

    def test_beam_with_member_type(self) -> None:
        """Test beam with member type classification."""
        beam = StructuralCurveMember(
            name="B2",
            cross_section="CS2",
            nodes=("N2", "N3"),
            segments=(SegmentType.LINE,),
            member_type="Beam",
            lcs=LCSType.Y_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=1.0,
            lcs_z=0.0,
            system_line=SystemLineType.TOP,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=50.0,
            analysis_y_eccentricity_end=50.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam.member_type == "Beam"

    def test_column(self) -> None:
        """Test column member."""
        column = StructuralCurveMember(
            name="C1",
            cross_section="CS3",
            nodes=("N4", "N5"),
            segments=(SegmentType.LINE,),
            member_type="Column",
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert column.member_type == "Column"

    def test_curved_beam(self) -> None:
        """Test curved beam with multiple segments."""
        beam = StructuralCurveMember(
            name="B3",
            cross_section="CS4",
            nodes=("N6", "N7", "N8"),
            segments=(
                SegmentType.CIRCULAR_ARC,
                SegmentType.LINE,
            ),
            geometrical_shape=GeometricalShapeType.CIRCULAR_ARC,
            lcs=LCSType.Y_BY_POINT,
            lcs_rotation=45.0,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            system_line=SystemLineType.TOP,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam.geometrical_shape == GeometricalShapeType.CIRCULAR_ARC

    def test_beam_with_internal_nodes(self) -> None:
        """Test beam with internal (analysis) nodes."""
        beam = StructuralCurveMember(
            name="B4",
            cross_section="CS5",
            nodes=("N9", "N10"),
            segments=(SegmentType.LINE,),
            internal_nodes=("N77", "N78"),
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert len(beam.internal_nodes) == 2

    def test_beam_with_length(self) -> None:
        """Test beam with length property."""
        beam = StructuralCurveMember(
            name="B5",
            cross_section="CS6",
            nodes=("N11", "N12"),
            segments=(SegmentType.LINE,),
            length=6.425,
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam.length == pytest.approx(6.425)

    def test_beam_with_lcs_rotation(self) -> None:
        """Test beam with LCS rotation."""
        beam = StructuralCurveMember(
            name="B6",
            cross_section="CS7",
            nodes=("N13", "N14"),
            segments=(SegmentType.LINE,),
            lcs=LCSType.Y_BY_VECTOR,
            lcs_rotation=45.0,
            lcs_x=1.0,
            lcs_y=0.0,
            lcs_z=0.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam.lcs_rotation == 45.0

    def test_beam_with_eccentricities(self) -> None:
        """Test beam with structural and analysis eccentricities."""
        beam = StructuralCurveMember(
            name="B7",
            cross_section="CS8",
            nodes=("N15", "N16"),
            segments=(SegmentType.LINE,),
            structural_y_eccentricity_begin=-150.0,
            structural_y_eccentricity_end=75.0,
            structural_z_eccentricity_begin=0.0,
            structural_z_eccentricity_end=0.0,
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.TOP_LEFT,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=75.0,
            analysis_y_eccentricity_end=75.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam.structural_y_eccentricity_begin == -150.0
        assert beam.analysis_y_eccentricity_begin == 75.0

    def test_beam_with_layer(self) -> None:
        """Test beam with layer classification."""
        beam = StructuralCurveMember(
            name="B8",
            cross_section="CS9",
            nodes=("N17", "N18"),
            segments=(SegmentType.LINE,),
            layer="1st floor",
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam.layer == "1st floor"

    def test_beam_with_color(self) -> None:
        """Test beam with color."""
        beam = StructuralCurveMember(
            name="B9",
            cross_section="CS10",
            nodes=("N19", "N20"),
            segments=(SegmentType.LINE,),
            color="#7FFFFF00",
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam.color == "#7FFFFF00"

    def test_beam_with_behaviour_types(self) -> None:
        """Test beam with different behaviour types."""
        for behaviour in [
            BehaviourType.STANDARD,
            BehaviourType.AXIAL_FORCE_ONLY,
            BehaviourType.COMPRESSION_ONLY,
            BehaviourType.TENSION_ONLY,
        ]:
            beam = StructuralCurveMember(
                name="B10",
                cross_section="CS11",
                nodes=("N21", "N22"),
                segments=(SegmentType.LINE,),
                behaviour=behaviour,
                lcs=LCSType.Z_BY_VECTOR,
                lcs_rotation=0.0,
                lcs_x=0.0,
                lcs_y=0.0,
                lcs_z=1.0,
                system_line=SystemLineType.CENTRE,
                analysis_y_eccentricity_begin=0.0,
                analysis_y_eccentricity_end=0.0,
                analysis_z_eccentricity_begin=0.0,
                analysis_z_eccentricity_end=0.0,
            )
            assert beam.behaviour == behaviour

    def test_beam_with_different_system_lines(self) -> None:
        """Test beam with different system line types."""
        for system_line in [
            SystemLineType.CENTRE,
            SystemLineType.TOP,
            SystemLineType.BOTTOM,
            SystemLineType.LEFT,
            SystemLineType.RIGHT,
            SystemLineType.TOP_LEFT,
            SystemLineType.TOP_RIGHT,
            SystemLineType.BOTTOM_LEFT,
            SystemLineType.BOTTOM_RIGHT,
        ]:
            beam = StructuralCurveMember(
                name="B11",
                cross_section="CS12",
                nodes=("N23", "N24"),
                segments=(SegmentType.LINE,),
                system_line=system_line,
                lcs=LCSType.Z_BY_VECTOR,
                lcs_rotation=0.0,
                lcs_x=0.0,
                lcs_y=0.0,
                lcs_z=1.0,
                behaviour=BehaviourType.STANDARD,
                analysis_y_eccentricity_begin=0.0,
                analysis_y_eccentricity_end=0.0,
                analysis_z_eccentricity_begin=0.0,
                analysis_z_eccentricity_end=0.0,
            )
            assert beam.system_line == system_line


class TestStructuralCurveMemberValidation:
    """Test validation of StructuralCurveMember."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralCurveMember(
                name="",
                cross_section="CS1",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
                lcs=LCSType.Z_BY_VECTOR,
                lcs_rotation=0.0,
                lcs_x=0.0,
                lcs_y=0.0,
                lcs_z=1.0,
                system_line=SystemLineType.CENTRE,
                behaviour=BehaviourType.STANDARD,
                analysis_y_eccentricity_begin=0.0,
                analysis_y_eccentricity_end=0.0,
                analysis_z_eccentricity_begin=0.0,
                analysis_z_eccentricity_end=0.0,
            )

    def test_empty_cross_section_raises_error(self) -> None:
        """Test that empty cross_section raises ValueError."""
        with pytest.raises(ValueError, match="cross_section cannot be empty"):
            StructuralCurveMember(
                name="B1",
                cross_section="",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
                lcs=LCSType.Z_BY_VECTOR,
                lcs_rotation=0.0,
                lcs_x=0.0,
                lcs_y=0.0,
                lcs_z=1.0,
                system_line=SystemLineType.CENTRE,
                behaviour=BehaviourType.STANDARD,
                analysis_y_eccentricity_begin=0.0,
                analysis_y_eccentricity_end=0.0,
                analysis_z_eccentricity_begin=0.0,
                analysis_z_eccentricity_end=0.0,
            )

    def test_less_than_two_nodes_raises_error(self) -> None:
        """Test that fewer than 2 nodes raises ValueError."""
        with pytest.raises(ValueError, match="at least 2 nodes"):
            StructuralCurveMember(
                name="B1",
                cross_section="CS1",
                nodes=("N1",),
                segments=(),
                lcs=LCSType.Z_BY_VECTOR,
                lcs_rotation=0.0,
                lcs_x=0.0,
                lcs_y=0.0,
                lcs_z=1.0,
                system_line=SystemLineType.CENTRE,
                behaviour=BehaviourType.STANDARD,
                analysis_y_eccentricity_begin=0.0,
                analysis_y_eccentricity_end=0.0,
                analysis_z_eccentricity_begin=0.0,
                analysis_z_eccentricity_end=0.0,
            )

    def test_segment_count_mismatch_raises_error(self) -> None:
        """Test that segment count not matching nodes - 1 raises ValueError."""
        with pytest.raises(ValueError, match="segments length"):
            StructuralCurveMember(
                name="B1",
                cross_section="CS1",
                nodes=("N1", "N2", "N3"),
                segments=(SegmentType.LINE,),  # Should have 2
                lcs=LCSType.Z_BY_VECTOR,
                lcs_rotation=0.0,
                lcs_x=0.0,
                lcs_y=0.0,
                lcs_z=1.0,
                system_line=SystemLineType.CENTRE,
                behaviour=BehaviourType.STANDARD,
                analysis_y_eccentricity_begin=0.0,
                analysis_y_eccentricity_end=0.0,
                analysis_z_eccentricity_begin=0.0,
                analysis_z_eccentricity_end=0.0,
            )

    def test_empty_node_name_raises_error(self) -> None:
        """Test that empty node name raises ValueError."""
        with pytest.raises(ValueError, match="Node name at index"):
            StructuralCurveMember(
                name="B1",
                cross_section="CS1",
                nodes=("N1", ""),
                segments=(SegmentType.LINE,),
                lcs=LCSType.Z_BY_VECTOR,
                lcs_rotation=0.0,
                lcs_x=0.0,
                lcs_y=0.0,
                lcs_z=1.0,
                system_line=SystemLineType.CENTRE,
                behaviour=BehaviourType.STANDARD,
                analysis_y_eccentricity_begin=0.0,
                analysis_y_eccentricity_end=0.0,
                analysis_z_eccentricity_begin=0.0,
                analysis_z_eccentricity_end=0.0,
            )

    def test_empty_internal_node_name_raises_error(self) -> None:
        """Test that empty internal node name raises ValueError."""
        with pytest.raises(ValueError, match="Internal node name at index"):
            StructuralCurveMember(
                name="B1",
                cross_section="CS1",
                nodes=("N1", "N2"),
                segments=(SegmentType.LINE,),
                internal_nodes=("N77", ""),
                lcs=LCSType.Z_BY_VECTOR,
                lcs_rotation=0.0,
                lcs_x=0.0,
                lcs_y=0.0,
                lcs_z=1.0,
                system_line=SystemLineType.CENTRE,
                behaviour=BehaviourType.STANDARD,
                analysis_y_eccentricity_begin=0.0,
                analysis_y_eccentricity_end=0.0,
                analysis_z_eccentricity_begin=0.0,
                analysis_z_eccentricity_end=0.0,
            )


class TestEnums:
    """Test enum values."""

    def test_geometrical_shape_type_values(self) -> None:
        """Test GeometricalShapeType enum values."""
        assert GeometricalShapeType.LINE.value == "Line"
        assert GeometricalShapeType.CIRCULAR_ARC.value == "Circular Arc"
        assert GeometricalShapeType.PARABOLIC_ARC.value == "Parabolic Arc"
        assert GeometricalShapeType.BEZIER.value == "Bezier"
        assert GeometricalShapeType.SPLINE.value == "Spline"
        assert GeometricalShapeType.POLYLINE.value == "Polyline"

    def test_lcs_type_values(self) -> None:
        """Test LCSType enum values."""
        assert LCSType.Y_BY_VECTOR.value == "y by vector"
        assert LCSType.Z_BY_VECTOR.value == "z by vector"
        assert LCSType.Y_BY_POINT.value == "y by point"
        assert LCSType.Z_BY_POINT.value == "z by point"

    def test_system_line_type_values(self) -> None:
        """Test SystemLineType enum values."""
        assert SystemLineType.CENTRE.value == "Centre"
        assert SystemLineType.TOP.value == "Top"
        assert SystemLineType.BOTTOM.value == "Bottom"
        assert SystemLineType.TOP_LEFT.value == "Top left"

    def test_behaviour_type_values(self) -> None:
        """Test BehaviourType enum values."""
        assert BehaviourType.STANDARD.value == "Standard"
        assert BehaviourType.AXIAL_FORCE_ONLY.value == "Axial force only"
        assert BehaviourType.COMPRESSION_ONLY.value == "Compression only"
        assert BehaviourType.TENSION_ONLY.value == "Tension only"

    def test_segment_type_values(self) -> None:
        """Test SegmentType enum values."""
        assert SegmentType.LINE.value == "Line"
        assert SegmentType.CIRCULAR_ARC.value == "Circular Arc"
        assert SegmentType.BEZIER.value == "Bezier"


class TestStructuralCurveMemberImmutability:
    """Test immutability of StructuralCurveMember."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        beam = StructuralCurveMember(
            name="B1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        with pytest.raises(Exception):
            beam.name = "B2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that member can be used in sets."""
        beam = StructuralCurveMember(
            name="B1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        beam_set = {beam}
        assert beam in beam_set


class TestStructuralCurveMemberEquality:
    """Test equality of StructuralCurveMember."""

    def test_equal_members(self) -> None:
        """Test that identical members are equal."""
        beam1 = StructuralCurveMember(
            name="B1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        beam2 = StructuralCurveMember(
            name="B1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam1 == beam2

    def test_unequal_members_different_names(self) -> None:
        """Test that members with different names are not equal."""
        beam1 = StructuralCurveMember(
            name="B1",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        beam2 = StructuralCurveMember(
            name="B2",
            cross_section="CS1",
            nodes=("N1", "N2"),
            segments=(SegmentType.LINE,),
            lcs=LCSType.Z_BY_VECTOR,
            lcs_rotation=0.0,
            lcs_x=0.0,
            lcs_y=0.0,
            lcs_z=1.0,
            system_line=SystemLineType.CENTRE,
            behaviour=BehaviourType.STANDARD,
            analysis_y_eccentricity_begin=0.0,
            analysis_y_eccentricity_end=0.0,
            analysis_z_eccentricity_begin=0.0,
            analysis_z_eccentricity_end=0.0,
        )
        assert beam1 != beam2
