"""Formula 6.42 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot42BetaCircular(Formula):
    r"""Class representing formula 6.42 for the calculation of [$\beta$]."""

    label = "6.42"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        d: MM,
        diameter: MM,
        e: MM,
    ) -> None:
        r"""[$\beta$] Calculation of [$\beta$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.3(3) - Formula (6.42)

        Parameters
        ----------
        d : MM
            [$d$] Effective depth of the slab [$mm$].
        diameter : MM
            [$D$] Diameter of the circular column [$mm$].
        e : MM
            [$e$] Distance from the axis about which the moment [$M_{Ed}$] acts [$mm$].
        """
        super().__init__()
        self.d = d
        self.diameter = diameter
        self.e = e

    @staticmethod
    def _evaluate(
        d: MM,
        diameter: MM,
        e: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d=d, diameter=diameter, e=e)
        denominator = diameter + 4 * d
        raise_if_less_or_equal_to_zero(denominator=denominator)

        return 1 + 0.6 * np.pi * e / (diameter + 4 * d)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.42."""
        _equation: str = r"1 + 0.6 \cdot \pi \cdot \frac{e}{D + 4 \cdot d}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r" d": f" {self.d:.3f}",
                r"D": f"{self.diameter:.3f}",
                r"e": f"{self.e:.3f}",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"\beta",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
