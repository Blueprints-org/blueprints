"""Formula 5.8 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit states."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1993_5_2008 import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot8RelativeWebSlenderness(Formula):
    """Class representing formula 5.8 for relative slenderness of the web."""

    label = "5.8"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        c: MM,  # Length of the web
        t_w: MM,  # Thickness of the web
        f_y: MPA,  # Yield strength
        e: MPA,  # Young's modulus
    ) -> None:
        r"""[$\overline{\lambda}$] Calculate the relative slenderness of the web [$-$].

        NEN-EN 1993-5:2008(E) art.5.2.2(7) - Formula (5.8)

        Parameters
        ----------
        c : MM
            [$c$] Length of the web in [$mm$].
        t_w : MM
            [$t_{w}$] Thickness of the web in [$mm$].
        f_y : MPA
            [$f_{y}$] Yield strength in [$MPa$].
        e : MPA
            [$E$] Young's modulus in [$MPa$].
        """
        super().__init__()
        self.c: MM = c
        self.t_w: MM = t_w
        self.f_y: MPA = f_y
        self.e: MPA = e

    @staticmethod
    def _evaluate(
        c: MM,
        t_w: MM,
        f_y: MPA,
        e: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula for relative slenderness."""
        raise_if_less_or_equal_to_zero(c=c, t_w=t_w, f_y=f_y, e=e)
        return 0.346 * (c / t_w) * np.sqrt(f_y / e)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.8."""
        return LatexFormula(
            return_symbol=r"\overline{\lambda}",
            result=str(self),
            equation=rf"0.346 \cdot {latex_fraction(numerator='c', denominator='t_w')} \sqrt{{{latex_fraction(numerator='f_y', denominator='E')}}}",
            numeric_equation=rf"0.346 \cdot {latex_fraction(numerator=self.c, denominator=self.t_w)} \sqrt{{"
            rf"{latex_fraction(numerator=self.f_y, denominator=self.e)}}}",
            comparison_operator_label="=",
        )
