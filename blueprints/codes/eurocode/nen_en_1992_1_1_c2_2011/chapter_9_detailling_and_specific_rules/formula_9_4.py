"""Formula 9.4 from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailing of members and particular rules."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG, DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_greater_than_90, raise_if_negative


class Form9Dot4ShearReinforcementRatio(Formula):
    """Class representing the formula 9.4 for the calculation of the shear reinforcement ratio."""

    label = "9.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_sw: MM2,
        s: MM,
        b_w: MM,
        alpha: DEG,
    ) -> None:
        r"""[$\rho_w$] Shear reinforcement ratio [$-$].

        NEN-EN 1992-1-1+C2:2011 art.9.2.2(5) - Formula (9.4)

        Parameters
        ----------
        a_sw: MM2
            [$A_{sw}$] Area of shear reinforcement within length s [$mm^2$].
        s: MM
            [$s$] The spacing between shear reinforcement along the longitudinal axis of the element [$mm$].
        b_w: MM
            [$b_w$] The width of the web of the element [$mm$].
        alpha: DEG
            [$\alpha$] The angle between the shear reinforcement and the longitudinal axis of the beam (see 9.2.2(1)) [$deg$].
        """
        super().__init__()
        self.a_sw = a_sw
        self.s = s
        self.b_w = b_w
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        a_sw: MM2,
        s: MM,
        b_w: MM,
        alpha: DEG,
    ) -> DIMENSIONLESS:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(a_sw=a_sw, s=s, b_w=b_w, alpha=alpha)
        raise_if_greater_than_90(alpha=alpha)

        # Convert the angle from degrees to radians
        alpha_radians = np.deg2rad(alpha)

        return a_sw / (s * b_w * np.sin(alpha_radians))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 9.4."""
        return LatexFormula(
            return_symbol=r"\rho_w",
            result=f"{self:.6f}",
            equation=r"\frac{A_{sw}}{s \cdot b_w \cdot sin(\alpha)}",
            numeric_equation=rf"\frac{{{self.a_sw:.2f}}}{{{self.s:.2f} \cdot {self.b_w:.2f} \cdot sin({self.alpha:.2f})}}",
            comparison_operator_label="=",
        )
