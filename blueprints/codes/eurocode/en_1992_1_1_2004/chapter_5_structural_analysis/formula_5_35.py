"""Formula 5.35 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot35EffectiveDepth(Formula):
    r"""Class representing formula 5.35 for the calculation of the effective depth, [$d$]."""

    label = "5.35"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        h: MM,
        i_s: MM,
    ) -> None:
        r"""[$d$] Effective depth [$mm$].

        EN 1992-1-1:2004 art.5.8.8.3 - Formula (5.35)

        Parameters
        ----------
        h : MM
            [$h$] Total height of the section [$mm$].
        i_s : MM
            [$i_s$] Radius of gyration of the total reinforcement area [$mm$].
        """
        super().__init__()
        self.h = h
        self.i_s = i_s

    @staticmethod
    def _evaluate(
        h: MM,
        i_s: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(h=h, i_s=i_s)

        return h / 2 + i_s

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.35."""
        return LatexFormula(
            return_symbol=r"d",
            result=f"{self:.{n}f}",
            equation=r"\frac{h}{2} + i_s",
            numeric_equation=rf"\frac{{{self.h:.{n}f}}}{{2}} + {self.i_s:.{n}f}",
            comparison_operator_label="=",
            unit="mm",
        )
