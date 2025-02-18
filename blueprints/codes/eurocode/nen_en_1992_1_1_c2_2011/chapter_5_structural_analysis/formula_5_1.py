"""Formula 5.1 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot1Imperfections(Formula):
    r"""Class representing formula 5.1 for the calculation of initial inclination imperfections, [$\Theta_i$]."""

    label = "5.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        theta_0: DIMENSIONLESS,
        alpha_h: DIMENSIONLESS,
        alpha_m: DIMENSIONLESS,
    ) -> None:
        r"""[$\\Theta_i$] Initial inclination imperfections, [$\\Theta_i$], is a ratio between height and inclination of the member [-].

        NEN-EN 1992-1-1+C2:2011 art.5.2(5) - Formula (5.1)

        Parameters
        ----------
        theta_0 : float
            [$\\Theta_0$] Basic value [-].
            Note: The value of [$\\Theta_0$] for use in a Country may be found in its National Annex.
            The recommended value is 1/200
        alpha_h : float
            [$\alpha_h$] Reduction factor for length or height [-].
            Use your own implementation of this value or use the SubForm5Dot1ReductionFactorLengthOrHeight class.
        alpha_m : float
            [$\alpha_m$] Reduction factor for number of members [-].
            Use your own implementation of this value or use the SubForm5Dot1ReductionFactorNumberOfMembers class.
        """
        super().__init__()
        self.theta_0 = theta_0
        self.alpha_h = alpha_h
        self.alpha_m = alpha_m

    @staticmethod
    def _evaluate(
        theta_0: DIMENSIONLESS,
        alpha_h: DIMENSIONLESS,
        alpha_m: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(theta_0=theta_0, alpha_h=alpha_h, alpha_m=alpha_m)
        return theta_0 * alpha_h * alpha_m

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.1."""
        return LatexFormula(
            return_symbol=r"\theta_i",
            result=f"{self:.4f}",
            equation=r"\theta_0 \cdot \alpha_h \cdot \alpha_m",
            numeric_equation=rf"{self.theta_0:.3f} \cdot {self.alpha_h:.3f} \cdot {self.alpha_m:.3f}",
            comparison_operator_label="=",
        )


class SubForm5Dot1ReductionFactorLengthOrHeight(Formula):
    r"""Class representing sub-formula 5.1 for the calculation of the reduction factor for length or height, [$\alpha_h$]."""

    label = "5.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        length: M,
    ) -> None:
        r"""[$\alpha_h$] Reduction factor for length or height [-].

        The calculated value of [$\alpha_h$] is between 2/3 and 1.0.

        NEN-EN 1992-1-1+C2:2011 art.5.2(5) - Formula (5.1)

        Parameters
        ----------
        length : M
            [$\text{length}$] Length or height, see art.5.2(6) [$m$].
        """
        super().__init__()
        self.length = length

    @staticmethod
    def _evaluate(
        length: M,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(length=length)
        # the value of alpha_h is between 2/3 and 1.0
        alpha_h = 2 / np.sqrt(length)
        if alpha_h < 2 / 3:
            return 2 / 3
        if alpha_h > 1:
            return 1
        return alpha_h

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.1 subformula 1."""
        return LatexFormula(
            return_symbol=r"\alpha_h",
            result=f"{self:.3f}",
            equation=r"\min( \max(2 / \sqrt{l}; 2/3); 1)",
            numeric_equation=rf"\min( \max(2 / \sqrt{{{self.length:.3f}}}; 2/3); 1)",
            comparison_operator_label="=",
        )


class SubForm5Dot1ReductionFactorNumberOfMembers(Formula):
    r"""Class representing sub-formula 5.1 for the calculation of the reduction factor for number of members, [$\alpha_m$]."""

    label = "5.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        members: int,
    ) -> None:
        r"""[$\alpha_m$] Reduction factor for number of members [-].

        NEN-EN 1992-1-1+C2:2011 art.5.2(5) - Formula (5.1)

        Parameters
        ----------
        members : int
            [$m$] Number of vertical members contributing to the total effect [-].
        """
        super().__init__()
        self.members = members

    @staticmethod
    def _evaluate(
        members: int,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(members=members)
        # the value of alpha_m is between 1.0 and 1.5
        return np.sqrt(0.5 * (1 + 1 / members))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.1 subformula 2."""
        return LatexFormula(
            return_symbol=r"\alpha_m",
            result=f"{self:.3f}",
            equation=r"\sqrt{0.5 \cdot ( 1 + 1 / m)}",
            numeric_equation=rf"\sqrt{{0.5 \cdot ( 1 + 1 / {self.members:.3f})}}",
            comparison_operator_label="=",
        )
