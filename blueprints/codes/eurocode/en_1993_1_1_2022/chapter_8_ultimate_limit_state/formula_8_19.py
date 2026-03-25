"""Formula 8.19 from EN 1993-1-1:2022: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.en_1993_1_1_2022 import EN_1993_1_1_2022
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot19CheckBendingMoment(ComparisonFormula):
    r"""Class representing formula 8.19 for the test of the bending moment."""

    label = "8.19"
    source_document = EN_1993_1_1_2022

    def __init__(
        self,
        m_ed: NMM,
        m_c_rd: NMM,
    ) -> None:
        r"""Check the bending moment.

        EN 1993-1-1:2022 art.8.2.5(1) - Formula (8.19)

        Parameters
        ----------
        m_ed : NMM
            [$M_{Ed}$] Design bending moment [$Nmm$].
        m_c_rd : NMM
            [$M_{c,Rd}$] The design resistance for bending about one principal axis of a cross-section [$Nmm$].
        """
        super().__init__()
        self.m_ed = m_ed
        self.m_c_rd = m_c_rd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        m_ed: NMM,
        m_c_rd: NMM,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the left-hand side of the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(m_c_rd=m_c_rd)
        raise_if_negative(m_ed=m_ed)

        return m_ed / m_c_rd

    @staticmethod
    def _evaluate_rhs(*_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the formula, for more information see the __init__ method."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.19."""
        _equation: str = r"\frac{M_{Ed}}{M_{c,Rd}} \leq 1.0"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            replacements={
                "M_{Ed}": f"{self.m_ed:.{n}f}",
                "M_{c,Rd}": f"{self.m_c_rd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            replacements={
                "M_{Ed}": rf"{self.m_ed:.{n}f} \ Nmm",
                "M_{c,Rd}": rf"{self.m_c_rd:.{n}f} \ Nmm",
            },
            unique_symbol_check=False,
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
