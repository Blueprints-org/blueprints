"""Formula 5.17 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

import math

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, KN_M2, M
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot17EffectiveLengthBucklingLoad(Formula):
    r"""Class representing formula 5.17 for the calculation of effective length of unbraced members, in the
    case where criteria (2) and (3) do not apply such as by variable loading, [$l_0$].
    """

    label = "5.17"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, ei: KN_M2, n_b: KN) -> None:
        r"""[$l_{0}$] Effective length for unbraced members [$m$].

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.2(6) - Formula (5.17)

        Parameters
        ----------
        ei : KN_M2
            [$EI$] is a representative bending stiffness [$kN/m^2$].
        n_b : KN
            [$N_{b}$] is the buckling load expressed in terms of EI (in equation (5.14) i should correspond
            to this EI). [$kN$].
        """
        super().__init__()
        self.ei = ei
        self.n_b = n_b

    @staticmethod
    def _evaluate(ei: KN_M2, n_b: KN) -> M:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(ei=ei, n_b=n_b)
        raise_if_less_or_equal_to_zero(n_b=n_b)
        return math.pi * math.sqrt(ei / n_b)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.17."""
        return LatexFormula(
            return_symbol=r"l_0",
            result=f"{self:.3f}",
            equation=r"\pi \cdot \sqrt{\frac{EI}{N_{b}}}",
            numeric_equation=rf"\pi \cdot \sqrt{{\frac{{{self.ei}}}{{{self.n_b}}}}}",
            comparison_operator_label="=",
        )
