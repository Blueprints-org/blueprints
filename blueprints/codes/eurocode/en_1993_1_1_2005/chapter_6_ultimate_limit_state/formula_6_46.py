"""Formula 6.46 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

import operator
from collections.abc import Callable
from typing import Any

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot46BucklingResistanceOfMembersInCompression(ComparisonFormula):
    r"""Class representing formula 6.46 for the verification of a compression member against buckling.

    [$\frac{N_{Ed}}{N_{b,Rd}} \leq 1.0$]
    """

    label = "6.46"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        n_ed: N,
        n_b_rd: N,
    ) -> None:
        r"""Check whether the design value of the compression force does not exceed the design buckling resistance.

        EN 1993-1-1:2005 art.6.3.1.1(1) - Formula (6.46)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design value of the compression force [$N$].
        n_b_rd : N
            [$N_{b,Rd}$] Design buckling resistance of the compression member [$N$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_b_rd = n_b_rd

    @classmethod
    def _comparison_operator(cls) -> Callable[[Any, Any], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        n_ed: N,
        n_b_rd: N,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the left-hand side of the comparison, see __init__ for details."""
        raise_if_negative(n_ed=n_ed)
        raise_if_less_or_equal_to_zero(n_b_rd=n_b_rd)

        return n_ed / n_b_rd

    @staticmethod
    def _evaluate_rhs(*_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the comparison, see __init__ for details."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.46."""
        _equation: str = r"\frac{N_{Ed}}{N_{b,Rd}} \leq 1.0"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"N_{b,Rd}": f"{self.n_b_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"N_{b,Rd}": rf"{self.n_b_rd:.{n}f} \ N",
            },
            False,
        )
        _intermediate_result: str = rf"\left( {self.lhs:.{n}f} \leq 1.0 \right)"
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if bool(self) else r"\text{Not OK}",
            intermediate_result=_intermediate_result,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )
