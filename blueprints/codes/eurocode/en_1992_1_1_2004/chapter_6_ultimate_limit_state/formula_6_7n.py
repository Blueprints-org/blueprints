"""Formula 6.7n from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.math_helpers import cot
from blueprints.type_alias import DEG
from blueprints.validations import raise_if_greater_than_90, raise_if_negative


class Form6Dot7nCheckCotTheta(Formula):
    r"""Class representing formula 6.7n for check of cotangent of theta."""

    label = "6.7n"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        theta: DEG,
    ) -> None:
        r"""Check if cotangent of theta is between 1 and 2.5.

        EN 1992-1-1:2004 art.6.2.3(2) - Formula (6.7n)

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
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_greater_than_90(theta=theta)
        raise_if_negative(theta=theta)

        return (cot(theta) >= 1) and (cot(theta) <= 2.5)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.7n."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"1 \leq \cot(\theta) \leq 2.5",
            numeric_equation=rf"1 \leq \cot({self.theta:.{n}f}) \leq 2.5",
            comparison_operator_label="\\to",
            unit="",
        )
