"""Tests for StructuralCurveMemberVarying SAF class."""

import pytest

from blueprints.saf.structural_analysis_elements.structural_curve_member_varying import (
    AlignmentType,
    StructuralCurveMemberVarying,
    VaryingSegment,
)


class TestValidInitialization:
    """Test valid initialization of StructuralCurveMemberVarying."""

    def test_single_segment_prismatic(self) -> None:
        """Test single prismatic segment (same cross-section at start and end)."""
        segment = VaryingSegment(
            cross_section_start="CS1",
            cross_section_end="CS1",
            span=1.0,
            alignment=AlignmentType.CENTRE,
        )
        varying = StructuralCurveMemberVarying(name="AD1", segments=(segment,))
        assert varying.name == "AD1"
        assert len(varying.segments) == 1
        assert varying.segments[0].span == 1.0

    def test_single_segment_tapered(self) -> None:
        """Test single tapered segment (different cross-sections)."""
        segment = VaryingSegment(
            cross_section_start="CS1",
            cross_section_end="CS2",
            span=1.0,
            alignment=AlignmentType.CENTRE,
        )
        varying = StructuralCurveMemberVarying(name="AD2", segments=(segment,))
        assert varying.segments[0].cross_section_start == "CS1"
        assert varying.segments[0].cross_section_end == "CS2"

    def test_multiple_segments_equal_span(self) -> None:
        """Test multiple segments with equal spans."""
        segments = (
            VaryingSegment("CS1", "CS2", 0.5, AlignmentType.CENTRE),
            VaryingSegment("CS2", "CS1", 0.5, AlignmentType.TOP),
        )
        varying = StructuralCurveMemberVarying(name="AD3", segments=segments)
        assert len(varying.segments) == 2
        assert sum(s.span for s in varying.segments) == pytest.approx(1.0)

    def test_multiple_segments_unequal_span(self) -> None:
        """Test multiple segments with unequal spans."""
        segments = (
            VaryingSegment("CS1", "CS2", 0.3, AlignmentType.CENTRE),
            VaryingSegment("CS2", "CS3", 0.4, AlignmentType.TOP),
            VaryingSegment("CS3", "CS1", 0.3, AlignmentType.BOTTOM),
        )
        varying = StructuralCurveMemberVarying(name="AD4", segments=segments)
        assert len(varying.segments) == 3

    def test_segment_with_all_alignments(self) -> None:
        """Test segments with different alignment types."""
        alignments = [
            AlignmentType.CENTRE,
            AlignmentType.TOP,
            AlignmentType.BOTTOM,
            AlignmentType.LEFT,
            AlignmentType.RIGHT,
            AlignmentType.TOP_LEFT,
            AlignmentType.TOP_RIGHT,
            AlignmentType.BOTTOM_LEFT,
            AlignmentType.BOTTOM_RIGHT,
        ]
        for alignment in alignments:
            segment = VaryingSegment("CS1", "CS2", 1.0, alignment)
            varying = StructuralCurveMemberVarying(name="AD", segments=(segment,))
            assert varying.segments[0].alignment == alignment

    def test_with_uuid(self) -> None:
        """Test with UUID identifier."""
        segment = VaryingSegment("CS1", "CS1", 1.0, AlignmentType.CENTRE)
        varying = StructuralCurveMemberVarying(
            name="AD5",
            segments=(segment,),
            id="39f238a5-01d0-45cf-a2eb-958170fd4f39",
        )
        assert varying.id == "39f238a5-01d0-45cf-a2eb-958170fd4f39"

    def test_many_segments(self) -> None:
        """Test with many segments."""
        span_per_segment = 1.0 / 10
        segments = tuple(VaryingSegment(f"CS{i}", f"CS{i + 1}", span_per_segment, AlignmentType.CENTRE) for i in range(10))
        varying = StructuralCurveMemberVarying(name="AD6", segments=segments)
        assert len(varying.segments) == 10
        assert sum(s.span for s in varying.segments) == pytest.approx(1.0)


