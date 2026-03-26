"""Formula 8.45 from EN 1993-1-1:2022: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.en_1993_1_1_2022 import EN_1993_1_1_2022
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot45CheckAxialForceY(ComparisonFormula):
    r"""Class representing formula 8.45 for checking axial force about the y-y axis."""

    label = "8.45"
    source_document = EN_1993_1_1_2022

    def __init__(
        self,
        n_ed: N,
        n_pl_rd: N,
    ) -> None:
        r"""For doubly symmetrical I- and H-sections or other flanges sections,
        allowance need not be made for the effect of the axial force on the
        plastic resistance moment about the y-y axis when 8.45 and 8.46 are satisfied.

        EN 1993-1-1:2022 art.8.2.9.1(4) - Formula (8.45)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design axial force [$N$].
        n_pl_rd : N
            [$N_{pl,Rd}$] Plastic resistance normal force [$N$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_pl_rd = n_pl_rd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        n_ed: N,
        n_pl_rd: N,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the left-hand side of the comparison. See __init__ for details."""
        raise_if_less_or_equal_to_zero(n_pl_rd=n_pl_rd)
        return n_ed

    @staticmethod
    def _evaluate_rhs(
        n_pl_rd: N,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the right-hand side of the comparison. See __init__ for details."""
        return 0.25 * n_pl_rd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.45."""
        _equation: str = r"N_{Ed} \leq 0.25 \cdot N_{pl,Rd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            replacements={
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"N_{pl,Rd}": f"{self.n_pl_rd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            replacements={
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"N_{pl,Rd}": rf"{self.n_pl_rd:.{n}f} \ N",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol="CHECK",
            result="OK" if bool(self) else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="\\to",
            unit="",
        )
