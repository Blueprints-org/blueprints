"""Formula 6.34 and 6.35 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from math import sqrt

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form6Dot34And35ContourRadiusRectangular(Formula):
    r"""Class representing formulas 6.34 and 6.35 for the calculation of the contour radius for rectangular columns with a rectangular head
    where $l_H < 2.0 h_H$.
    """

    label = "6.34 and 6.35"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        d: MM,
        c_1: MM,
        c_2: MM,
        l_h1: MM,
        l_h2: MM,
    ) -> None:
        r"""[$r_{cont}$] Contour radius [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.3(8) - Formula (6.34 and 6.35)

        Parameters
        ----------
        d : MM
            [$d$] Effective depth [$mm$].
        c_1 : MM
            [$c_{1}$] Column size in one direction [$mm$].
        c_2 : MM
            [$c_{2}$] Column size in the perpendicular direction [$mm$].
        l_h1 : MM
            [$l_{H1}$] Head size in one direction [$mm$].
        l_h2 : MM
            [$l_{H2}$] Head size in the perpendicular direction [$mm$].
        """
        super().__init__()
        self.d = d

        self.l_1 = c_1 + 2 * l_h1
        self.l_2 = c_2 + 2 * l_h2

        self.c_1, self.c_2 = (c_2, c_1) if self.l_1 > self.l_2 else (c_1, c_2)
        self.l_h1, self.l_h2 = (l_h2, l_h1) if self.l_1 > self.l_2 else (l_h1, l_h2)

    @staticmethod
    def _evaluate(
        d: MM,
        c_1: MM,
        c_2: MM,
        l_h1: MM,
        l_h2: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d=d, c_1=c_1, c_2=c_2, l_h1=l_h1, l_h2=l_h2)

        l_1 = c_1 + 2 * l_h1
        l_2 = c_2 + 2 * l_h2

        if l_1 > l_2:
            l_1, l_2 = l_2, l_1

        return min(2 * d + 0.56 * sqrt(l_1 * l_2), 2 * d + 0.69 * l_1)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formulas 6.34 and 6.35."""
        return LatexFormula(
            return_symbol=r"r_{cont}",
            result=f"{self:.3f}",
            equation=r"min\left(2 \cdot d + 0.56 \cdot \sqrt{(c_1 + 2 \cdot l_{H1}) \cdot (c_2 + 2 \cdot l_{H2})}, "
            r"2 \cdot d + 0.69 \cdot (c_1 + 2 \cdot l_{H1})\right)",
            numeric_equation=rf"min\left(2 \cdot {self.d:.3f} + 0.56 \cdot \sqrt{{({self.c_1:.3f} + 2 \cdot {self.l_h1:.3f}) \cdot "
            rf"({self.c_2:.3f} + 2 \cdot {self.l_h2:.3f})}}, 2 \cdot {self.d:.3f} + 0.69 \cdot ({self.c_1:.3f} + 2 \cdot {self.l_h1:.3f})\right)",
            comparison_operator_label="=",
            unit="mm",
        )
