"""Formula 6.45 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2
from blueprints.validations import raise_if_negative


class Form6Dot45W1Rectangular(Formula):
    r"""Class representing formula 6.45 for the calculation of [$W_1$]."""

    label = "6.45"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c_1: MM,
        c_2: MM,
        d: MM,
    ) -> None:
        r"""[$W_1$] Calculation of [$W_1$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.3(4) - Formula (6.45)

        Parameters
        ----------
        c_1 : MM
            [$c_1$] Column dimension parallel to the eccentricity of the load [$mm$].
        c_2 : MM
            [$c_2$] Column dimension perpendicular to the eccentricity of the load [$mm$].
        d : MM
            [$d$] Mean effective depth of the slab [$mm$].
        """
        super().__init__()
        self.c_1 = c_1
        self.c_2 = c_2
        self.d = d

    @staticmethod
    def _evaluate(
        c_1: MM,
        c_2: MM,
        d: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(c_1=c_1, c_2=c_2, d=d)

        return (c_2**2) / 4 + c_1 * c_2 + 4 * c_1 * d + 8 * d**2 + np.pi * d * c_2

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.45."""
        _equation: str = r"\frac{c_2^2}{4} + c_1 \cdot c_2 + 4 \cdot c_1 \cdot d + 8 \cdot d^2 + \pi \cdot d \cdot c_2"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"c_1": f"{self.c_1:.3f}",
                r"c_2": f"{self.c_2:.3f}",
                r" d": f" {self.d:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"W_1",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )
