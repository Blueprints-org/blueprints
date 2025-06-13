"""Formula 5.40b from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import M
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot40bCheckLateralInstability(Formula):
    r"""Class representing formula 5.40b for checking lateral instability in transient situations."""

    label = "5.40b"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        l_0t: M,
        b: M,
        h: M,
    ) -> None:
        r"""Check the conditions to ignore second order effects in connection with lateral instability.

        EN 1992-1-1:2004 art.5.9(3) - Formula (5.40b)

        Parameters
        ----------
        l_0t : M
            [$l_{0t}$] is the distance between torsional restraints [$m$].
        b : M
            [$b$] is the width of compression flange [$m$].
        h : M
            [$h$] is the total depth of beam in central part of [$l_{0t}$] [$m$].
        """
        super().__init__()
        self.l_0t = l_0t
        self.b = b
        self.h = h

    @staticmethod
    def _evaluate(
        l_0t: M,
        b: M,
        h: M,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(b=b, h=h)
        raise_if_negative(l_0t=l_0t)

        return (l_0t / b <= 70 / (h / b) ** (1 / 3)) and (h / b <= 3.5)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.40b."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\left( \frac{l_{0t}}{b} \leq \frac{70}{\left( h/b \right)^{1/3}} \text{ and } \frac{h}{b} \leq 3.5 \right)",
            numeric_equation=rf"\left( \frac{{{self.l_0t:.{n}f}}}{{{self.b:.{n}f}}} \leq \frac{{70}}{{\left("
            rf" {self.h:.{n}f}/{self.b:.{n}f} \right)^{{1/3}}}} \text{{ and }} "
            rf"\frac{{{self.h:.{n}f}}}{{{self.b:.{n}f}}} \leq 3.5 \right)",
            comparison_operator_label="\\to",
            unit="",
        )
