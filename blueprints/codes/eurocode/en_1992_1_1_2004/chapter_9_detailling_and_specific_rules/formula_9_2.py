"""Formula 9.2 from EN 1992-1-1:2004: Chapter 9 - Detailing of members and particular rules."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG, MM
from blueprints.validations import raise_if_greater_than_90, raise_if_negative


class Form9Dot2ShiftInMomentDiagram(Formula):
    """Class representing the formula 9.2 for the calculation of the shift in the moment diagram for elements with shear reinforcement."""

    label = "9.2"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        z: MM,
        theta: DEG,
        alpha: DEG,
    ) -> None:
        r"""[$a_l$] Shift in the moment diagram of an element with shear reinforcement [$mm$].

        EN 1992-1-1:2004 art.9.2.1.3(2) - Formula (9.2)

        Parameters
        ----------
        z: MM
            [$z$] The internal lever arm for an element with constant height, corresponding to the bending moment in the considered element. In the
            shear force calculation of reinforced concrete without axial force, the approximate value [$z = 0.9d$] may generally be used [$mm$].
        alpha: DEG
            [$\alpha$] The angle between the shear reinforcement and the longitudinal axis of the beam (see 9.2.2(1)) [$deg$].
        theta: DEG
            [$\theta$] The angle between the shear compression strut and the axis of the beam 6.2.3 [$C1$] [$deg$].
        """
        super().__init__()
        self.z = z
        self.theta = theta
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        z: MM,
        theta: DEG,
        alpha: DEG,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(z=z, theta=theta, alpha=alpha)
        raise_if_greater_than_90(theta=theta, alpha=alpha)

        # Convert the angle from degrees to radians
        theta_radians = np.deg2rad(theta)
        alpha_radians = np.deg2rad(alpha)

        # Calculate the cotangent
        cot_theta = 1 / np.tan(theta_radians)
        cot_alpha = 1 / np.tan(alpha_radians)

        return z * (cot_theta - cot_alpha) / 2

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 9.2."""
        return LatexFormula(
            return_symbol=r"a_l",
            result=f"{self:.{n}f}",
            equation=r"z \cdot \left( \cot(\theta) - \cot(\alpha) \right) / 2",
            numeric_equation=rf"{self.z:.{n}f} \cdot \left( \cot({self.theta:.{n}f}) - \cot({self.alpha:.{n}f}) \right) / 2",
            comparison_operator_label="=",
        )
