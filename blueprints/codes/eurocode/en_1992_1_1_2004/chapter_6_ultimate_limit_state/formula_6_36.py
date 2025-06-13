"""Formula 6.36 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form6Dot36ExternalContourRadiusCircularColumnHeads(Formula):
    r"""Class representing formula 6.36 for the calculation of the contour radius for circular column heads, [$r_{cont,ext}$]."""

    label = "6.36"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        l_h: MM,
        d: MM,
        c: MM,
    ) -> None:
        r"""[$r_{cont,ext}$] Contour radius for circular column heads [$mm$].

        EN 1992-1-1:2004 art.6.4.2(11) - Formula (6.36)

        Parameters
        ----------
        l_h : MM
            [$l_{H}$] Distance from the column face to the edge of the column head [$mm$].
        d : MM
            [$d$] Effective depth [$mm$].
        c : MM
            [$c$] Diameter of a circular column [$mm$].
        """
        super().__init__()
        self.l_h = l_h
        self.d = d
        self.c = c

    @staticmethod
    def _evaluate(
        l_h: MM,
        d: MM,
        c: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(l_h=l_h, d=d, c=c)
        return l_h + 2 * d + 0.5 * c

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.36."""
        return LatexFormula(
            return_symbol=r"r_{cont,ext}",
            result=f"{self:.{n}f}",
            equation=r"l_{H} + 2 \cdot d + 0.5 \cdot c",
            numeric_equation=rf"{self.l_h:.{n}f} + 2 \cdot {self.d:.{n}f} + 0.5 \cdot {self.c:.{n}f}",
            comparison_operator_label="=",
            unit="mm",
        )
