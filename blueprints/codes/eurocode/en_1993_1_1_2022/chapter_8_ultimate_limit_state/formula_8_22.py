"""Formula 8.22 from EN 1993-1-1:2022: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.en_1993_1_1_2022 import EN_1993_1_1_2022
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot22CheckShearForce(ComparisonFormula):
    r"""Class representing formula 8.22 for checking the design value of the shear force."""

    label = "8.22"
    source_document = EN_1993_1_1_2022

    def __init__(
        self,
        v_ed: N,
        v_c_rd: N,
    ) -> None:
        r"""Check the design value of the shear force at each cross section.

        EN 1993-1-1:2022 art.8.2.6(1) - Formula (8.22)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design value of the shear force [$N$].
        v_c_rd : N
            [$V_{c,Rd}$] Design shear resistance [$N$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.v_c_rd = v_c_rd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        v_ed: N,
        v_c_rd: N,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the left-hand side of the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(v_c_rd=v_c_rd)
        raise_if_negative(v_ed=v_ed)

        return v_ed / v_c_rd

    @staticmethod
    def _evaluate_rhs(*_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the formula, for more information see the __init__ method."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.22."""
        _equation: str = r"\frac{V_{Ed}}{V_{c,Rd}} \leq 1.0"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "V_{Ed}": f"{self.v_ed:.{n}f}",
                "V_{c,Rd}": f"{self.v_c_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                "V_{c,Rd}": rf"{self.v_c_rd:.{n}f} \ N",
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
