"""Formula 5.4 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.validations import raise_if_negative


class Form5Dot4TransverseForceEffectBracingSystem(Formula):
    """Class representing formula 5.4 for the calculation of the effect of the inclination on bracing systems, :math:`H_{i}`.

    See Figure 5.1 b.
    """

    label = "5.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        theta_i: DIMENSIONLESS,
        n_a: KN,
        n_b: KN,
    ) -> None:
        """[:math:`H_{i}`] Effect of the inclination on bracing systems [:math:`kN`].

        NEN-EN 1992-1-1+C2:2011 art.5.2(8) - Formula (5.4)

        Parameters
        ----------
        theta_i : DIMENSIONLESS
            [:math:`Θ_{i}`] Eccentricity, initial inclination imperfections [-].
        n_a : KN
            [:math:`N_{a}`] Axial force in the member [:math:`kN`].
        n_b : KN
            [:math:`N_{b}`] Axial force in the member [:math:`kN`].

        Notes
        -----
        where :math:`N_{a} and :math:`N_{b}` are longitudinal forces contributing to :math:`H_{i}`.
        Positive values for compression, tension is not allowed.
        """
        super().__init__()
        self.theta_i = theta_i
        self.n_a = n_a
        self.n_b = n_b

    @staticmethod
    def _evaluate(
        theta_i: DIMENSIONLESS,
        n_a: KN,
        n_b: KN,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            theta_i=theta_i,
            n_a=n_a,
            n_b=n_b,
        )
        return theta_i * (n_b - n_a)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.4."""
        return LatexFormula(
            return_symbol=r"H_{i}",
            result=f"{self:.3f}",
            equation=r"Θ_{i} \cdot (N_{b} - N_{a})",
            numeric_equation=rf"{self.theta_i:.3f} \cdot ({self.n_b:.3f} - {self.n_a:.3f})",
            comparison_operator_label="=",
        )
