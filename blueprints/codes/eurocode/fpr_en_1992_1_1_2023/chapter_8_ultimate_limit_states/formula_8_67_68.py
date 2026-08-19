"""Formula 8.67 and 8.68 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import operator
from collections.abc import Callable, Sequence
from typing import Literal, Self

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import AggregatedComparisonFormula, ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero

FLANGE_TYPE = Literal["compression", "tension"]


def _upper_bound(flange_type: FLANGE_TYPE) -> float:
    """Returns the upper bound on the cotangent, which is 3,0 in compression flanges per Formula (8.67) and
    1,25 in tension flanges per Formula (8.68).
    """
    limits = {"compression": 3.0, "tension": 1.25}
    limit = limits.get(flange_type.lower())
    if limit is None:
        raise ValueError(f"Invalid flange type: {flange_type}. Must be 'compression' or 'tension'.")
    return limit


class SubForm8Dot67To68LowerBound(ComparisonFormula):
    r"""Class representing the lower bound of formulas 8.67 and 8.68, [$1 \leq \cot\theta_f$].

    The standard prints the same lower bound for both flange types.
    """

    label = "8.67/8.68"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, cot_theta_f: DIMENSIONLESS) -> None:
        r"""Check the selected inclination of the compression field in the flange against its lower bound.

        FprEN 1992-1-1:2023 (E) art 8.2.5 (3) - Formula (8.67) and (8.68)

        Parameters
        ----------
        cot_theta_f : DIMENSIONLESS
            [$\cot\theta_f$] Cotangent of the selected inclination of the compression field in the flange
            with respect to the longitudinal axis [$-$].
        """
        super().__init__()
        self.cot_theta_f = cot_theta_f

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(*_args, **_kwargs) -> float:
        """Evaluates the lower bound, which the standard prints as the constant 1."""
        return 1.0

    @staticmethod
    def _evaluate_rhs(cot_theta_f: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the value under check, for more information see the __init__ method."""
        # A cotangent of zero or less is not the inclination of a compression field, and it must be refused
        # rather than reported as a failed check. ComparisonFormula.__bool__ answers through the unity check,
        # which for a lower bound written "constant <= value" is constant/value. A negative value flips the
        # sign of that ratio, so the bound would silently report OK, and a zero value divides by zero.
        raise_if_less_or_equal_to_zero(cot_theta_f=cot_theta_f)

        return float(cot_theta_f)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the lower bound."""
        _equation: str = r"1 \leq \cot(\theta_f)"
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=latex_replace_symbols(
                template=_equation,
                replacements={r"\cot(\theta_f)": f"{self.cot_theta_f:.{n}f}"},
                unique_symbol_check=False,
            ),
            comparison_operator_label=r"\to",
            unit="",
        )


class SubForm8Dot67To68UpperBound(ComparisonFormula):
    r"""Class representing the upper bound of formulas 8.67 and 8.68, [$\cot\theta_f \leq 3,0$] in compression
    flanges and [$\cot\theta_f \leq 1,25$] in tension flanges.
    """

    label = "8.67/8.68"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, cot_theta_f: DIMENSIONLESS, flange_type: FLANGE_TYPE) -> None:
        r"""Check the selected inclination of the compression field in the flange against its upper bound.

        FprEN 1992-1-1:2023 (E) art 8.2.5 (3) - Formula (8.67) and (8.68)

        Parameters
        ----------
        cot_theta_f : DIMENSIONLESS
            [$\cot\theta_f$] Cotangent of the selected inclination of the compression field in the flange [$-$].
        flange_type : FLANGE_TYPE
            Which of the two printed formulas applies: "compression" for Formula (8.67) or "tension" for
            Formula (8.68).
        """
        super().__init__()
        self.cot_theta_f = cot_theta_f
        self.flange_type = flange_type

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(cot_theta_f: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the value under check, for more information see the __init__ method."""
        # A cotangent of zero or less is not the inclination of a compression field, and it must be refused
        # rather than reported as a failed check. ComparisonFormula.__bool__ answers through the unity check,
        # which for a lower bound written "constant <= value" is constant/value. A negative value flips the
        # sign of that ratio, so the bound would silently report OK, and a zero value divides by zero.
        raise_if_less_or_equal_to_zero(cot_theta_f=cot_theta_f)

        return float(cot_theta_f)

    @staticmethod
    def _evaluate_rhs(flange_type: FLANGE_TYPE, *_args, **_kwargs) -> float:
        """Evaluates the upper bound, for more information see the __init__ method."""
        return _upper_bound(flange_type)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the upper bound."""
        _equation: str = r"\cot(\theta_f) \leq limit"
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=latex_replace_symbols(
                template=_equation,
                replacements={r"\cot(\theta_f)": f"{self.cot_theta_f:.{n}f}", "limit": f"{_upper_bound(self.flange_type):.{n}f}"},
                unique_symbol_check=False,
            ),
            comparison_operator_label=r"\to",
            unit="",
        )


class Form8Dot67To68CheckCotangentFlangeCompressionField(AggregatedComparisonFormula):
    r"""Class representing formulas 8.67 and 8.68 for the check of the cotangent of the inclination of the
    compression field in the flanges.

    The standard prints the two as separate numbered formulas with the same lower bound and a different upper
    bound: 3,0 in compression flanges and 1,25 in tension flanges. They are one rule selected by the state of
    the flange, so they are implemented as one class with that state as an input, the same way (8.22) to (8.24)
    are one class selected by a ratio.

    The printed range is one relation, but it is modelled as two comparisons joined with ``all`` so that each
    bound carries its own unity check. Those two are available through ``comparison_formulas``, and
    ``unity_check`` on this class is the larger of the two.
    """

    label = "8.67/8.68"
    source_document = FPR_EN_1992_1_1_2023

    def __new__(cls, cot_theta_f: DIMENSIONLESS, flange_type: FLANGE_TYPE) -> Self:
        """Translates the arguments of this formula into the aggregation the base class evaluates."""
        return super().__new__(cls, aggregation=all, comparison_formulas=cls._bounds(cot_theta_f, flange_type))

    def __init__(self, cot_theta_f: DIMENSIONLESS, flange_type: FLANGE_TYPE) -> None:
        r"""Check whether the selected inclination of the compression field in the flange lies within the
        permitted range.

        FprEN 1992-1-1:2023 (E) art 8.2.5 (3) - Formula (8.67) and (8.68)

        The standard lets the designer select the inclination, so this is a verification of that choice and
        not a value to be calculated. Both bounds are inclusive as printed. Lower angles in the tensile flange
        than those given here may be adopted under the conditions of 8.2.5(5), which is a separate route and
        not a relaxation of this check.

        Parameters
        ----------
        cot_theta_f : DIMENSIONLESS
            [$\cot\theta_f$] Cotangent of the selected inclination of the compression field in the flange
            with respect to the longitudinal axis [$-$].
        flange_type : FLANGE_TYPE
            Which of the two printed formulas applies: "compression" for Formula (8.67), which bounds the
            cotangent at 3,0, or "tension" for Formula (8.68), which bounds it at 1,25.
        """
        super().__init__(aggregation=all, comparison_formulas=self._bounds(cot_theta_f, flange_type))
        self.cot_theta_f = cot_theta_f
        self.flange_type = flange_type

    @staticmethod
    def _bounds(cot_theta_f: DIMENSIONLESS, flange_type: FLANGE_TYPE) -> Sequence[ComparisonFormula]:
        """Builds the two halves of the printed range."""
        return (
            SubForm8Dot67To68LowerBound(cot_theta_f=cot_theta_f),
            SubForm8Dot67To68UpperBound(cot_theta_f=cot_theta_f, flange_type=flange_type),
        )

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 8.67 and 8.68."""
        _equation: str = r"1 \leq \cot(\theta_f) \leq limit"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\cot(\theta_f)": f"{self.cot_theta_f:.{n}f}",
                "limit": f"{_upper_bound(self.flange_type):.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            # Every term here is dimensionless, so the representation with units is the same one.
            numeric_equation_with_units=_numeric_equation,
            comparison_operator_label=r"\to",
            unit="",
        )
