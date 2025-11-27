"""Formula 5.1 from NEN-EN 1993-1-1:2006: Chapter 5 - Structural Analysis."""

import operator
from collections.abc import Callable
from typing import Any

from blueprints.codes.eurocode.nen_en_1993_1_1_2006 import EN_1993_1_1_2006
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_mismatch_sign


class From5Dot1CriteriumDisregardSecondOrderEffects(ComparisonFormula):
    r"""Class representing formula 5.1 to check whether second order effects of a structure can be disregarded
    or not.
    """

    label = "5.1"
    source_document = EN_1993_1_1_2006

    def __init__(self, f_cr: N, f_ed: N) -> None:
        r"""Check if second order effects of a structure can be disregarded.

        NEN-EN 1993-1-1:2006 - Formula (5.1)

        Parameters
        ----------
        f_cr: N
            [$F_{cr}$] Elastic critical buckling load for global instability mode based on initial elastic stiffness.
        f_ed: N
            [$F_{Ed}$] Design loading on the structure.
        """
        super().__init__()
        self.f_cr = f_cr
        self.f_ed = f_ed
        self._check_signs()

    def _check_signs(self) -> None:
        """Check whether signs of f_cr and f_ed match."""
        raise_if_mismatch_sign(f_cr=self.f_cr, f_ed=self.f_ed)

    @classmethod
    def _comparison_operator(cls) -> Callable[[Any, Any], bool]:
        return operator.ge

    @staticmethod
    def _evaluate_lhs(f_cr: N, f_ed: N, *args, **kwargs) -> float:  # noqa: ARG004
        """Evaluates the left-hand side of the comparison. See __init__ for details."""
        return f_cr / f_ed

    @staticmethod
    def _evaluate_rhs(*args, **kwargs) -> float:  # noqa: ARG004
        """Evaluates the right-hand side of the comparison. See __init__ for details."""
        return 10

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 5.1."""
        _equation: str = r"\alpha_{cr} = \frac{F_{cr}}{F_{Ed}} \ge 10"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_{cr}": f"{(self.f_cr / self.f_ed):.{n}f}",
                "F_{cr}": f"{self.f_cr:.{n}f}",
                "F_{Ed}": f"{self.f_ed:.{n}f}"},
            unique_symbol_check=False
        )
        return LatexFormula(
            return_symbol="CHECK",
            result=r"OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label=r"\to",
            unit=""
        )
