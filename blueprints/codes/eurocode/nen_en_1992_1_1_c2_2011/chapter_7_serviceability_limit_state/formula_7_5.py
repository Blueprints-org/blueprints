"""Formula 7.5 from NEN-EN 1992-1-1+C2:2011: Chapter 7 - Serviceability Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot5AdjustedBondStrengthRatio(Formula):
    r"""Class representing formula 7.5 for the calculation of [$\xi_1$]."""

    label = "7.5"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        xi: DIMENSIONLESS,
        diam_s: MM,
        diam_p: MM,
    ) -> None:
        r"""[$\xi_1$] Calculation of the ratio of bond strength of presetressing and reinforcing steel [$-$].
        Note: if only prestressing steel is used to control cracking: [$\xi_1 = \sqrt{\xi}$].

        NEN-EN 1992-1-1+C2:2011 art.7.3.2(3) - Formula (7.5)

        Parameters
        ----------
        xi : DIMENSIONLESS
            [$\xi$] Ratio of bond strength of prestressing and reinforcing steel.
        diam_s : MM
            [$⌀_s$] Largest bar diameter of reinforcing steel [$mm$].
        diam_p : MM
            [$⌀_p$] Equivalent diameter of tendon [$mm$].
        """
        super().__init__()
        self.xi = xi
        self.diam_s = diam_s
        self.diam_p = diam_p

    @staticmethod
    def _evaluate(
        xi: DIMENSIONLESS,
        diam_s: MM,
        diam_p: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(xi=xi, diam_s=diam_s)
        raise_if_less_or_equal_to_zero(diam_p=diam_p)

        return np.sqrt(xi * (diam_s / diam_p))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 7.5."""
        _equation: str = r"\sqrt{\xi \cdot \left( \frac{⌀_s}{⌀_p} \right)}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\xi": f"{self.xi:.3f}",
                r"⌀_s": f"{self.diam_s:.3f}",
                r"⌀_p": f"{self.diam_p:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\xi_1",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
