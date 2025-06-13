"""Formula 5.2 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot2Eccentricity(Formula):
    """Class representing formula 5.2 for the calculation of eccentricity, [$e_i$]."""

    label = "5.2"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        theta_i: DIMENSIONLESS,
        l_0: M,
    ) -> None:
        r"""[$e_i$] Eccentricity, [$e_i$], for isolated members [$m$].

        EN 1992-1-1:2004 art.5.2(7) - Formula (5.2)

        Parameters
        ----------
        theta_i : DIMENSIONLESS
            [$\Theta_i$] Eccentricity, initial inclination imperfections [-].
            Use your own implementation of this value or use the Form5Dot2Imperfections class.
        l_0 : M
            [$l_0$] Effective length of the member, see 5.8.3.2 [$m$].
        """
        super().__init__()
        self.theta_i = theta_i
        self.l_0 = l_0

    @staticmethod
    def _evaluate(
        theta_i: float,
        l_0: M,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(theta_i=theta_i)
        raise_if_less_or_equal_to_zero(l_0=l_0)
        return theta_i * l_0 / 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.2."""
        return LatexFormula(
            return_symbol=r"e_i",
            result=f"{self:.4f}",
            equation=r"\theta_i \cdot l_0 / 2",
            numeric_equation=rf"{self.theta_i:.{n}f} \cdot {self.l_0:.{n}f} / 2",
            comparison_operator_label="=",
        )
