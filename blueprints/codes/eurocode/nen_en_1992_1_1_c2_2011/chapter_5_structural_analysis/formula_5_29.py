"""Formula 5.29 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot29BetaFactor(Formula):
    r"""Class representing formula 5.29 for the calculation of the beta factor, [$\beta$]."""

    label = "5.29"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c_0: DIMENSIONLESS,
    ) -> None:
        r"""[$\beta$] Factor which depends on the distribution of first order moment [-].

        NEN-EN 1992-1-1+C2:2011 art.5.8.8.2(3) - Formula (5.29)

        Parameters
        ----------
        c_0 : float
            Coefficient which depends on the distribution of first order moment [-].
            For instance, c_0 = 8 for a constant first order moment, c_0 = 9.6 for a parabolic and 12 for a symmetric triangular distribution.
        """
        super().__init__()
        self.c_0 = c_0

    @staticmethod
    def _evaluate(
        c_0: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(c_0=c_0)
        return (np.pi**2) / c_0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.29."""
        return LatexFormula(
            return_symbol=r"\beta",
            result=f"{self:.3f}",
            equation=r"\frac{\pi^2}{c_0}",
            numeric_equation=rf"\frac{{\pi^2}}{{{self.c_0:.3f}}}",
            comparison_operator_label="=",
            unit="-",
        )
