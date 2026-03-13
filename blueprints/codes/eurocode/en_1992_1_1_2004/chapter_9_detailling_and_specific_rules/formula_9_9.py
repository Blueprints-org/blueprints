"""Formula 9.9 from EN 1992-1-1:2004: Chapter 9 - Detailling and specific rules."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG, MM
from blueprints.validations import raise_if_negative


class Form9Dot9MaximumSpacingSeriesOfLinks(Formula):
    r"""Class representing the formula 9.9 for the calculation of the maximum distance between successive series of links in longitudinal direction
    for slabs.
    """

    label = "9.9"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        d: MM,
        alpha: DEG,
    ) -> None:
        r"""[$s_{max}$] Maximum distance between successive series of links in longitudinal direction for slabs [$mm$].

        EN 1992-1-1:2004 art.9.3.2(4) - Formula (9.9)

        Parameters
        ----------
        d: MM
            [$d$] Effective height of the cross-section [$mm$].
        alpha: DEG
            [$\alpha$] The angle between the shear reinforcement and the longitudinal axis of the slab (see 9.2.2(1)) [$deg$].
        """
        super().__init__()
        self.d = d
        self.alpha = alpha

    @staticmethod
    def _evaluate(d: MM, alpha: DEG) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(d=d)

        # Convert the angle from degrees to radians
        alpha_radians = np.deg2rad(alpha)

        # Calculate the cotangent
        cot_alpha = 1 / np.tan(alpha_radians)

        return 0.75 * d * (1 + cot_alpha)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 9.9."""
        return LatexFormula(
            return_symbol=r"s_{max}",
            result=f"{self:.{n}f}",
            equation=r"0.75 \cdot d \cdot \left( 1 + cot(\alpha) \right)",
            numeric_equation=rf"0.75 \cdot {self.d:.{n}f} \cdot \left( 1 + cot({self.alpha:.{n}f}) \right)",
            comparison_operator_label="=",
        )
