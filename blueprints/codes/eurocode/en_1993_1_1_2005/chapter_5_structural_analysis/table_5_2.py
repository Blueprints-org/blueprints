"""Table 5.2 from EN 1993-1-1:2005: Chapter 5 - Structural Analysis."""

import operator
from collections.abc import Callable
from enum import Enum, IntEnum
from math import sqrt
from typing import ClassVar

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula


class CrossSectionClass(IntEnum):
    """Cross-section classes as defined by EN 1993-1-1:2005 paragraf 5.5.2 Classification.

    - Class 1 cross-sections are those which can form a plastic hinge with the rotation
      capacity required from plastic analysis without reduction of the resistance.
    - Class 2 cross-sections arc those which can develop their plastic moment resistance,
      but have limited rotation capacity because of local buckling.
    - Class 3 cross-sections are those in which the stress in the extreme compression fibre
      of the steel member assuming an elastic distribution of stresses can reach the yield
      strength, but local buckling is liable to prevent development of the plastic moment
      resistance.
    - Class 4 cross-sections are those in which local buckling will occur before the
      attainment of yield stress in one or more parts of the cross-section.
    """

    CLASS_1 = 1
    CLASS_2 = 2
    CLASS_3 = 3
    CLASS_4 = 4


class Table5Dot2CompressionPart(Enum):
    """Compression part types covered by EN 1993-1-1:2005 Table 5.2.

    INTERNAL_COMPRESSION_PART: Internal compression parts are plate elements in compression
    that are supported along both longitudinal edges by adjacent material (e.g. webs of I-sections
    or plates in box sections), which increases their resistance to local buckling; their behavior
    is governed by the width-to-thickness ratio c/t relative to the bending axis.

    OUTSTAND_FLANGE: Outstand flanges are compression elements supported along only one
    longitudinal edge, with the other edge free (such as flange tips of I-sections or welded plates),
    making them more susceptible to local buckling and therefore subject to stricter c/t limits.

    ANGLE: Angles consist of two outstand legs connected at right angles; when in compression,
    each leg behaves similarly to an outstand flange with classification based on both
    height-to-thickness and height-plus-width-to-thickness ratios.

    TUBULAR_SECTION: Tubular sections (circular hollow sections) have compression uniformly
    distributed around a closed perimeter, providing high inherent stability against local buckling,
    with classification typically based on diameter-to-thickness ratios.
    """

    INTERNAL_COMPRESSION_PART = "Internal compression part"
    OUTSTAND_FLANGE = "Outstand flange"
    ANGLE = "Angle"
    TUBULAR_SECTION = "Tubular section"


class Table5Dot2LoadingCondition(Enum):
    """Loading conditions covered by EN 1993-1-1:2005 Table 5.2.

    SUBJECT_TO_BENDING: Compression elements primarily subjected to bending moments.
    SUBJECT_TO_COMPRESSION: Compression elements primarily subjected to axial compressive forces.
    SUBJECT_TO_BENDING_AND_COMPRESSION: Compression elements subjected to a combination of
    bending moments and axial compressive forces.
    """

    SUBJECT_TO_BENDING = "Bending"
    SUBJECT_TO_COMPRESSION = "Compression"
    SUBJECT_TO_BENDING_AND_COMPRESSION = "Bending and compression"
    SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_COMPRESSION = "Bending and compression (tip in compression)"
    SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_TENSION = "Bending and compression (tip in tension)"


