"""Formula 5.6 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.validations import raise_if_negative


class Form5Dot6TransverseForceEffectRoofDiaphragm(Formula):
    """Class representing formula 5.6 for the calculation of the effect of the inclination on roof diaphragm, [$H_{i}$].
    See Figure 5.1 c2.
    """

    label = "5.6"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        theta_i: DIMENSIONLESS,
        n_a: KN,
    ) -> None:
        r"""[$H_{i}$] Effect of the inclination on roof diaphragm [$kN$].

        NEN-EN 1992-1-1+C2:2011 art.5.2(8) - Formula (5.6)

        Parameters
        ----------
        theta_i : DIMENSIONLESS
            [$Θ_{i}$] Eccentricity, initial inclination imperfections [-].
        n_a : KN
            [$N_{a}$] Axial force in the member [$kN$].

        Notes
        -----
        where [$N_{a}$] is a longitudinal force contributing to [$H_{i}$].
        Positive values for compression, tension is not allowed.
        """
        super().__init__()
        self.theta_i = theta_i
        self.n_a = n_a

    @staticmethod
    def _evaluate(
        theta_i: DIMENSIONLESS,
        n_a: KN,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            theta_i=theta_i,
            n_a=n_a,
        )
        return theta_i * n_a

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.6."""
        return LatexFormula(
            return_symbol=r"H_{i}",
            result=f"{self:.3f}",
            equation=r"Θ_{i} \cdot N_{a}",
            numeric_equation=rf"{self.theta_i:.3f} \cdot {self.n_a:.3f}",
            comparison_operator_label="=",
        )
