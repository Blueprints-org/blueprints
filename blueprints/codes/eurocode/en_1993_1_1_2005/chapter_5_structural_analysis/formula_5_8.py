"""Formula 5.8 from EN 1993-1-1:2005: Chapter 5 - Structural Analysis."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot8CheckSlenderness(Formula):
    r"""Class representing formula 5.8 for check of slenderness."""

    label = "5.8"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        lambda_bar: DIMENSIONLESS,
        a: MM2,
        f_y: MPA,
        n_ed: N,
    ) -> None:
        r"""Check the slenderness ratio.

        EN 1993-1-1:2005 art.5.3.2(6) - Formula (5.8)

        Parameters
        ----------
        lambda_bar : DIMENSIONLESS
            [$\lambda_{bar}$] Non-dimensional slenderness [-].
        a : MM2
            [$A$] Cross-sectional area [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength [$MPa$].
        n_ed : N
            [$N_{Ed}$] Design value of the compression force [$N$].
        """
        super().__init__()
        self.lambda_bar = lambda_bar
        self.a = a
        self.f_y = f_y
        self.n_ed = n_ed

    @staticmethod
    def _evaluate(
        lambda_bar: DIMENSIONLESS,
        a: MM2,
        f_y: MPA,
        n_ed: N,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(lambda_bar=lambda_bar, A=a, f_y=f_y, N_Ed=n_ed)

        return lambda_bar > 0.5 * np.sqrt(a * f_y / n_ed)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.8."""
        n = 2
        _equation: str = r"\left( \lambda_{bar} > 0.5 \sqrt{\frac{A \cdot f_{y}}{N_{Ed}}} \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\lambda_{bar}": f"{self.lambda_bar:.{n}f}",
                "A": f"{self.a:.{n}f}",
                "f_{y}": f"{self.f_y:.{n}f}",
                "N_{Ed}": f"{self.n_ed:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
