"""Formula 5.1 from EN 1993-1-1:2005: Chapter 5 - Structural Analysis."""

import operator
from collections.abc import Callable
from typing import Any, Literal

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_mismatch_sign


class Form5Dot1CriteriumDisregardSecondOrderEffects(ComparisonFormula):
    r"""Class representing formula 5.1 to check whether second order effects of a structure can be disregarded
    or not.
    """

    label = "5.1"
    source_document = EN_1993_1_1_2005

    def __init__(self, f_cr: N, f_ed: N, analysis_type: Literal["elastic", "plastic"]) -> None:
        r"""Check if second order effects of a structure can be disregarded.

        EN 1993-1-1:2005 - Formula (5.1)

        Parameters
        ----------
        f_cr: N
            [$F_{cr}$] Elastic critical buckling load for global instability mode based on initial elastic stiffness (N).
        f_ed: N
            [$F_{Ed}$] Design loading on the structure (N).
        analysis_type: Literal["elastic", "plastic"]
            Type of analysis being performed (elastic or plastic).
        """
        super().__init__()
        self.f_cr = f_cr
        self.f_ed = f_ed
        self.analysis_type = analysis_type

    @classmethod
    def _comparison_operator(cls) -> Callable[[Any, Any], bool]:
        return operator.ge

    @staticmethod
    def _evaluate_lhs(f_cr: N, f_ed: N, *_args, **_kwargs) -> float:
        """Evaluates the left-hand side of the comparison. See __init__ for details."""
        raise_if_mismatch_sign(f_cr=f_cr, f_ed=f_ed)
        return f_cr / f_ed

    @staticmethod
    def _limit(analysis_type: Literal["elastic", "plastic"]) -> float:
        """Returns the limit value for the comparison based on the analysis type."""
        analysis_type_map = {
            "elastic": 10,
            "plastic": 15,
        }

        limit = analysis_type_map.get(analysis_type.lower())

        if limit is None:
            raise ValueError(f"Invalid analysis type: {analysis_type}. Must be 'elastic' or 'plastic'.")
        return limit

    @staticmethod
    def _evaluate_rhs(analysis_type: Literal["elastic", "plastic"], *_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the comparison. See __init__ for details."""
        return Form5Dot1CriteriumDisregardSecondOrderEffects._limit(analysis_type=analysis_type)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 5.1."""
        limit = self._limit(analysis_type=self.analysis_type)
        _equation: str = r"\alpha_{cr} = \frac{F_{cr}}{F_{Ed}} \ge limit"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\alpha_{cr}": f"{(self.f_cr / self.f_ed):.{n}f}",
                "F_{cr}": f"{self.f_cr:.{n}f}",
                "F_{Ed}": f"{self.f_ed:.{n}f}",
                "limit": f"{limit:d}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol="CHECK",
            result=r"OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label=r"\to",
            unit="",
        )
