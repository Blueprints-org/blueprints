"""Formula 5.16 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

import math

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_negative


class Form5Dot16EffectiveLengthUnbraced(Formula):
    """Class representing formula 5.16 for the calculation of effective length of unbraced members, [$l_0$]."""

    label = "5.16"
    source_document = EN_1992_1_1_2004

    def __init__(self, k_1: DIMENSIONLESS, k_2: DIMENSIONLESS, height: M) -> None:
        r"""[$l_{0}$] Effective length for unbraced members [$m$].

        EN 1992-1-1:2004 art.5.8.3.2(3) - Formula (5.16)

        Parameters
        ----------
        k_1 : DIMENSIONLESS
            [$k_{1}$] Relative flexibility of rotational constraint at end 1 [$-$].
        k_2 : DIMENSIONLESS
            [$k_{2}$] Relative flexibility of rotational constraint at end 2 [$-$].
        height : M
            [$l$] Clear height of compression member between end constraint [$m$].
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
        return height * max(math.sqrt(1.0 + 10 * (k_1 * k_2 / (k_1 + k_2))), (1.0 + k_1 / (1.0 + k_1)) * (1.0 + k_2 / (1.0 + k_2)))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.16."""
        return LatexFormula(
            return_symbol=r"l_0",
            result=f"{self:.{n}f}",
            equation=r"l \cdot max\left\{"
            r"\sqrt{1+10 \cdot \frac{k_1 \cdot k_2}{k_1+k_2}}; "
            r"\left(1+\frac{k_1}{1 + k_1}\right) \cdot \left(1 + \frac{k_2}{1 + k_2}\right) \right\}",
            numeric_equation=rf"{self.height:.{n}f} \cdot max\left\{{"
            rf"\sqrt{{1+10 \cdot \frac{{{self.k_1:.{n}f} \cdot {self.k_2:.{n}f}}}{{{self.k_1:.{n}f}+{self.k_2:.{n}f}}}}}; "
            rf"\left(1+\frac{{{self.k_1:.{n}f}}}{{1 + {self.k_1:.{n}f}}}\right) \cdot "
            rf"\left(1 + \frac{{{self.k_2:.{n}f}}}{{1 + {self.k_2:.{n}f}}}\right) \right\}}",
            comparison_operator_label="=",
        )
