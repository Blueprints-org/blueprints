"""Formula 5.101 from EN 1992-2:2005: Chapter 5 - Structural Analysis."""

import numpy as np

from blueprints.codes.eurocode.en_1992_2_2005 import EN_1992_2_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot101Imperfections(Formula):
    r"""Class representing formula 5.101 for the calculation of initial inclination imperfections, [$$\Theta_i$$]."""

    label = "5.101"
    source_document = EN_1992_2_2005

    def __init__(
        self,
        theta_0: DIMENSIONLESS,
        alpha_h: DIMENSIONLESS,
    ) -> None:
        r"""[$$\Theta_i$$] Initial inclination imperfections, [$$\Theta_i$$], is a ratio between height
        and inclination of the member [$$-$$].

        EN 1992-2:2005 art.5.2(5) - Formula (5.101)

        Parameters
        ----------
        theta_0 : DIMENSIONLESS
            [$$\Theta_0$$] Basic value [$$-$$].
            Note: The value of [$$\Theta_0$$] for use in a Country may be found in its National Annex.
            The recommended value is 1/200 [$$-$$].
        alpha_h : DIMENSIONLESS
            [$$\alpha_h$$] Reduction factor for length or height [$$-$$].
            Use your own implementation of this value or use the SubForm5Dot101ReductionFactorLengthOrHeight class.
        """
        super().__init__()
        self.theta_0 = theta_0
        self.alpha_h = alpha_h

    @staticmethod
    def _evaluate(
        theta_0: DIMENSIONLESS,
        alpha_h: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(theta_0=theta_0, alpha_h=alpha_h)
        return theta_0 * alpha_h

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.101."""
        return LatexFormula(
            return_symbol=r"\theta_i",
            result=f"{self:.{n + 1}f}",
            equation=r"\theta_0 \cdot \alpha_h",
            numeric_equation=rf"{self.theta_0:.{n}f} \cdot {self.alpha_h:.{n}f}",
            comparison_operator_label="=",
        )


class Form5Dot101Sub1ReductionFactorLengthOrHeight(Formula):
    r"""Class representing sub-formula 5.101 for the calculation of the reduction factor for length
    or height, [$$\alpha_h$$].
    """

    label = "5.101"
    source_document = EN_1992_2_2005

    def __init__(
        self,
        length: M,
    ) -> None:
        r"""[$$\alpha_h$$] Reduction factor for length or height [$$-$$].

        The calculated value of [$$\alpha_h$$] is below 1.0.

        NEN-EN 1992-2+C2:2005 art.5.2(105) - Formula (5.101)

        Parameters
        ----------
        length : M
            [$$length$$] Length or height [$$m$$].
        """
        super().__init__()
        self.length = length

    @staticmethod
    def _evaluate(
        length: M,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(length=length)
        return min(1, 2 / np.sqrt(length))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.101 subformula 1."""
        return LatexFormula(
            return_symbol=r"\alpha_h",
            result=f"{self:.{n}f}",
            equation=r"\min(2 / \sqrt{l}, 1)",
            numeric_equation=rf"\min( 2 / \sqrt{{{self.length:.{n}f}}}, 1)",
            comparison_operator_label="=",
        )
