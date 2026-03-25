"""Formula 6.54 from EN 1993-1-1:2005: Chapter 6 - Ultimate limit state."""

import operator
from collections.abc import Callable
from typing import Any

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM
from blueprints.validations import (
    raise_if_less_or_equal_to_zero,
    raise_if_negative,
)


class Form6Dot54BucklingResistanceOfMembersInBending(ComparisonFormula):
    r"""Class representing formula 6.54 for buckling resistance.

    [$\frac{M_{Ed}}{M_{b,Rd}} \leq 1.0$]
    """

    label = "6.54"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        m_ed: NMM,
        m_b_rd: NMM,
    ) -> None:
        r"""Buckling resistance check for laterally unrestrained members.

        Members subject to major axis bending.

        EN 1993-1-1:2005 art. 6.3.2.1 (1) - Formula (6.54)

        Parameters
        ----------
        m_ed : NMM
            [$M_{Ed}$] Design value of the moment [$Nmm$].
        m_b_rd : NMM
            [$M_{b,Rd}$] Design buckling resistance moment [$Nmm$].
        """
        super().__init__()
        self.m_ed = m_ed
        self.m_b_rd = m_b_rd

    @classmethod
    def _comparison_operator(cls) -> Callable[[Any, Any], bool]:
        """Returns the comparison operator for this formula.

        LHS should be less than or equal to RHS.
        """
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        m_ed: NMM,
        m_b_rd: NMM,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the left-hand side of the comparison.

        see __init__ for details.
        """
        raise_if_negative(m_ed=m_ed)
        raise_if_less_or_equal_to_zero(m_b_rd=m_b_rd)
        return m_ed / m_b_rd

    @staticmethod
    def _evaluate_rhs(*_, **_kwargs) -> float:
        """Evaluates the right-hand side of the comparison.

        see __init__ for details.
        """
        return 1.0

    @property
    def unity_check(self) -> float:
        """Returns the unity check value."""
        return self.lhs

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.54."""
        _equation: str = r"\frac{M_{Ed}}{M_{b,Rd}} \leq 1.0"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"M_{Ed}": f"{self.m_ed:.{n}f}",
                r"M_{b,Rd}": f"{self.m_b_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"M_{Ed}": rf"{self.m_ed:.{n}f} \ Nmm",
                r"M_{b,Rd}": rf"{self.m_b_rd:.{n}f} \ Nmm",
            },
            False,
        )
        _intermediate_result: str = (
            rf"\left( {self.unity_check:.{n}f} \leq 1.0 \right)"
        )
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
