"""Formula 6.45 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2
from blueprints.validations import raise_if_negative


class Form6Dot45W1Rectangular(Formula):
    r"""Class representing formula 6.45 for the calculation of [$W_1$]."""

    label = "6.45"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        c_1: MM,
        c_2: MM,
        d: MM,
    ) -> None:
        r"""[$W_1$] Calculation of [$W_1$].

        EN 1992-1-1:2004 art.6.4.3(4) - Formula (6.45)

        Parameters
        ----------
        c_1 : MM
            [$c_1$] Column dimension parallel to the eccentricity of the load [$mm$].
        c_2 : MM
            [$c_2$] Column dimension perpendicular to the eccentricity of the load [$mm$].
        d : MM
            [$d$] Mean effective depth of the slab [$mm$].
        """
        super().__init__()
        self.c_1 = c_1
        self.c_2 = c_2
        self.d = d

    @staticmethod
    def _evaluate(
        c_1: MM,
        c_2: MM,
        d: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(c_1=c_1, c_2=c_2, d=d)

        return (c_2**2) / 4 + c_1 * c_2 + 4 * c_1 * d + 8 * d**2 + np.pi * d * c_2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.45."""
        _equation: str = r"\frac{c_2^2}{4} + c_1 \cdot c_2 + 4 \cdot c_1 \cdot d + 8 \cdot d^2 + \pi \cdot d \cdot c_2"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"c_1": f"{self.c_1:.{n}f}",
                r"c_2": f"{self.c_2:.{n}f}",
                r" d": f" {self.d:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"W_1",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )
