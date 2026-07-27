"""Formula 8.41 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import operator
from collections.abc import Callable, Sequence
from typing import Self

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import AggregatedComparisonFormula, ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS


class SubForm8Dot41LowerBound(ComparisonFormula):
    r"""Class representing the lower bound of formula 8.41, [$1 \leq \cot\theta$]."""

    label = "8.41"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, cot_theta: DIMENSIONLESS) -> None:
        r"""Check the selected inclination of the compression field against its lower bound.

        FprEN 1992-1-1:2023 (E) art 8.2.3 (4) - Formula (8.41)

        Parameters
        ----------
        cot_theta : DIMENSIONLESS
            [$\cot\theta$] Cotangent of the selected inclination of the compression field [$-$].
        """
        super().__init__()
        self.cot_theta = cot_theta

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(*_args, **_kwargs) -> float:
        """Evaluates the lower bound, which the standard prints as the constant 1."""
        return 1.0

    @staticmethod
    def _evaluate_rhs(cot_theta: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the value under check, for more information see the __init__ method."""
        return float(cot_theta)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the lower bound of formula 8.41."""
        _equation: str = r"1 \leq \cot(\theta)"
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=latex_replace_symbols(
                template=_equation,
                replacements={r"\cot(\theta)": f"{self.cot_theta:.{n}f}"},
                unique_symbol_check=False,
            ),
            comparison_operator_label=r"\to",
            unit="",
        )


class SubForm8Dot41UpperBound(ComparisonFormula):
    r"""Class representing the upper bound of formula 8.41, [$\cot\theta \leq \cot\theta_{min}$]."""

    label = "8.41"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, cot_theta: DIMENSIONLESS, cot_theta_min: DIMENSIONLESS) -> None:
        r"""Check the selected inclination of the compression field against its upper bound.

        FprEN 1992-1-1:2023 (E) art 8.2.3 (4) - Formula (8.41)

        Parameters
        ----------
        cot_theta : DIMENSIONLESS
            [$\cot\theta$] Cotangent of the selected inclination of the compression field [$-$].
        cot_theta_min : DIMENSIONLESS
            [$\cot\theta_{min}$] Cotangent of the minimal inclination of the compression field [$-$].
        """
        super().__init__()
        self.cot_theta = cot_theta
        self.cot_theta_min = cot_theta_min

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(cot_theta: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the value under check, for more information see the __init__ method."""
        return float(cot_theta)

    @staticmethod
    def _evaluate_rhs(cot_theta_min: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the upper bound, for more information see the __init__ method."""
        return float(cot_theta_min)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the upper bound of formula 8.41."""
        _equation: str = r"\cot(\theta) \leq \cot(\theta_{min})"
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=latex_replace_symbols(
                template=_equation,
                replacements={
                    r"\cot(\theta_{min})": f"{self.cot_theta_min:.{n}f}",
                    r"\cot(\theta)": f"{self.cot_theta:.{n}f}",
                },
                unique_symbol_check=False,
            ),
            comparison_operator_label=r"\to",
            unit="",
        )


class Form8Dot41CheckCotangentCompressionFieldAngle(AggregatedComparisonFormula):
    r"""Class representing formula 8.41 for the check of the cotangent of the inclination of the compression
    field in the web carrying shear.

    The check is on [$\cot\theta$] and not on [$\theta$]. Since the cotangent decreases over the range of
    angles that apply here, the same check written in angles reverses direction, so the two are not
    interchangeable.

    The printed range is one relation, but it is modelled as two comparisons joined with ``all`` so that each
    bound carries its own unity check. Those two are available through ``comparison_formulas``, and
    ``unity_check`` on this class is the larger of the two, so it exceeds 1 as soon as either bound is violated.
    """

    label = "8.41"
    source_document = FPR_EN_1992_1_1_2023

    def __new__(cls, cot_theta: DIMENSIONLESS, cot_theta_min: DIMENSIONLESS) -> Self:
        """Translates the arguments of this formula into the aggregation the base class evaluates."""
        return super().__new__(cls, aggregation=all, comparison_formulas=cls._bounds(cot_theta, cot_theta_min))

    def __init__(self, cot_theta: DIMENSIONLESS, cot_theta_min: DIMENSIONLESS) -> None:
        r"""Check whether the selected inclination of the compression field lies within the permitted range.

        FprEN 1992-1-1:2023 (E) art 8.2.3 (4) - Formula (8.41)

        The standard lets the designer select the inclination, so this is a verification of that choice and
        not a value to be calculated. Both bounds are inclusive as printed.

        Parameters
        ----------
        cot_theta : DIMENSIONLESS
            [$\cot\theta$] Cotangent of the selected inclination of the compression field in the web
            carrying shear [$-$].
        cot_theta_min : DIMENSIONLESS
            [$\cot\theta_{min}$] Cotangent of the minimal inclination of the compression field. For shear
            reinforcement of ductility class B or C the standard gives 2,5 for ordinary reinforced members
            without axial force, 3,0 for members subjected to significant axial compressive force under the
            conditions of 8.2.3(4), with interpolation between 2,5 and 3,0 for intermediate cases, and
            [$2,5 - 0,1 \cdot N_{Ed}/|V_{Ed}| \geq 1,0$] for members subjected to axial tension. For ductility
            class A it shall be reduced by 20 %. None of these three values carries a formula number, so they
            are an input here rather than a separate class [$-$].
        """
        super().__init__(aggregation=all, comparison_formulas=self._bounds(cot_theta, cot_theta_min))
        self.cot_theta = cot_theta
        self.cot_theta_min = cot_theta_min

    @staticmethod
    def _bounds(cot_theta: DIMENSIONLESS, cot_theta_min: DIMENSIONLESS) -> Sequence[ComparisonFormula]:
        """Builds the two halves of the printed range."""
        return (
            SubForm8Dot41LowerBound(cot_theta=cot_theta),
            SubForm8Dot41UpperBound(cot_theta=cot_theta, cot_theta_min=cot_theta_min),
        )

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.41."""
        _equation: str = r"1 \leq \cot(\theta) \leq \cot(\theta_{min})"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\cot(\theta_{min})": f"{self.cot_theta_min:.{n}f}",
                r"\cot(\theta)": f"{self.cot_theta:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            # Both bounds and the value under check are dimensionless, so the representation with units is the same one.
            numeric_equation_with_units=_numeric_equation,
            comparison_operator_label=r"\to",
            unit="",
        )
