"""Formula NB.NB.11 from NEN-EN 1993-1-1:2006: Chapter NB.NB - Coefficient C."""

import numpy as np

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_2006 import NEN_EN_1993_1_1_2006_A1_2014_NB_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class FormNBDotNB11CoefficientC(Formula):
    r"""Class representing formula NB.NB.11 for the calculation of [$C$]."""

    label = "NB.NB.11"
    source_document = NEN_EN_1993_1_1_2006_A1_2014_NB_2016

    def __init__(
        self,
        c_1: DIMENSIONLESS,
        c_2: DIMENSIONLESS,
        l_g: MM,
        l_kip: MM,
        s: MM,
    ) -> None:
        r"""[$C$] Calculation of coefficient C [-].

        NEN-EN 1993-1-1:2006 art.NB.NB.4.3(2) - Formula (NB.NB.11)

        Parameters
        ----------
        c_1 : DIMENSIONLESS
            [$C_1$] Coefficient dependent on the nature of the loading [-].
        c_2 : DIMENSIONLESS
            [$C_2$] Coefficient dependent on the location of application of the load relative to the neutral axis.
            C₂ = 0 if the load acts at the centroid of the cross-section.
            C₂ must be entered in the formula for determining coefficient C with a positive sign if the load acts at the centroid of the top flange.
            C₂ must be entered in this formula with a negative sign if the load acts at the centroid of the bottom flange [-].
        l_g : MM
            [$L_g$] Length of the beam between the supports [$mm$].
        l_kip : MM
            [$L_{kip}$] Replaced unsupported tip length between two supports, between one support and one lateral support,
            or between two lateral supports [$mm$].
        s : MM
            [$S$] Parameter, for calculating S applies NB.NB.12 [$mm$].
        """
        super().__init__()
        self.c_1 = c_1
        self.c_2 = c_2
        self.l_g = l_g
        self.l_kip = l_kip
        self.s = s

    @staticmethod
    def _evaluate(
        c_1: DIMENSIONLESS,
        c_2: DIMENSIONLESS,
        l_g: MM,
        l_kip: MM,
        s: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(l_kip=l_kip)
        raise_if_negative(c_1=c_1, l_g=l_g, s=s)

        term1 = (np.pi * c_1 * l_g) / l_kip
        term2 = np.sqrt(1 + (np.pi**2 * s**2) / (l_kip**2) * (c_2**2 + 1))
        term3 = (np.pi * c_2 * s) / l_kip

        return term1 * (term2 + term3)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula NB.NB.11."""
        _equation: str = (
            r"\frac{\pi \cdot C_1 \cdot L_g}{L_{kip}} \cdot \left( \sqrt{1 + \frac{\pi^2 \cdot S^2}{L_{kip}^2} "
            r"\cdot \left(C_2^2 + 1\right)} + \frac{\pi \cdot C_2 \cdot S}{L_{kip}} \right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"C_1": f"{self.c_1:.{n}f}",
                r"C_2": f"{self.c_2:.{n}f}",
                r"L_g": f"{self.l_g:.{n}f}",
                r"L_{kip}": f"{self.l_kip:.{n}f}",
                r"S": f"{self.s:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"C_1": f"{self.c_1:.{n}f}",
                r"C_2": f"{self.c_2:.{n}f}",
                r"L_g": rf"{self.l_g:.{n}f} \ mm",
                r"L_{kip}": rf"{self.l_kip:.{n}f} \ mm",
                r"S": rf"{self.s:.{n}f} \ mm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"C",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
