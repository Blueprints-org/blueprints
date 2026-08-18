"""Formula 8.87 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot87CheckDetailedPunchingVerificationMayBeOmitted(ComparisonFormula):
    r"""Class representing formula 8.87 for the condition under which the detailed verification of the punching
    shear resistance may be omitted.

    This is item a) of the punching shear procedure of 8.4.1(2), which runs from a) to e). It states a permission
    and not a requirement: where the condition is satisfied the detailed verification may be skipped, and where it
    is not, the procedure simply carries on with Formula (8.88). A result of ``Not OK`` therefore does not mean
    that the slab fails, only that the shortcut does not apply.
    """

    label = "8.87"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, tau_ed: MPA, tau_rdc_min: MPA) -> None:
        r"""Check whether the punching shear stress at the control perimeter does not exceed the minimum shear
        stress resistance, in which case the detailed verification of the punching shear resistance may be omitted.

        FprEN 1992-1-1:2023 (E) art. 8.4.1(2) - Formula (8.87)

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Design punching shear stress at the control perimeter [$b_{0,5}$] [$MPa$].
        tau_rdc_min : MPA
            [$\tau_{Rdc,min}$] Minimum shear stress resistance according to 8.2.1(4) [$MPa$].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.tau_rdc_min = tau_rdc_min

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
    def _evaluate_rhs(tau_rdc_min: MPA, *_args, **_kwargs) -> float:
        """Evaluates the minimum shear stress resistance, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(tau_rdc_min=tau_rdc_min)

        return float(tau_rdc_min)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.87."""
        _equation: str = r"\tau_{Ed} \leq \tau_{Rdc,min}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"\tau_{Rdc,min}": f"{self.tau_rdc_min:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
                r"\tau_{Rdc,min}": rf"{self.tau_rdc_min:.{n}f} \ MPa",
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
