"""Formula 6.37 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form6Dot37InternalContourRadiusCircularColumnHeads(Formula):
    r"""Class representing formula 6.37 for the calculation of the contour radius for circular column heads, [$r_{cont,int}$]."""

    label = "6.37"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        d: MM,
        h_h: MM,
        c: MM,
    ) -> None:
        r"""[$r_{cont,int}$] Contour radius for circular column heads [$mm$].

        EN 1992-1-1:2004 art.6.4.2(11) - Formula (6.37)

        Parameters
        ----------
        d : MM
            [$d$] Effective depth [$mm$].
        h_h : MM
            [$h_{H}$] height of the column head [$mm$].
        c : MM
            [$c$] Diameter of a circular column [$mm$].
        """
        super().__init__()
        self.d = d
        self.h_h = h_h
        self.c = c

    @staticmethod
    def _evaluate(
        d: MM,
        h_h: MM,
        c: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d=d, h_h=h_h, c=c)
        return 2 * (d + h_h) + 0.5 * c

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.37."""
        return LatexFormula(
            return_symbol=r"r_{cont,int}",
            result=f"{self:.{n}f}",
            equation=r"2 \cdot (d + h_{H}) + 0.5 \cdot c",
            numeric_equation=rf"2 \cdot ({self.d:.{n}f} + {self.h_h:.{n}f}) + 0.5 \cdot {self.c:.{n}f}",
            comparison_operator_label="=",
            unit="mm",
        )
