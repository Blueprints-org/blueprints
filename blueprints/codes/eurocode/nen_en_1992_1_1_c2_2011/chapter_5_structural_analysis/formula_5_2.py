"""Formula 5.1 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot2Eccentricity(Formula):
    """Class representing formula 5.2 for the calculation of eccentricity, ei."""

    label = "5.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        theta_i: DIMENSIONLESS,
        l_0: M,
    ) -> None:
        """[ei] Eccentricity, ei, for isolated members [m].

        NEN-EN 1992-1-1+C2:2011 art.5.2(7) - Formula (5.2)

        Parameters
        ----------
        theta_i : DIMENSIONLESS
            [Θi] Eccentricity, initial inclination imperfections [-].
            Use your own implementation of this value or use the Form5Dot1Imperfections class.
        l_0 : M
            [l0] Effective length of the member, see 5.8.3.2 [m].
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
