"""Formula 8.58 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import operator
from collections.abc import Callable, Sequence
from typing import Self

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import AggregatedComparisonFormula, ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS


class SubForm8Dot58LowerBound(ComparisonFormula):
    r"""Class representing the lower bound of formula 8.58, [$\tan(\alpha_w/2) \leq \cot\theta$]."""

    label = "8.58"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, cot_theta: DIMENSIONLESS, alpha_w: DEG) -> None:
        r"""Check the selected inclination of the compression field against its lower bound.

        FprEN 1992-1-1:2023 (E) art 8.2.3 (13) - Formula (8.58)

        Parameters
        ----------
        cot_theta : DIMENSIONLESS
            [$\cot\theta$] Cotangent of the selected inclination of the compression field [$-$].
        alpha_w : DEG
            [$\alpha_w$] Inclination of the shear reinforcement [$degrees$].
        """
        super().__init__()
        self.cot_theta = cot_theta
        self.alpha_w = alpha_w

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(alpha_w: DEG, *_args, **_kwargs) -> float:
        """Evaluates the lower bound, for more information see the __init__ method."""
        return float(np.tan(np.deg2rad(alpha_w) / 2))

    @staticmethod
    def _evaluate_rhs(cot_theta: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the value under check, for more information see the __init__ method."""
        return float(cot_theta)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the lower bound of formula 8.58."""
        _equation: str = r"\tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta)"
        _replacements = {r"\alpha_w": f"{self.alpha_w:.{n}f}", r"\cot(\theta)": f"{self.cot_theta:.{n}f}"}
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=latex_replace_symbols(template=_equation, replacements=_replacements, unique_symbol_check=False),
            comparison_operator_label=r"\to",
            unit="",
        )


class SubForm8Dot58UpperBound(ComparisonFormula):
    r"""Class representing the upper bound of formula 8.58, [$\cot\theta \leq \cot\theta_{min}$]."""

    label = "8.58"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, cot_theta: DIMENSIONLESS, cot_theta_min: DIMENSIONLESS) -> None:
        r"""Check the selected inclination of the compression field against its upper bound.

        FprEN 1992-1-1:2023 (E) art 8.2.3 (13) - Formula (8.58)

        Parameters
        ----------
        cot_theta : DIMENSIONLESS
            [$\cot\theta$] Cotangent of the selected inclination of the compression field [$-$].
        cot_theta_min : DIMENSIONLESS
            [$\cot\theta_{min}$] Cotangent of the minimal inclination according to 8.2.3(4) [$-$].
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
        """Returns LatexFormula object for the upper bound of formula 8.58."""
        _equation: str = r"\cot(\theta) \leq \cot(\theta_{min})"
        _replacements = {r"\cot(\theta_{min})": f"{self.cot_theta_min:.{n}f}", r"\cot(\theta)": f"{self.cot_theta:.{n}f}"}
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=latex_replace_symbols(template=_equation, replacements=_replacements, unique_symbol_check=False),
            comparison_operator_label=r"\to",
            unit="",
        )


class Form8Dot58CheckCotangentInclinedShearReinforcement(AggregatedComparisonFormula):
    r"""Class representing formula 8.58 for the check of the cotangent of the inclination of the compression
    field in members with inclined shear reinforcement.

    This replaces Formula (8.41) for such members. The only difference is the lower bound, which is
    [$\tan(\alpha_w/2)$] instead of the constant 1. For vertical shear reinforcement, [$\alpha_w = 90$] degrees,
    the two coincide because [$\tan(45) = 1$].

    The printed range is one relation, but it is modelled as two comparisons joined with ``all`` so that each
    bound carries its own unity check. Those two are available through ``comparison_formulas``, and
    ``unity_check`` on this class is the larger of the two, so it exceeds 1 as soon as either bound is violated.
    """

    label = "8.58"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, cot_theta: DIMENSIONLESS, cot_theta_min: DIMENSIONLESS, alpha_w: DEG) -> None:
        r"""Check whether the selected inclination of the compression field lies within the permitted range for
        members with inclined shear reinforcement.

        FprEN 1992-1-1:2023 (E) art 8.2.3 (13) - Formula (8.58)

        The standard lets the designer select the inclination, so this is a verification of that choice and not
        a value to be calculated. Both bounds are inclusive as printed.

        Parameters
        ----------
        cot_theta : DIMENSIONLESS
            [$\cot\theta$] Cotangent of the selected inclination of the compression field in the web
            carrying shear [$-$].
        cot_theta_min : DIMENSIONLESS
            [$\cot\theta_{min}$] Cotangent of the minimal inclination of the compression field according to
            8.2.3(4). None of the rules that give it carries a formula number, so it is an input here [$-$].
        alpha_w : DEG
            [$\alpha_w$] Inclination of the shear reinforcement, measured positive as shown in Figure 8.11 b).
            The standard gives this clause for [$45 \leq \alpha_w < 90$] degrees and states that angles above
            90 degrees should be avoided. That is a condition of application rather than a bound, so it is not
            enforced here [$degrees$].
        """
        super().__init__(aggregation=all, comparison_formulas=self._bounds(cot_theta, cot_theta_min, alpha_w))
        self.cot_theta = cot_theta
        self.cot_theta_min = cot_theta_min
        self.alpha_w = alpha_w

    @staticmethod
    def _bounds(cot_theta: DIMENSIONLESS, cot_theta_min: DIMENSIONLESS, alpha_w: DEG) -> Sequence[ComparisonFormula]:
        """Builds the two halves of the printed range."""
        return (
            SubForm8Dot58LowerBound(cot_theta=cot_theta, alpha_w=alpha_w),
            SubForm8Dot58UpperBound(cot_theta=cot_theta, cot_theta_min=cot_theta_min),
        )

    def __new__(cls, cot_theta: DIMENSIONLESS, cot_theta_min: DIMENSIONLESS, alpha_w: DEG) -> Self:
        """Translates the arguments of this formula into the aggregation the base class evaluates."""
        return super().__new__(cls, aggregation=all, comparison_formulas=cls._bounds(cot_theta, cot_theta_min, alpha_w))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.58."""
        _equation: str = r"\tan\left(\frac{\alpha_w}{2}\right) \leq \cot(\theta) \leq \cot(\theta_{min})"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_w": f"{self.alpha_w:.{n}f}",
                r"\cot(\theta_{min})": f"{self.cot_theta_min:.{n}f}",
                r"\cot(\theta)": f"{self.cot_theta:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_w": rf"{self.alpha_w:.{n}f} \ degrees",
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
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )
