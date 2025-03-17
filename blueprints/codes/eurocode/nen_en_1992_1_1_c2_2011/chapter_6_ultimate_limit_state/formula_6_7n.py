"""Formula 6.7n from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG
from blueprints.validations import raise_if_greater_than_90, raise_if_negative


class Form6Dot7nCheckCotTheta(Formula):
    r"""Class representing formula 6.7n for check of cotangent of theta."""

    label = "6.7n"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        theta: DEG,
    ) -> None:
        r"""Check if cotangent of theta is between 1 and 2.5.

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(2) - Formula (6.7n)

        Parameters
        ----------
        theta : DEG
            [$\theta$] angle between the concrete compression strut and the beam axis perpendicular to the shear force [$-$].
        """
        super().__init__()
        self.theta = theta

    @staticmethod
    def _evaluate(
        theta: DEG,
    ) -> bool:
        def cot(theta: DEG) -> float:
            """Returns the cotangent of the given angle."""
            return 1 / np.tan(np.radians(theta))

        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_greater_than_90(theta=theta)
        raise_if_negative(theta=theta)

        return (cot(theta) >= 1) and (cot(theta) <= 2.5)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.7n."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"1 \leq \cot(\theta) \leq 2.5",
            numeric_equation=rf"1 \leq \cot({self.theta:.3f}) \leq 2.5",
            comparison_operator_label="\\to",
            unit="",
        )
