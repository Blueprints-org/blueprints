"""Table 5.2 from EN 1993-1-1:2005: Chapter 5 - Structural Analysis."""

import operator
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from math import sqrt
from typing import ClassVar, Final

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import AggregatedComparisonFormula, ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM


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


class Table5Dot2CompressionPart(StrEnum):
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


class Table5Dot2LoadingCondition(StrEnum):
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


# Substitution is a plain string replace, so parameters are wrapped in placeholders: a bare "c" would also
# match the "c" of \frac. Warning: the delimiter must be meaningless in latex; "%" would start a comment and swallow
# the rest of the equation.
_PLACEHOLDER: Final[str] = "@"
_PLACEHOLDER_PATTERN: Final[re.Pattern[str]] = re.compile(rf"{_PLACEHOLDER}(\w+){_PLACEHOLDER}")

# Latex symbol for every parameter that can appear in a Table 5.2 criterion.
_LATEX_SYMBOLS: Final[dict[str, str]] = {
    "c": "c",
    "t": "t",
    "h": "h",
    "b": "b",
    "d": "d",
    "alpha": r"\alpha",
    "psi": r"\psi",
    "k_sigma": r"k_{\sigma}",
    "epsilon": r"\epsilon",
}


def _format_value_for_latex(value: float, n: int) -> str:
    """Format a value for latex, parenthesising negatives so that they compose safely.

    Parameters
    ----------
    value : float
        The value to format.
    n : int
        The number of decimal places to round the value to.

    Returns
    -------
    str
        The formatted value.
    """
    return rf"\left({value:.{n}f}\right)" if value < 0 else f"{value:.{n}f}"


@dataclass(frozen=True)
class _TableCell:
    """Identifies one cell of Table 5.2: the three keys the table is indexed by."""

    part: Table5Dot2CompressionPart
    cross_section_class: CrossSectionClass
    loading_condition: Table5Dot2LoadingCondition

    def __str__(self) -> str:
        """Human readable description of the cell, used in error messages and formula names."""
        return f"{self.part.value}, class {self.cross_section_class.value:d}, {self.loading_condition.value.lower()}"


@dataclass(frozen=True)
class _LimitSpecification:
    r"""One width-to-thickness criterion of Table 5.2, as data: lhs <= rhs.

    Attributes
    ----------
    params : tuple[str, ...]
        Names of the parameters this criterion needs.
    lhs_fn : Callable[..., float]
        Evaluates the left-hand side (the width-to-thickness ratio) from the parameters.
    rhs_fn : Callable[..., float]
        Evaluates the right-hand side (the limit) from the parameters.
    lhs_latex : str
        Latex template of the left-hand side, e.g. ``r"\frac{@c@}{@t@}"``.
    rhs_latex : str
        Latex template of the right-hand side, e.g. ``r"72 \cdot @epsilon@"``.
    """

    params: tuple[str, ...]
    lhs_fn: Callable[..., float]
    rhs_fn: Callable[..., float]
    lhs_latex: str
    rhs_latex: str

    def __post_init__(self) -> None:
        """Check that the templates and the declared parameters describe the same criterion.

        This runs when the table below is built, so a criterion whose templates and parameters
        disagree is rejected on import instead of rendering a placeholder into the latex output.

        Raises
        ------
        ValueError
            If the placeholders in the templates are not exactly the declared parameters,
            or if a declared parameter has no latex symbol.
        """
        placeholders = set(_PLACEHOLDER_PATTERN.findall(f"{self.lhs_latex} {self.rhs_latex}"))
        if placeholders != set(self.params):
            raise ValueError(
                f"The latex templates of criterion '{self.lhs_latex} \\le {self.rhs_latex}' use placeholders "
                f"{sorted(placeholders)}, but the criterion declares parameters {sorted(self.params)}. They must match."
            )
        unknown = sorted(name for name in self.params if name not in _LATEX_SYMBOLS)
        if unknown:
            raise ValueError(f"No latex symbol is defined for {', '.join(unknown)}. Add it to _LATEX_SYMBOLS.")

    def collect_required_parameters(self, cell: _TableCell, **params: float | None) -> dict[str, float]:
        """Collect the parameters this criterion needs out of the provided ones.

        Parameters
        ----------
        cell : _TableCell
            The cell this criterion belongs to, used to build a readable error message.
        **params : float | None
            All parameters passed by the caller. Parameters not in ``self.params`` are ignored.

        Returns
        -------
        dict[str, float]
            The parameters this criterion needs.

        Raises
        ------
        ValueError
            If any of the required parameters was not provided.
        """
        missing = [name for name in self.params if params.get(name) is None]
        if missing:
            raise ValueError(f"Table 5.2 check for {cell} requires {', '.join(self.params)}; missing: {', '.join(missing)}.")
        return {name: params[name] for name in self.params}

    def render_latex_equation(self, replacements: dict[str, str]) -> str:
        """Render the criterion by replacing every ``@name@`` placeholder.

        Called twice per criterion: once with the latex symbols to get the symbolic equation, and once
        with the formatted values to get the numeric equation, so that the two can never drift apart.

        Parameters
        ----------
        replacements : dict[str, str]
            Replacement per parameter name, either a latex symbol or a formatted value.

        Returns
        -------
        str
            The rendered latex equation.
        """
        return latex_replace_symbols(
            template=f"{self.lhs_latex} \\le {self.rhs_latex}",
            replacements={f"{_PLACEHOLDER}{name}{_PLACEHOLDER}": replacements[name] for name in self.params},
            unique_symbol_check=False,
        )

    @property
    def symbolic_equation(self) -> str:
        """The criterion rendered with latex symbols instead of values."""
        return self.render_latex_equation(_LATEX_SYMBOLS)