class TestValidation:
    """Test validation of StructuralCurveMemberVarying."""

    def test_empty_name_raises_error(self) -> None:
        """Test that empty name raises ValueError."""
        segment = VaryingSegment("CS1", "CS1", 1.0, AlignmentType.CENTRE)
        with pytest.raises(ValueError, match="name cannot be empty"):
            StructuralCurveMemberVarying(name="", segments=(segment,))

    def test_empty_segments_raises_error(self) -> None:
        """Test that empty segments raises ValueError."""
        with pytest.raises(ValueError, match="segments must contain at least"):
            StructuralCurveMemberVarying(name="AD", segments=())

    def test_empty_cross_section_start_raises_error(self) -> None:
        """Test that empty cross_section_start raises ValueError."""
        segment = VaryingSegment("", "CS2", 1.0, AlignmentType.CENTRE)
        with pytest.raises(ValueError, match="cross_section_start"):
            StructuralCurveMemberVarying(name="AD", segments=(segment,))

    def test_empty_cross_section_end_raises_error(self) -> None:
        """Test that empty cross_section_end raises ValueError."""
        segment = VaryingSegment("CS1", "", 1.0, AlignmentType.CENTRE)
        with pytest.raises(ValueError, match="cross_section_end"):
            StructuralCurveMemberVarying(name="AD", segments=(segment,))

    def test_span_less_than_zero_raises_error(self) -> None:
        """Test that span < 0.0 raises ValueError."""
        segment = VaryingSegment("CS1", "CS2", -0.1, AlignmentType.CENTRE)
        with pytest.raises(ValueError, match="span"):
            StructuralCurveMemberVarying(name="AD", segments=(segment,))

    def test_span_greater_than_one_raises_error(self) -> None:
        """Test that span > 1.0 raises ValueError."""
        segment = VaryingSegment("CS1", "CS2", 1.1, AlignmentType.CENTRE)
        with pytest.raises(ValueError, match="span"):
            StructuralCurveMemberVarying(name="AD", segments=(segment,))

    def test_spans_not_summing_to_one_raises_error(self) -> None:
        """Test that spans not summing to 1.0 raises ValueError."""
        segments = (
            VaryingSegment("CS1", "CS2", 0.4, AlignmentType.CENTRE),
            VaryingSegment("CS2", "CS3", 0.4, AlignmentType.TOP),
        )
        with pytest.raises(ValueError, match=r"sum of all spans must equal 1.0"):
            StructuralCurveMemberVarying(name="AD", segments=segments)

    def test_spans_sum_to_one_with_tolerance(self) -> None:
        """Test that spans summing to ~1.0 within tolerance are accepted."""
        segments = (
            VaryingSegment("CS1", "CS2", 0.3333333333, AlignmentType.CENTRE),
            VaryingSegment("CS2", "CS3", 0.3333333334, AlignmentType.TOP),
            VaryingSegment("CS3", "CS1", 0.3333333333, AlignmentType.BOTTOM),
        )
        varying = StructuralCurveMemberVarying(name="AD", segments=segments)
        assert len(varying.segments) == 3


class TestEnums:
    """Test enum values."""

    def test_alignment_type_values(self) -> None:
        """Test AlignmentType enum values."""
        assert AlignmentType.CENTRE.value == "Centre"
        assert AlignmentType.TOP.value == "Top"
        assert AlignmentType.BOTTOM.value == "Bottom"
        assert AlignmentType.LEFT.value == "Left"
        assert AlignmentType.RIGHT.value == "Right"
        assert AlignmentType.TOP_LEFT.value == "Top left"
        assert AlignmentType.TOP_RIGHT.value == "Top right"
        assert AlignmentType.BOTTOM_LEFT.value == "Bottom left"
        assert AlignmentType.BOTTOM_RIGHT.value == "Bottom right"


class TestImmutability:
    """Test immutability of StructuralCurveMemberVarying."""

    def test_frozen_dataclass(self) -> None:
        """Test that dataclass is frozen."""
        segment = VaryingSegment("CS1", "CS1", 1.0, AlignmentType.CENTRE)
        varying = StructuralCurveMemberVarying(name="AD1", segments=(segment,))
        with pytest.raises(Exception):
            varying.name = "AD2"  # type: ignore[misc]

    def test_hashable(self) -> None:
        """Test that varying member can be used in sets."""
        segment = VaryingSegment("CS1", "CS1", 1.0, AlignmentType.CENTRE)
        varying = StructuralCurveMemberVarying(name="AD1", segments=(segment,))
        varying_set = {varying}
        assert varying in varying_set


class TestEquality:
    """Test equality of StructuralCurveMemberVarying."""

    def test_equal_varying_members(self) -> None:
        """Test that identical varying members are equal."""
        segment = VaryingSegment("CS1", "CS2", 1.0, AlignmentType.CENTRE)
        varying1 = StructuralCurveMemberVarying(name="AD1", segments=(segment,))
        varying2 = StructuralCurveMemberVarying(name="AD1", segments=(segment,))
        assert varying1 == varying2

    def test_unequal_varying_members_different_names(self) -> None:
        """Test that varying members with different names are not equal."""
        segment = VaryingSegment("CS1", "CS2", 1.0, AlignmentType.CENTRE)
        varying1 = StructuralCurveMemberVarying(name="AD1", segments=(segment,))
        varying2 = StructuralCurveMemberVarying(name="AD2", segments=(segment,))
        assert varying1 != varying2

    def test_unequal_varying_members_different_segments(self) -> None:
        """Test that varying members with different segments are not equal."""
        segment1 = VaryingSegment("CS1", "CS2", 1.0, AlignmentType.CENTRE)
        segment2 = VaryingSegment("CS1", "CS3", 1.0, AlignmentType.TOP)
        varying1 = StructuralCurveMemberVarying(name="AD1", segments=(segment1,))
        varying2 = StructuralCurveMemberVarying(name="AD1", segments=(segment2,))
        assert varying1 != varying2


class TestVaryingSegment:
    """Test VaryingSegment NamedTuple."""

    def test_segment_creation(self) -> None:
        """Test segment creation with all parameters."""
        segment = VaryingSegment("CS1", "CS2", 0.5, AlignmentType.TOP)
        assert segment.cross_section_start == "CS1"
        assert segment.cross_section_end == "CS2"
        assert segment.span == 0.5
        assert segment.alignment == AlignmentType.TOP

    def test_segment_immutability(self) -> None:
        """Test that segment is immutable."""
        segment = VaryingSegment("CS1", "CS2", 0.5, AlignmentType.TOP)
        with pytest.raises(AttributeError):
            segment.span = 0.6  # type: ignore[misc]
