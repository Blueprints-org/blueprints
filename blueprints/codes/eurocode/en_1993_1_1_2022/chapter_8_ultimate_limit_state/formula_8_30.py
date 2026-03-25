"""Formula 8.30 from EN 1993-1-1:2022: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.en_1993_1_1_2022 import EN_1993_1_1_2022
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot30CheckCombinedShearForceAndTorsionalMoment(ComparisonFormula):
    r"""Class representing formula 8.30 for combined shear force and torsional moment."""

    label = "8.30"
    source_document = EN_1993_1_1_2022

    def __init__(
        self,
        v_ed: N,
        v_pl_t_rd: N,
    ) -> None:
        r"""Check the combined shear force and torsional moment.

        EN 1993-1-1:2022 art.8.2.7(9) - Formula (8.30)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design shear force [$N$].
        v_pl_t_rd : N
            [$V_{pl,T,Rd}$] Plastic shear resistance accounting for torsional effects, derived from equation 8.31, 8.32 or 8.33 [$N$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.v_pl_t_rd = v_pl_t_rd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        v_ed: N,
        v_pl_t_rd: N,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the left-hand side of the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(v_pl_t_rd=v_pl_t_rd)
        raise_if_negative(v_ed=v_ed)

        return v_ed / v_pl_t_rd

    @staticmethod
    def _evaluate_rhs(*_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the formula, for more information see the __init__ method."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.30."""
        _equation: str = r"\frac{V_{Ed}}{V_{pl,T,Rd}} \leq 1.0"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            replacements={
                "V_{Ed}": f"{self.v_ed:.{n}f}",
                "V_{pl,T,Rd}": f"{self.v_pl_t_rd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            replacements={
                "V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                "V_{pl,T,Rd}": rf"{self.v_pl_t_rd:.{n}f} \ N",
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
