"""Formula 6.33 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form6Dot33ContourRadiusCircularColumnHeads(Formula):
    r"""Class representing formula 6.33 for the calculation of the contour radius for circular column heads, [$r_{cont}$]."""

    label = "6.33"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        d: MM,
        l_h: MM,
        c: MM,
    ) -> None:
        r"""[$r_{cont}$] Contour radius for circular column heads [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.2(8) - Formula (6.33)

        Parameters
        ----------
        d : MM
            [$d$] Effective depth [$mm$].
        l_h : MM
            [$l_{H}$] Distance from the column face to the edge of the column head [$mm$].
        c : MM
            [$c$] Diameter of a circular column [$mm$].
        """
        super().__init__()
        self.d = d
        self.l_h = l_h
        self.c = c

    @staticmethod
    def _evaluate(
        d: MM,
        l_h: MM,
        c: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            d=d,
            l_h=l_h,
            c=c,
        )

        return 2 * d + l_h + 0.5 * c

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.33."""
        return LatexFormula(
            return_symbol=r"r_{cont}",
            result=f"{self:.3f}",
            equation=r"2 \cdot d + l_{H} + 0.5 \cdot c",
            numeric_equation=rf"2 \cdot {self.d:.3f} + {self.l_h:.3f} + 0.5 \cdot {self.c:.3f}",
            comparison_operator_label="=",
            unit="mm",
        )
