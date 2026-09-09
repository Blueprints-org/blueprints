"""Formula 8.85 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable, Sequence
from typing import Self

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import AggregatedComparisonFormula, ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero


class SubForm8Dot85LowerBound(ComparisonFormula):
    r"""Class representing the lower bound of formula 8.85, [$1 / \cot\theta_{min} \leq \cot\theta$]."""

    label = "8.85"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, theta: DEG, theta_min: DEG) -> None:
        r"""Check the selected inclination of the compression field against its lower bound.

        FprEN 1992-1-1:2023 (E) art. 8.3.4(4) - Formula (8.85)

        Parameters
        ----------
        theta : DEG
            [$\theta$] Selected inclination of the compression field [$degrees$].
        theta_min : DEG
            [$\theta_{min}$] Minimal inclination of the compression field according to 8.2.3(4) [$degrees$].
        """
        super().__init__()
        self.theta = theta
        self.theta_min = theta_min

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(theta_min: DEG, *_args, **_kwargs) -> float:
        """Evaluates the lower bound, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(theta_min=theta_min)

        return float(1 / cot(theta_min))

    @staticmethod
    def _evaluate_rhs(theta: DEG, *_args, **_kwargs) -> float:
        """Evaluates the value under check, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(theta=theta)

        return float(cot(theta))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the lower bound of formula 8.85."""
        _equation: str = r"\frac{1}{\cot(\theta_{min})} \leq \cot(\theta)"
        _replacements = {r"\theta_{min}": f"{self.theta_min:.{n}f}", r"\theta": f"{self.theta:.{n}f}"}
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=latex_replace_symbols(template=_equation, replacements=_replacements, unique_symbol_check=False),
            comparison_operator_label=r"\to",
            unit="",
        )


class SubForm8Dot85UpperBound(ComparisonFormula):
    r"""Class representing the upper bound of formula 8.85, [$\cot\theta \leq \cot\theta_{min}$]."""

    label = "8.85"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, theta: DEG, theta_min: DEG) -> None:
        r"""Check the selected inclination of the compression field against its upper bound.

        FprEN 1992-1-1:2023 (E) art. 8.3.4(4) - Formula (8.85)

        Parameters
        ----------
        theta : DEG
            [$\theta$] Selected inclination of the compression field [$degrees$].
        theta_min : DEG
            [$\theta_{min}$] Minimal inclination of the compression field according to 8.2.3(4) [$degrees$].
        """
        super().__init__()
        self.theta = theta
        self.theta_min = theta_min

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(theta: DEG, *_args, **_kwargs) -> float:
        """Evaluates the value under check, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(theta=theta)

        return float(cot(theta))

    @staticmethod
    def _evaluate_rhs(theta_min: DEG, *_args, **_kwargs) -> float:
        """Evaluates the upper bound, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(theta_min=theta_min)

        return float(cot(theta_min))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the upper bound of formula 8.85."""
        _equation: str = r"\cot(\theta) \leq \cot(\theta_{min})"
        _replacements = {r"\theta_{min}": f"{self.theta_min:.{n}f}", r"\theta": f"{self.theta:.{n}f}"}
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=latex_replace_symbols(template=_equation, replacements=_replacements, unique_symbol_check=False),
            comparison_operator_label=r"\to",
            unit="",
        )


class Form8Dot85CheckCotangentCompressionFieldTorsion(AggregatedComparisonFormula):
    r"""Class representing formula 8.85 for the check of the cotangent of the inclination of the compression
    field used in the torsional resistances of Formulas (8.82) to (8.84).

    It is not the same range as Formula (8.41), even though both are bounded above by
    [$\cot\theta_{min}$] of 8.2.3(4). The lower bound here is [$1 / \cot\theta_{min}$] instead of the constant
    1, so torsion permits a flatter compression field than shear does, symmetric in [$\cot\theta$] about 1.

    The printed range is one relation, but it is modelled as two comparisons joined with ``all`` so that each
    bound carries its own unity check. Those two are available through ``comparison_formulas``, and
    ``unity_check`` on this class is the larger of the two, so it exceeds 1 as soon as either bound is violated.
    """

    label = "8.85"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, theta: DEG, theta_min: DEG) -> None:
        r"""Check whether the selected inclination of the compression field lies within the range the standard
        gives for usual cases of torsion.

        FprEN 1992-1-1:2023 (E) art. 8.3.4(4) - Formula (8.85)

        The standard lets the designer select the inclination, so this is a verification of that choice and not
        a value to be calculated. Both bounds are inclusive as printed, and the standard phrases the range as a
        recommendation for usual cases, so it is a check and not a hard limit inside Formulas (8.82) to (8.84).

        Parameters
        ----------
        theta : DEG
            [$\theta$] Selected inclination of the compression field, used in Formulas (8.82) to (8.84)
            [$degrees$].
        theta_min : DEG
            [$\theta_{min}$] Minimal inclination of the compression field according to 8.2.3(4). None of the
            rules that give it carries a formula number, so it is an input here [$degrees$].
        """
        super().__init__(aggregation=all, comparison_formulas=self._bounds(theta, theta_min))
        self.theta = theta
        self.theta_min = theta_min

    @staticmethod
    def _bounds(theta: DEG, theta_min: DEG) -> Sequence[ComparisonFormula]:
        """Builds the two halves of the printed range."""
        return (
            SubForm8Dot85LowerBound(theta=theta, theta_min=theta_min),
            SubForm8Dot85UpperBound(theta=theta, theta_min=theta_min),
        )

    def __new__(cls, theta: DEG, theta_min: DEG) -> Self:
        """Translates the arguments of this formula into the aggregation the base class evaluates."""
        return super().__new__(cls, aggregation=all, comparison_formulas=cls._bounds(theta, theta_min))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.85."""
        _equation: str = r"\frac{1}{\cot(\theta_{min})} \leq \cot(\theta) \leq \cot(\theta_{min})"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta_{min}": f"{self.theta_min:.{n}f}",
                r"\theta": f"{self.theta:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta_{min}": rf"{self.theta_min:.{n}f} ^\circ",
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )
