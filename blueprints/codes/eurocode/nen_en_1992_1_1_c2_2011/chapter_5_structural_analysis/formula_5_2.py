"""Formula 5.1 from NEN-EN 1992-1-1+C2:2011: Chapter Structural Analysis."""
# pylint: disable=arguments-differ
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import M


class Form5Dot2Eccentricity(Formula):
    """Class representing formula 5.2 for the calculation of eccentricity, ei."""

    label = "5.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        theta_i: float,
        l_0: M,
    ) -> None:
        """[ei] Eccentricity, ei, for isolated members [m].

        NEN-EN 1992-1-1+C2:2011 art.5.2(7) - Formula (5.2)

        Parameters
        ----------
        theta_i : float
            [Θi] Eccentricity [m].
        theta_i : float
            [Θi] Initial inclination imperfections, Θi, is a ratio between height and inclination of the member [-].
            Use your own implementation of this value or use the Form5Dot1Imperfections class.
        """
        super().__init__()
        self.theta_i = theta_i
        self.l_0 = l_0

    @staticmethod
    def _evaluate(
        theta_i: float,
        l_0: M,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method"""
        if theta_i < 0:
            raise ValueError(f"Negative theta_i: {theta_i}. theta_i cannot be negative")
        if l_0 <= 0:
            raise ValueError(f"Invalid l_0: {l_0}. l_0 cannot be negative or zero")
        return theta_i * l_0 / 2
