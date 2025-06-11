"""Formula 6.41 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM, MM2
from blueprints.validations import raise_if_negative


class Form6Dot41W1Rectangular(Formula):
    r"""Class representing formula 6.41 for the calculation of [$W_1$]."""

    label = "6.41"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        c_1: MM,
        c_2: MM,
        d: MM,
    ) -> None:
        r"""[$W_1$] Calculation of [$W_1$].

        EN 1992-1-1:2004 art.6.4.3(3) - Formula (6.41)

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

        return (c_1**2) / 2 + c_1 * c_2 + 4 * c_2 * d + 16 * d**2 + 2 * np.pi * d * c_1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.41."""
        return LatexFormula(
            return_symbol=r"W_1",
            result=f"{self:.{n}f}",
            equation=r"\frac{c_1^2}{2} + c_1 \cdot c_2 + 4 \cdot c_2 \cdot d + 16 \cdot d^2 + 2 \cdot \pi \cdot d \cdot c_1",
            numeric_equation=rf"\frac{{{self.c_1:.{n}f}^2}}{{2}} + {self.c_1:.{n}f} \cdot "
            rf"{self.c_2:.{n}f} + 4 \cdot {self.c_2:.{n}f} \cdot {self.d:.{n}f} + 16 \cdot {self.d:.{n}f}^2 + "
            rf"2 \cdot \pi \cdot {self.d:.{n}f} \cdot {self.c_1:.{n}f}",
            comparison_operator_label="=",
            unit="mm^2",
        )
