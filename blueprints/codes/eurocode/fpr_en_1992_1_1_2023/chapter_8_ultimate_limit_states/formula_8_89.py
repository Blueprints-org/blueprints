"""Formula 8.89 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot89CheckMaximumPunchingShearResistance(ComparisonFormula):
    r"""Class representing formula 8.89 for the check of the maximum punching shear resistance at the control
    perimeter.

    This is item c) of the punching shear procedure of 8.4.1(2), which runs from a) to e). Unlike Formulas (8.87)
    and (8.88) it is a requirement: it applies where [$\tau_{Ed} > \tau_{Rd,c}$], so where punching shear
    reinforcement is needed, and it may not be exceeded no matter how much reinforcement is provided. A result of
    ``Not OK`` means the cross-section itself is too small.

    The class checks the design stress against [$\tau_{Rd,max}$], it does not produce that maximum. Its value
    follows from 8.4.4(5) and (6) and is an input here.
    """

    label = "8.89"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, tau_ed: MPA, tau_rd_max: MPA) -> None:
        r"""Check whether the punching shear stress at the control perimeter does not exceed the maximum punching
        shear resistance.

        FprEN 1992-1-1:2023 (E) art. 8.4.1(2) - Formula (8.89)

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Design punching shear stress at the control perimeter [$b_{0,5}$] [$MPa$].
        tau_rd_max : MPA
            [$\tau_{Rd,max}$] Maximum punching shear resistance at the control perimeter [$b_{0,5}$], according to
            8.4.4(5) and (6) [$MPa$].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.tau_rd_max = tau_rd_max

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(tau_ed: MPA, *_args, **_kwargs) -> float:
        """Evaluates the punching shear stress, for more information see the __init__ method."""
        raise_if_negative(tau_ed=tau_ed)

        return float(tau_ed)

    @staticmethod
    def _evaluate_rhs(tau_rd_max: MPA, *_args, **_kwargs) -> float:
        """Evaluates the maximum punching shear resistance, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(tau_rd_max=tau_rd_max)

        return float(tau_rd_max)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.89."""
        _equation: str = r"\tau_{Ed} \leq \tau_{Rd,max}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"\tau_{Rd,max}": f"{self.tau_rd_max:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
                r"\tau_{Rd,max}": rf"{self.tau_rd_max:.{n}f} \ MPa",
            },
            unique_symbol_check=True,
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