class _MaximumWidthToThicknessRatio(ComparisonFormula):
    """A single width-to-thickness check from EN 1993-1-1:2005 Table 5.2."""

    label = "Table 5.2"
    source_document = EN_1993_1_1_2005

    def __init__(self, limit_spec: _LimitSpecification, table_cell: _TableCell, **params: float | None) -> None:
        """Check a single width-to-thickness criterion of Table 5.2 based on the provided limit specification.

        Parameters
        ----------
        limit_spec : _LimitSpecification
            The criterion to check.
        table_cell : _TableCell
            The cell of Table 5.2 the criterion was taken from.
        **params : float | None
            The parameters of the criterion. Parameters not needed by ``spec`` are ignored.
        """
        formula_parameters = limit_spec.collect_required_parameters(table_cell, **params)
        super().__init__()
        self.limit_spec = limit_spec
        self.table_cell = table_cell
        for name, value in formula_parameters.items():
            setattr(self, name, value)

    @property
    def name(self) -> str:
        """Description of which cell of the table this check comes from, and which criterion it is."""
        return f"Table 5.2 - {self.table_cell} - {self.limit_spec.symbolic_equation}"

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Return the comparison operator for this formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(spec: _LimitSpecification, table_cell: _TableCell, **params: float | None) -> float:
        """Evaluates the left-hand side of the comparison. See __init__ for details."""
        return spec.lhs_fn(**spec.collect_required_parameters(table_cell, **params))

    @staticmethod
    def _evaluate_rhs(spec: _LimitSpecification, table_cell: _TableCell, **params: float | None) -> float:
        """Evaluates the right-hand side of the comparison. See __init__ for details."""
        return spec.rhs_fn(**spec.collect_required_parameters(table_cell, **params))

    def latex(self, n: int = 3) -> LatexFormula:
        """Return the latex representation of the formula, given in math mode."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if bool(self) else r"\text{Not OK}",
            equation=self.limit_spec.symbolic_equation,
            numeric_equation=self.limit_spec.render_latex_equation(
                {name: _format_value_for_latex(getattr(self, name), n) for name in self.limit_spec.params}
            ),
            comparison_operator_label=r"\to",
        )


# Short aliases, used only to keep each cell of the table literal on one line.
_PART = Table5Dot2CompressionPart
_CLS = CrossSectionClass
_LOAD = Table5Dot2LoadingCondition


class Table5Dot2MaximumWidthToThicknessRatio(AggregatedComparisonFormula):
    r"""Class representing Table 5.2 which checks the maximum width-to-thickness ratio of a compression part.

    A cell of the table holds one criterion, except for angles in compression which hold two that must
    both be satisfied. The check is satisfied when all criteria of the selected cell are satisfied.
    """

    label = "Table 5.2"
    source_document = EN_1993_1_1_2005

    _ratio_factor_mapping: ClassVar[dict[_TableCell, tuple[_LimitSpecification, ...]]] = {
        # --- Internal compression parts ---
        _TableCell(_PART.INTERNAL_COMPRESSION_PART, _CLS.CLASS_1, _LOAD.SUBJECT_TO_BENDING): (
            _LimitSpecification(
                params=("c", "t", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda epsilon, **_: 72 * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"72 \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.INTERNAL_COMPRESSION_PART, _CLS.CLASS_1, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda epsilon, **_: 33 * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"33 \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.INTERNAL_COMPRESSION_PART, _CLS.CLASS_1, _LOAD.SUBJECT_TO_BENDING_AND_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "alpha", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda alpha, epsilon, **_: 396 * epsilon / (13 * alpha - 1) if alpha > 0.5 else 36 * epsilon / alpha,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=(
                    r"\frac{396 \cdot @epsilon@}{13 \cdot @alpha@ - 1}"
                    r" \text{ if } @alpha@ > 0.5 \text{ else }"
                    r" \frac{36 \cdot @epsilon@}{@alpha@}"
                ),
            ),
        ),
        _TableCell(_PART.INTERNAL_COMPRESSION_PART, _CLS.CLASS_2, _LOAD.SUBJECT_TO_BENDING): (
            _LimitSpecification(
                params=("c", "t", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda epsilon, **_: 83 * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"83 \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.INTERNAL_COMPRESSION_PART, _CLS.CLASS_2, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda epsilon, **_: 38 * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"38 \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.INTERNAL_COMPRESSION_PART, _CLS.CLASS_2, _LOAD.SUBJECT_TO_BENDING_AND_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "alpha", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda alpha, epsilon, **_: 456 * epsilon / (13 * alpha - 1) if alpha > 0.5 else 41.5 * epsilon / alpha,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=(
                    r"\frac{456 \cdot @epsilon@}{13 \cdot @alpha@ - 1}"
                    r" \text{ if } @alpha@ > 0.5 \text{ else }"
                    r" \frac{41.5 \cdot @epsilon@}{@alpha@}"
                ),
            ),
        ),
        _TableCell(_PART.INTERNAL_COMPRESSION_PART, _CLS.CLASS_3, _LOAD.SUBJECT_TO_BENDING): (
            _LimitSpecification(
                params=("c", "t", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda epsilon, **_: 124 * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"124 \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.INTERNAL_COMPRESSION_PART, _CLS.CLASS_3, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda epsilon, **_: 42 * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"42 \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.INTERNAL_COMPRESSION_PART, _CLS.CLASS_3, _LOAD.SUBJECT_TO_BENDING_AND_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "psi", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda psi, epsilon, **_: 42 * epsilon / (0.67 + 0.33 * psi) if psi > -1 else 62 * epsilon * (1 - psi) * sqrt(-psi),
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=(
                    r"\frac{42 \cdot @epsilon@}{0.67 + 0.33 \cdot @psi@}"
                    r" \text{ if } @psi@ > -1 \text{ else }"
                    r" 62 \cdot @epsilon@ \left(1 - @psi@\right) \sqrt{-@psi@}"
                ),
            ),
        ),
        # --- Outstand flanges ---
        _TableCell(_PART.OUTSTAND_FLANGE, _CLS.CLASS_1, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda epsilon, **_: 9 * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"9 \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.OUTSTAND_FLANGE, _CLS.CLASS_1, _LOAD.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "alpha", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda alpha, epsilon, **_: 9 * epsilon / alpha,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"\frac{9 \cdot @epsilon@}{@alpha@}",
            ),
        ),
        _TableCell(_PART.OUTSTAND_FLANGE, _CLS.CLASS_1, _LOAD.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_TENSION): (
            _LimitSpecification(
                params=("c", "t", "alpha", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda alpha, epsilon, **_: 9 * epsilon / (alpha * sqrt(alpha)),
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"\frac{9 \cdot @epsilon@}{@alpha@ \sqrt{@alpha@}}",
            ),
        ),
        _TableCell(_PART.OUTSTAND_FLANGE, _CLS.CLASS_2, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda epsilon, **_: 10 * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"10 \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.OUTSTAND_FLANGE, _CLS.CLASS_2, _LOAD.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "alpha", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda alpha, epsilon, **_: 10 * epsilon / alpha,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"\frac{10 \cdot @epsilon@}{@alpha@}",
            ),
        ),
        _TableCell(_PART.OUTSTAND_FLANGE, _CLS.CLASS_2, _LOAD.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_TENSION): (
            _LimitSpecification(
                params=("c", "t", "alpha", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda alpha, epsilon, **_: 10 * epsilon / (alpha * sqrt(alpha)),
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"\frac{10 \cdot @epsilon@}{@alpha@ \sqrt{@alpha@}}",
            ),
        ),
        _TableCell(_PART.OUTSTAND_FLANGE, _CLS.CLASS_3, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda epsilon, **_: 14 * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"14 \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.OUTSTAND_FLANGE, _CLS.CLASS_3, _LOAD.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_COMPRESSION): (
            _LimitSpecification(
                params=("c", "t", "k_sigma", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda k_sigma, epsilon, **_: 21 * sqrt(k_sigma) * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"21 \sqrt{@k_sigma@} \cdot @epsilon@",
            ),
        ),
        _TableCell(_PART.OUTSTAND_FLANGE, _CLS.CLASS_3, _LOAD.SUBJECT_TO_BENDING_AND_COMPRESSION_TIP_IN_TENSION): (
            _LimitSpecification(
                params=("c", "t", "k_sigma", "epsilon"),
                lhs_fn=lambda c, t, **_: c / t,
                rhs_fn=lambda k_sigma, epsilon, **_: 21 * sqrt(k_sigma) * epsilon,
                lhs_latex=r"\frac{@c@}{@t@}",
                rhs_latex=r"21 \sqrt{@k_sigma@} \cdot @epsilon@",
            ),
        ),
        # --- Angles ---
        _TableCell(_PART.ANGLE, _CLS.CLASS_3, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("h", "t", "epsilon"),
                lhs_fn=lambda h, t, **_: h / t,
                rhs_fn=lambda epsilon, **_: 15 * epsilon,
                lhs_latex=r"\frac{@h@}{@t@}",
                rhs_latex=r"15 \cdot @epsilon@",
            ),
            _LimitSpecification(
                params=("h", "b", "t", "epsilon"),
                lhs_fn=lambda h, b, t, **_: (h + b) / (2 * t),
                rhs_fn=lambda epsilon, **_: 11.5 * epsilon,
                lhs_latex=r"\frac{@h@ + @b@}{2 \cdot @t@}",
                rhs_latex=r"11.5 \cdot @epsilon@",
            ),
        ),
        # --- Tubular sections ---
        _TableCell(_PART.TUBULAR_SECTION, _CLS.CLASS_1, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("d", "t", "epsilon"),
                lhs_fn=lambda d, t, **_: d / t,
                rhs_fn=lambda epsilon, **_: 50 * epsilon**2,
                lhs_latex=r"\frac{@d@}{@t@}",
                rhs_latex=r"50 \cdot @epsilon@^2",
            ),
        ),
        _TableCell(_PART.TUBULAR_SECTION, _CLS.CLASS_2, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("d", "t", "epsilon"),
                lhs_fn=lambda d, t, **_: d / t,
                rhs_fn=lambda epsilon, **_: 70 * epsilon**2,
                lhs_latex=r"\frac{@d@}{@t@}",
                rhs_latex=r"70 \cdot @epsilon@^2",
            ),
        ),
        _TableCell(_PART.TUBULAR_SECTION, _CLS.CLASS_3, _LOAD.SUBJECT_TO_COMPRESSION): (
            _LimitSpecification(
                params=("d", "t", "epsilon"),
                lhs_fn=lambda d, t, **_: d / t,
                rhs_fn=lambda epsilon, **_: 90 * epsilon**2,
                lhs_latex=r"\frac{@d@}{@t@}",
                rhs_latex=r"90 \cdot @epsilon@^2",
            ),
        ),
    }

    def __init__(  # noqa: PLR0913
        self,
        cross_section_class: CrossSectionClass | int,
        part: Table5Dot2CompressionPart,
        loading_condition: Table5Dot2LoadingCondition,
        *,
        epsilon: DIMENSIONLESS,
        c: MM | None = None,
        t: MM | None = None,
        h: MM | None = None,
        b: MM | None = None,
        d: MM | None = None,
        alpha: DIMENSIONLESS | None = None,
        psi: DIMENSIONLESS | None = None,
        k_sigma: DIMENSIONLESS | None = None,
    ) -> None:
        r"""Check the maximum width-to-thickness ratio of a compression part.

        EN 1993-1-1:2005 - Table 5.2

        Only the parameters needed by the selected cell of the table have to be provided.

        Parameters
        ----------
        cross_section_class : CrossSectionClass | int
            The cross-section class to check the compression part against.
        part : Table5Dot2CompressionPart
            The type of compression part.
        loading_condition : Table5Dot2LoadingCondition
            The loading condition the compression part is subjected to.
        epsilon : DIMENSIONLESS
            [$\epsilon$] Material factor $\sqrt{235 / f_y}$ (-).
        c : MM | None
            [$c$] Width of the compression part (mm).
        t : MM | None
            [$t$] Thickness of the compression part (mm).
        h : MM | None
            [$h$] Height of the angle leg (mm).
        b : MM | None
            [$b$] Width of the angle leg (mm).
        d : MM | None
            [$d$] Diameter of the tubular section (mm).
        alpha : DIMENSIONLESS | None
            [$\alpha$] Ratio of the plastic compressed part of the compression part (-).
        psi : DIMENSIONLESS | None
            [$\psi$] Ratio of the elastic stresses at both ends of the compression part (-).
        k_sigma : DIMENSIONLESS | None
            [$k_{\sigma}$] Buckling factor of the compression part (-).
        """
        # The checks themselves were already built by __new__ through _define_aggregation; what is stored
        # here is the input of the check, so that the instance describes what it was asked to verify.
        super().__init__()
        self.cell = _TableCell(part, CrossSectionClass(cross_section_class), loading_condition)
        self.epsilon = epsilon
        self.c = c
        self.t = t
        self.h = h
        self.b = b
        self.d = d
        self.alpha = alpha
        self.psi = psi
        self.k_sigma = k_sigma

    @classmethod
    def _define_aggregation(
        cls,
        cross_section_class: CrossSectionClass | int,
        part: Table5Dot2CompressionPart,
        loading_condition: Table5Dot2LoadingCondition,
        **params: float | None,
    ) -> tuple[Callable[[Iterable[bool]], bool], list[_MaximumWidthToThicknessRatio]]:
        """Build the checks of the selected cell of the table. See __init__ for details.

        Returns
        -------
        tuple[Callable[[Iterable[bool]], bool], list[_MaximumWidthToThicknessRatio]]
            The ``all`` aggregation and the checks of the selected cell.

        Raises
        ------
        ValueError
            If Table 5.2 does not define a limit for the given combination.
        """
        table_cell = _TableCell(part, CrossSectionClass(cross_section_class), loading_condition)
        limit_specs = cls._ratio_factor_mapping.get(table_cell)
        if limit_specs is None:
            raise ValueError(f"Table 5.2 does not define a limit for {table_cell}.")
        return all, [_MaximumWidthToThicknessRatio(limit_spec, table_cell, **params) for limit_spec in limit_specs]
