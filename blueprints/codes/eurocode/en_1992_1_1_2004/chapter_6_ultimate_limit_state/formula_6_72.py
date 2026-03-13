"""Formula 6.72 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form6Dot72FatigueResistanceConcreteCompression(Formula):
    r"""Class representing formula 6.72 for checking the fatigue resistance of concrete under compression."""

    label = "6.72"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        e_cd_max_equ: MPA,
        r_equ: DIMENSIONLESS,
    ) -> None:
        r"""Check the fatigue resistance of concrete under compression.

        EN 1992-1-1:2004 art.6.8.7(1) - Formula (6.72)

        Parameters
        ----------
        e_cd_max_equ : MPA
            [$E_{cd,max,equ}$] Maximum compressive stress level [$MPa$].
        r_equ : DIMENSIONLESS
            [$R_{equ}$] Stress ratio [$-$].
        """
        super().__init__()
        self.e_cd_max_equ = e_cd_max_equ
        self.r_equ = r_equ

    @staticmethod
    def _evaluate(
        e_cd_max_equ: MPA,
        r_equ: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(e_cd_max_equ=e_cd_max_equ, r_equ=r_equ)
        in_sqrt = 1 - r_equ
        raise_if_negative(in_sqrt=in_sqrt)

        return (e_cd_max_equ + 0.43 * np.sqrt(1 - r_equ)) <= 1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.72."""
        _equation: str = r"E_{cd,max,equ} + 0.43 \cdot \sqrt{1 - R_{equ}} \leq 1"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "E_{cd,max,equ}": f"{self.e_cd_max_equ:.{n}f}",
                "R_{equ}": f"{self.r_equ:.{n}f}",
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
