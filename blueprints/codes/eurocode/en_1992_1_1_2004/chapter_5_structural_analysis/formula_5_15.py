"""Formula 5.15 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

import math

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_negative


class Form5Dot15EffectiveLengthBraced(Formula):
    r"""Class representing formula 5.15 for the calculation of the effective length of braced members, [$l_0$]."""

    label = "5.15"
    source_document = EN_1992_1_1_2004

    def __init__(self, k_1: DIMENSIONLESS, k_2: DIMENSIONLESS, height: M) -> None:
        r"""[$l_{0}$] Effective length for braced members [$m$].

        EN 1992-1-1:2004 art.5.8.3.2(3) - Formula (5.15)

        Parameters
        ----------
        k_1 : DIMENSIONLESS
            [$k_{1}$] Relative flexibility of rotational constraint at end 1 [$-$].
        k_2 : DIMENSIONLESS
            [$k_{2}$] Relative flexibility of rotational constraint at end 2 [$-$].
        height : M
            [$l$] Clear height of compression member between end constraints [$m$].
        """
        super().__init__()
        self.k_1 = k_1
        self.k_2 = k_2
        self.height = height

    @staticmethod
    def _evaluate(
        k_1: DIMENSIONLESS,
        k_2: DIMENSIONLESS,
        height: M,
    ) -> M:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(k_1=k_1, k_2=k_2, height=height)
        return 0.5 * height * math.sqrt((1 + k_1 / (0.45 + k_1)) * (1 + k_2 / (0.45 + k_2)))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.15."""
        return LatexFormula(
            return_symbol=r"l_0",
            result=f"{self:.{n}f}",
            equation=r"0.5 \cdot l \cdot \sqrt{\left(1+\frac{k_1}{0.45 + k_1}\right) \cdot \left(1 + \frac{k_2}{0.45 + k_2}\right)}",
            numeric_equation=rf"0.5 \cdot {self.height:.{n}f} \cdot \sqrt{{\left(1+\frac{{{self.k_1:.{n}f}}}{{0.45 + "
            rf"{self.k_1:.{n}f}}}\right) \cdot \left(1 + \frac{{{self.k_2:.{n}f}}}{{0.45 + {self.k_2:.{n}f}}}\right)}}",
            comparison_operator_label="=",
        )