class _MaximumWidthToThicknessRatio(ComparisonFormula):
    """Configurable base for all Table 5.2 width-to-thickness checks."""

    label = "Maximum width-to-thickness ratio"
    source_document = EN_1993_1_1_2005

    # Set by the factory on each generated class:
    _param_names: ClassVar[tuple[str, ...]]
    _lhs_fn: ClassVar[Callable[..., float]]
    _rhs_fn: ClassVar[Callable[..., float]]
    _lhs_latex: ClassVar[str]
    _rhs_latex: ClassVar[str]

    def __init__(self, *args, **kwargs) -> None:
        # Map positional args → named attributes using _param_names
        merged = {**dict(zip(type(self)._param_names, args)), **kwargs}  # noqa: SLF001
        for name in type(self)._param_names:  # noqa: SLF001
            setattr(self, name, merged[name])
        super().__init__(*args, **kwargs)

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Return the comparison operator for this formula."""
        return operator.le

    @classmethod
    def _evaluate_lhs(cls, *args, **kwargs) -> float:
        return cls._lhs_fn(*args, **kwargs)

    @classmethod
    def _evaluate_rhs(cls, *args, **kwargs) -> float:
        return cls._rhs_fn(*args, **kwargs)

    def latex(self, n: int = 3) -> LatexFormula:
        return LatexFormula(
            return_symbol=self._lhs_latex,
            result=f"{round(self.lhs / self.rhs, n):.{n}f}",
            equation=f"{self._lhs_latex} {self._comparison_operator().__name__} {self._rhs_latex}",
            numeric_equation=rf"{self.lhs:.{n}f} \leq {self.rhs:.{n}f}",
            comparison_operator_label=r"\leq",
        )


def _make_limit_class(
    name: str,
    params: tuple[str, ...],
    lhs_fn: Callable[..., float],
    rhs_fn: Callable[..., float],
    lhs_latex: str,
    rhs_latex: str,
) -> type[_MaximumWidthToThicknessRatio]:
    """Dynamically build a _MaximumWidthToThicknessRatio subclass."""
    return type(
        name,
        (_MaximumWidthToThicknessRatio,),
        {
            "_param_names": params,
            "_lhs_fn": staticmethod(lhs_fn),
            "_rhs_fn": staticmethod(rhs_fn),
            "_lhs_latex": lhs_latex,
            "_rhs_latex": rhs_latex,
        },
    )


class Table5Dot2MaximumWidthToThicknessRatio:
    """Proposal API for EN 1993-1-1:2005 Table 5.2."""

    label = "Table 5.2"
    source_document = EN_1993_1_1_2005
    _ratio_factor_mapping: ClassVar = {
        Table5Dot2CompressionPart.INTERNAL_COMPRESSION_PART: {
            CrossSectionClass.CLASS_1: {
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING: _make_limit_class(
                    name="Form5Dot2BendingCheckClass1",
                    params=("c", "t", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda epsilon, **_: 72 * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"72 \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION: _make_limit_class(
                    name="Form5Dot2CompressionCheckClass1",
                    params=("c", "t", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda epsilon, **_: 33 * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"33 \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION: _make_limit_class(
                    name="Form5Dot2BendingAndCompressionCheckClass1",
                    params=("c", "t", "alpha", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda alpha, epsilon, **_: 396 * epsilon / (13 * alpha - 1) if alpha > 0.5 else 36 * epsilon / alpha,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"\frac{396 \epsilon}{\left(13 \alpha - 1\right)} \text{ if } \alpha > 0.5 \text{ else } \frac{36 \epsilon}{\alpha}",
                ),
            },
            CrossSectionClass.CLASS_2: {
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING: _make_limit_class(
                    name="Form5Dot2InternalBendingClass2",
                    params=("c", "t", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda epsilon, **_: 83 * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"83 \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION: _make_limit_class(
                    name="Form5Dot2InternalCompressionClass2",
                    params=("c", "t", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda epsilon, **_: 38 * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"38 \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION: _make_limit_class(
                    name="Form5Dot2InternalBendingAndCompressionClass2",
                    params=("c", "t", "alpha", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda alpha, epsilon, **_: 456 * epsilon / (13 * alpha - 1) if alpha > 0.5 else 41.5 * epsilon / alpha,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"\frac{456 \epsilon}{13 \alpha - 1} \text{ if } \alpha > 0.5 \text{ else } \frac{41.5 \epsilon}{\alpha}",
                ),
            },
            CrossSectionClass.CLASS_3: {
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING: _make_limit_class(
                    name="Form5Dot2InternalBendingClass3",
                    params=("c", "t", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda epsilon, **_: 124 * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"124 \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION: _make_limit_class(
                    name="Form5Dot2InternalCompressionClass3",
                    params=("c", "t", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda epsilon, **_: 42 * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"42 \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION: _make_limit_class(
                    name="Form5Dot2InternalBendingAndCompressionClass3",
                    params=("c", "t", "psi", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda psi, epsilon, **_: 42 * epsilon / (0.67 + 0.33 * psi) if psi > -1 else 62 * epsilon * (1 - psi) * sqrt(-psi),
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=(
                        r"\frac{42 \epsilon}{0.67 + 0.33 \psi}"
                        r" \text{ if } \psi > -1 \text{ else }"
                        r" 62 \epsilon \left(1 - \psi\right) \sqrt{-\psi}"
                    ),
                ),
            },
        },
        Table5Dot2CompressionPart.OUTSTAND_FLANGE: {
            CrossSectionClass.CLASS_1: {
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION: _make_limit_class(
                    name="Form5Dot2OutstandBendingAndCompressionClass1",
                    params=("c", "t", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda epsilon, **_: 9 * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"9 \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_COMPRESSION: _make_limit_class(
                    name="Form5Dot2OutstandTipInCompressionClass1",
                    params=("c", "t", "alpha", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda alpha, epsilon, **_: 9 * epsilon / alpha,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"\frac{9 \epsilon}{\alpha}",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_TENSION: _make_limit_class(
                    name="Form5Dot2OutstandTipInTensionClass1",
                    params=("c", "t", "alpha", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda alpha, epsilon, **_: 9 * epsilon / (alpha * sqrt(alpha)),
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"\frac{9 \epsilon}{\alpha \sqrt{\alpha}}",
                ),
            },
            CrossSectionClass.CLASS_2: {
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION: _make_limit_class(
                    name="Form5Dot2OutstandCompressionClass2",
                    params=("c", "t", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda epsilon, **_: 10 * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"10 \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_COMPRESSION: _make_limit_class(
                    name="Form5Dot2OutstandTipInCompressionClass2",
                    params=("c", "t", "alpha", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda alpha, epsilon, **_: 10 * epsilon / alpha,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"\frac{10 \epsilon}{\alpha}",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_TENSION: _make_limit_class(
                    name="Form5Dot2OutstandTipInTensionClass2",
                    params=("c", "t", "alpha", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda alpha, epsilon, **_: 10 * epsilon / (alpha * sqrt(alpha)),
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"\frac{10 \epsilon}{\alpha \sqrt{\alpha}}",
                ),
            },
            CrossSectionClass.CLASS_3: {
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION: _make_limit_class(
                    name="Form5Dot2OutstandCompressionClass3",
                    params=("c", "t", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda epsilon, **_: 14 * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"14 \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_COMPRESSION: _make_limit_class(
                    name="Form5Dot2OutstandTipInCompressionClass3",
                    params=("c", "t", "k_sigma", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda k_sigma, epsilon, **_: 21 * sqrt(k_sigma) * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"21 \sqrt{k_{\sigma}} \epsilon",
                ),
                Table5Dot2LoadingCondition.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_TENSION: _make_limit_class(
                    name="Form5Dot2OutstandTipInTensionClass3",
                    params=("c", "t", "k_sigma", "epsilon"),
                    lhs_fn=lambda c, t, **_: c / t,
                    rhs_fn=lambda k_sigma, epsilon, **_: 21 * sqrt(k_sigma) * epsilon,
                    lhs_latex=r"\frac{c}{t}",
                    rhs_latex=r"21 \sqrt{k_{\sigma}} \epsilon",
                ),
            },
        },
        Table5Dot2CompressionPart.ANGLE: {
            CrossSectionClass.CLASS_3: {
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION: lambda h, b, t, epsilon: operator.le(h / t, 15 * epsilon)
                and operator.le((h + b) / (2 * t), 11.5 * epsilon),
            }
        },
        Table5Dot2CompressionPart.TUBULAR_SECTION: {
            CrossSectionClass.CLASS_1: {
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION: _make_limit_class(
                    name="Form5Dot2TubularCompressionClass1",
                    params=("d", "t", "epsilon"),
                    lhs_fn=lambda d, t, **_: d / t,
                    rhs_fn=lambda epsilon, **_: 50 * epsilon**2,
                    lhs_latex=r"\frac{d}{t}",
                    rhs_latex=r"50 \epsilon^2",
                ),
            },
            CrossSectionClass.CLASS_2: {
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION: _make_limit_class(
                    name="Form5Dot2TubularCompressionClass2",
                    params=("d", "t", "epsilon"),
                    lhs_fn=lambda d, t, **_: d / t,
                    rhs_fn=lambda epsilon, **_: 70 * epsilon**2,
                    lhs_latex=r"\frac{d}{t}",
                    rhs_latex=r"70 \epsilon^2",
                ),
            },
            CrossSectionClass.CLASS_3: {
                Table5Dot2LoadingCondition.SUBJECT_TO_COMPRESSION: _make_limit_class(
                    name="Form5Dot2TubularCompressionClass3",
                    params=("d", "t", "epsilon"),
                    lhs_fn=lambda d, t, **_: d / t,
                    rhs_fn=lambda epsilon, **_: 90 * epsilon**2,
                    lhs_latex=r"\frac{d}{t}",
                    rhs_latex=r"90 \epsilon^2",
                ),
            },
        },
    }

    def __init__(
        self,
        cross_section_class: CrossSectionClass | int,
        part: Table5Dot2CompressionPart,
        force_type: Table5Dot2LoadingCondition,
    ) -> None: ...

    def latex(
        self,
        cross_section_class: CrossSectionClass | int,
        part: Table5Dot2CompressionPart,
        force_type: Table5Dot2LoadingCondition,
        n: int = 3,
    ) -> LatexFormula:
        """Return a LaTeX explanation for the selected Table 5.2 limit."""
