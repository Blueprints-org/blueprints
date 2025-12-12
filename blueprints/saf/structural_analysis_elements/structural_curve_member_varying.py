"""Curve member with varying cross-section definition for structural analysis following SAF specification.

A 1D structural member with a varying cross-section along its length.
"""

from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class AlignmentType(str, Enum):
    """Alignment of cross-section relative to reference axis following SAF specification.

    Defines how the cross-section is positioned relative to the analytical axis.
    """

    CENTRE = "Centre"
    TOP = "Top"
    BOTTOM = "Bottom"
    LEFT = "Left"
    RIGHT = "Right"
    TOP_LEFT = "Top left"
    TOP_RIGHT = "Top right"
    BOTTOM_LEFT = "Bottom left"
    BOTTOM_RIGHT = "Bottom right"


class VaryingSegment(NamedTuple):
    """Individual varying segment within a curve member.

    Attributes
    ----------
    cross_section_start : str
        Reference to StructuralCrossSection by name at segment start.
    cross_section_end : str
        Reference to StructuralCrossSection by name at segment end.
        For prismatic segments, this should be the same as cross_section_start.
    span : float
        Relative segment length (0.0 to 1.0). All spans must sum to 1.0.
    alignment : AlignmentType
        Cross-section positioning relative to original coordinate system.
    """

    cross_section_start: str
    cross_section_end: str
    span: float
    alignment: AlignmentType


@dataclass(frozen=True)
class StructuralCurveMemberVarying:
    """Structural curve member with varying cross-section following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralcurvemembervarying.html.

    A 1D structural member with a varying cross-section along its length. Each segment
    references cross-sections at start and end points for linear transitions, with
    alignment and span parameters.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "AD1").
    segments : tuple[VaryingSegment, ...]
        Varying segments with cross-sections and span parameters.
        Must contain at least 1 segment. All spans must sum to 1.0 (within tolerance).
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name is empty.
        If segments is empty.
        If any segment has empty cross-section names.
        If any segment span is not between 0.0 and 1.0.
        If total of all spans does not equal 1.0 (within tolerance).

    Examples
    --------
    >>> from blueprints.saf import StructuralCurveMemberVarying, VaryingSegment, AlignmentType
    >>> # Simple tapered member with one segment
    >>> segment = VaryingSegment(
    ...     cross_section_start="CS1",
    ...     cross_section_end="CS2",
    ...     span=1.0,
    ...     alignment=AlignmentType.CENTRE,
    ... )
    >>> varying = StructuralCurveMemberVarying(
    ...     name="AD1",
    ...     segments=(segment,),
    ... )

    >>> # Multi-segment varying member
    >>> segments = (
    ...     VaryingSegment("CS1", "CS2", 0.5, AlignmentType.CENTRE),
    ...     VaryingSegment("CS2", "CS1", 0.5, AlignmentType.TOP),
    ... )
    >>> varying_multi = StructuralCurveMemberVarying(
    ...     name="AD2",
    ...     segments=segments,
    ... )
    """

    name: str
    segments: tuple[VaryingSegment, ...]
    id: str = ""

    def __post_init__(self) -> None:
        """Validate varying member properties.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")

        if not self.segments:
            raise ValueError("segments must contain at least one VaryingSegment")

        # Validate all segments have non-empty cross-section names
        for i, segment in enumerate(self.segments):
            if not segment.cross_section_start:
                raise ValueError(f"cross_section_start at segment {i} cannot be empty")
            if not segment.cross_section_end:
                raise ValueError(f"cross_section_end at segment {i} cannot be empty")
            if segment.span < 0.0 or segment.span > 1.0:
                raise ValueError(f"span at segment {i} must be between 0.0 and 1.0, got {segment.span}")

        # Validate that all spans sum to 1.0 (with tolerance for floating point)
        total_span = sum(segment.span for segment in self.segments)
        tolerance = 1e-9
        if abs(total_span - 1.0) > tolerance:
            raise ValueError(f"sum of all spans must equal 1.0, got {total_span:.10f}")
