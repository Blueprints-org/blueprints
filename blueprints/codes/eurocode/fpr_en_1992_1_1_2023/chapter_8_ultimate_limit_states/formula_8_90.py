"""Formula 8.90 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot90CheckPunchingShearResistanceWithReinforcement(ComparisonFormula):
    r"""Class representing formula 8.90 for the check of the punching shear resistance of a slab with punching
    shear reinforcement.

    This is item d) of the punching shear procedure of 8.4.1(2), which runs from a) to e). It is the condition the
    provided punching shear reinforcement has to satisfy where reinforcement is required, so it is a requirement
    and not a permission.

    Satisfying it is not on its own enough to conclude that the punching verification passes. The standard couples
    it to the detailing rules of 12.5.1, item c) requires Formula (8.89) at the same control perimeter, and item
    e) requires a further control perimeter [$b_{0,5,out}$] to be checked according to 8.4.4(7) or (8). None of
    those are in the scope of this class.
    """

    label = "8.90"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, tau_ed: MPA, tau_rd_cs: MPA) -> None:
        r"""Check whether the punching shear stress at the control perimeter does not exceed the punching shear
        stress resistance of the slab with punching shear reinforcement.

        FprEN 1992-1-1:2023 (E) art. 8.4.1(2) - Formula (8.90)

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Design punching shear stress at the control perimeter [$b_{0,5}$] [$MPa$].
        tau_rd_cs : MPA
            [$\tau_{Rd,cs}$] Design punching shear stress resistance of the slab with punching shear
            reinforcement, according to 8.4.4(1) to (4) and complying with the detailing rules of 12.5.1 [$MPa$].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.tau_rd_cs = tau_rd_cs

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
    def _evaluate_rhs(tau_rd_cs: MPA, *_args, **_kwargs) -> float:
        """Evaluates the punching shear stress resistance, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(tau_rd_cs=tau_rd_cs)

        return float(tau_rd_cs)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.90."""
        _equation: str = r"\tau_{Ed} \leq \tau_{Rd,cs}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"\tau_{Rd,cs}": f"{self.tau_rd_cs:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
                r"\tau_{Rd,cs}": rf"{self.tau_rd_cs:.{n}f} \ MPa",
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
