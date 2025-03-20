"""Formula 1.0.1 from NEN 9997-1+C2:2017: Chapter 1: General rules."""

import numpy as np

from blueprints.codes.eurocode.nen_9997_1_c2_2017 import NEN_9997_1_C2_2017
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction
from blueprints.type_alias import M
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form1Dot0Dot1EquivalentPilePointCenterline(Formula):
    r"""Class representing formula 1.0.1 for the calculation of the equivalent pile point centerline [$D_{eq}$] in [$m$]."""

    label = "1.0.1"
    source_document = NEN_9997_1_C2_2017

    def __init__(self, a: M, b: M) -> None:
        r"""[$D_{eq}$] Equivalent pile point centerline.

        NEN 9997-1+C2:2017 art.1.5.2.106a - Formula (1.0.1)

        Parameters
        ----------
        a : M
            [$a$] minor dimension of the largest cross-section at the pile tip [$m$].
        b : M
            [$b$] major dimension of the largest cross-section at the pile tip [$m$].

            Where: b ≤ 1.5 * a
        """
        super().__init__()
        self.a = a
        self.b = b

    @staticmethod
    def _evaluate(
        a: M,
        b: M,
    ) -> M:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(a=a, b=b)
        if b > 1.5 * a:
            raise ValueError("b must be less than or equal to 1.5 * a")
        return 1.13 * a * np.sqrt(b / a)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 1.0.1."""
        return LatexFormula(
            return_symbol=r"D_{eq}",
            result=f"{self:.3f}",
            equation=r"1.13 \cdot a \cdot \sqrt{\frac{min(b, 1.5 \cdot a)}{a}}",
            numeric_equation=rf"1.13 \cdot {self.a} \cdot \sqrt{latex_fraction(numerator=self.b, denominator=self.a)}",
            comparison_operator_label="=",
        )
