"""Formula 5.45 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN, ONE_OVER_M, M
from blueprints.validations import raise_if_negative


class Form5Dot45LossesDueToFriction(Formula):
    r"""Class representing formula 5.45 for the calculation of losses due to friction in post-tensioned tendons, [$\Delta P_{\mu}(x)$]."""

    label = "5.45"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        p_max: KN,
        mu: DIMENSIONLESS,
        theta: DIMENSIONLESS,
        k: ONE_OVER_M,
        x: M,
    ) -> None:
        r"""[$\Delta P_{\mu}(x)$] Losses due to friction [$kN$].

        EN 1992-1-1:2004 art.5.10.5.2(1) - Formula (5.45)

        Parameters
        ----------
        p_max : KN
            [$P_{max}$] Force at the active end during tensioning [$kN$].
        mu : DIMENSIONLESS
            [$\mu$] Coefficient of friction between the tendon and its duct [$-$].
        theta : DIMENSIONLESS
            [$\theta$] Sum of the angular displacements over a distance x (irrespective of direction or sign) [$-$].
        k : ONE_OVER_M
            [$k$] Unintentional angular displacement for internal tendons (per unit length) [$1/m$].
        x : M
            [$x$] Distance along tendon from point where the prestressing force equals Pmax (force at active end during tensioning) [$m$].
        """
        super().__init__()
        self.p_max = p_max
        self.mu = mu
        self.theta = theta
        self.k = k
        self.x = x

    @staticmethod
    def _evaluate(
        p_max: KN,
        mu: DIMENSIONLESS,
        theta: DIMENSIONLESS,
        k: ONE_OVER_M,
        x: M,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            p_max=p_max,
            mu=mu,
            theta=theta,
            k=k,
            x=x,
        )

        return p_max * (1 - (np.e ** (-mu * (theta + k * x))))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.45."""
        return LatexFormula(
            return_symbol=r"\Delta P_{\mu}(x)",
            result=f"{self:.{n}f}",
            equation=r"P_{max} \cdot \left( 1 - e^{-\mu \cdot (\theta + k \cdot x)} \right)",
            numeric_equation=rf"{self.p_max:.{n}f} \cdot \left( 1 - e^{{-{self.mu:.{n}f} \cdot ({self.theta:.{n}f} + "
            rf"{self.k:.{n}f} \cdot {self.x:.{n}f})}} \right)",
            comparison_operator_label="=",
            unit="kN",
        )
