"""Formula 8.13 from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot13UnityCheckTensileStrength(ComparisonFormula):
    r"""Class representing formula 8.13 for the unity check for tensile strength."""

    label = "8.13"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        n_ed: N,
        n_t_rd: N,
    ) -> None:
        r"""Unity check for tensile strength of an element in tension.

        EN 1993-1-1:2025 art.8.2.3(1) - Formula (8.13)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design value of the normal tensile force [$N$].
        n_t_rd : N
            [$N_{t,Rd}$] Design value of the resistance against tensile force [$N$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_t_rd = n_t_rd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        n_ed: N,
        n_t_rd: N,
    ) -> float:
        """Evaluates the left-hand side of the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_t_rd=n_t_rd)
        raise_if_negative(n_ed=n_ed)
        return n_ed / n_t_rd

    @staticmethod
    def _evaluate_rhs(*_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the formula, for more information see the __init__ method."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.13."""
        _equation: str = r"\left( \frac{N_{Ed}}{N_{t,Rd}} \leq 1 \right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                "N_{Ed}": f"{self.n_ed:.{n}f}",
                "N_{t,Rd}": f"{self.n_t_rd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
