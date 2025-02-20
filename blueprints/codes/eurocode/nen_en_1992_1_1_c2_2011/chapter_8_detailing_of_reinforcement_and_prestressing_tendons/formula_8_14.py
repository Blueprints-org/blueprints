"""Formula 8.14 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_negative


class Form8Dot14EquivalentDiameterBundledBars(Formula):
    """Class representing formula 8.14 for the calculation of the equivalent diameter of bundled bars, [$Ø_{n}$]."""

    label = "8.14"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        diameter: MM,
        n_b: DIMENSIONLESS,
    ) -> None:
        r"""[$Ø_{n}$] Equivalent diameter of bundled bars [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.8.9.1(2) - Formula (8.14)

        Parameters
        ----------
        diameter : MM
            [$Ø$] Diameter of the bars [$mm$]
        n_b : DIMENSIONLESS
            [$n_{b}$] Number of bars in the bundle [$-$].

            ≤ 4 for vertical bars in compression and for bars in a lapped joint.

            ≤ 3 for all other cases.
        """
        super().__init__()
        self.diameter = diameter
        self.n_b = n_b

    @staticmethod
    def _evaluate(diameter: MM, n_b: DIMENSIONLESS) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            diameter=diameter,
            n_b=n_b,
        )
        return min(diameter * np.sqrt(n_b), 55)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 8.14."""
        return LatexFormula(
            return_symbol=r"Ø_n",
            result=f"{self:.2f}",
            equation=r"\min \left(55 \ \text{mm}, Ø \cdot \sqrt{n_b} \right)",
            numeric_equation=rf"\min \left(55 \ \text{{mm}}, {self.diameter:.2f} \cdot \sqrt{{{self.n_b:.2f}}} \right)",
            comparison_operator_label="=",
        )
