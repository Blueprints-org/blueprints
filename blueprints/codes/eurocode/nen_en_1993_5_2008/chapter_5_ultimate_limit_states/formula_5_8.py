"""Formula 5.8 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, fraction
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot8RelativeSlenderness(Formula):
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
        """Calculate the relative slenderness of the web based on formula 5.8 from NEN-EN 1993-5:2007(E) art. 5.2.2(7).

        Parameters
        ----------
        c : MM
            Length of the web in [mm].
        t_w : MM
            Thickness of the web in [mm].
        f_y : MPA
            Yield strength in [MPa].
        e : MPA
            Young's modulus in [MPa].
        """
        super().__init__()
        self.c: float = c
        self.t_w: float = t_w
        self.f_y: float = f_y
        self.e: float = e

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
            equation=rf"0.346 \cdot {fraction('c', 't_w')} \sqrt{{{fraction('f_y', 'E')}}}",
            numeric_equation=rf"0.346 \cdot {fraction(self.c, self.t_w)} \sqrt{{{fraction(self.f_y, self.e)}}}",
            comparison_operator_label="=",
        )
