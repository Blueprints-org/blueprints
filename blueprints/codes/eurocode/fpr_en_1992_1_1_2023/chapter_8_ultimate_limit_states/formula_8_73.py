"""Formula 8.73 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot73CheckShearStressAtInterface(ComparisonFormula):
    r"""Class representing formula 8.73 for the check of the shear stress at an interface."""

    label = "8.73"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, tau_edi: MPA, tau_rdi: MPA) -> None:
        r"""Check whether the shear stress at the interface does not exceed the shear resistance of that interface.

        FprEN 1992-1-1:2023 (E) art. 8.2.6(3) - Formula (8.73)

        Parameters
        ----------
        tau_edi : MPA
            [$\tau_{Edi}$] Design value of the shear stress in the interface according to Formula (8.74), or
            Formula (8.75) for composite action [$MPa$].
        tau_rdi : MPA
            [$\tau_{Rdi}$] Design shear resistance at the interface. If no reinforcement across the interface is
            required or if the required reinforcement across the interface is sufficiently anchored, it should be
            calculated by Formula (8.76). In other cases according to 8.2.6(7), Formula (8.77) should be used
            [$MPa$].
        """
        super().__init__()
        self.tau_edi = tau_edi
        self.tau_rdi = tau_rdi

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(tau_edi: MPA, *_args, **_kwargs) -> float:
        """Evaluates the shear stress at the interface, for more information see the __init__ method."""
        raise_if_negative(tau_edi=tau_edi)

        return float(tau_edi)

    @staticmethod
    def _evaluate_rhs(tau_rdi: MPA, *_args, **_kwargs) -> float:
        """Evaluates the shear resistance at the interface, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(tau_rdi=tau_rdi)

        return float(tau_rdi)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.73."""
        _equation: str = r"\tau_{Edi} \leq \tau_{Rdi}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Edi}": f"{self.tau_edi:.{n}f}",
                r"\tau_{Rdi}": f"{self.tau_rdi:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Edi}": rf"{self.tau_edi:.{n}f} \ MPa",
                r"\tau_{Rdi}": rf"{self.tau_rdi:.{n}f} \ MPa",
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
