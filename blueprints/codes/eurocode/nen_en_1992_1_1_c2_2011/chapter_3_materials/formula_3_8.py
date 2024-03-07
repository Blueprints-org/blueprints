"""Formula 3.8 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula


class Form3Dot8TotalShrinkage(Formula):
    """Class representing formula 3.8 for the calculation of the total shrinkage."""

    label = "3.8"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        epsilon_cd: float,
        epsilon_ca: float,
    ) -> None:
        """[εcs] The total shrinkage [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.8)

        Parameters
        ----------
        epsilon_cd : float
            [εcd] Drying shrinkage [-].
        epsilon_ca : float
            [εca] Autogene shrinkage [-].

        Returns
        -------
        None
        """
        super().__init__()
        self.epsilon_cd = epsilon_cd
        self.epsilon_ca = epsilon_ca

    @staticmethod
    def _evaluate(
        epsilon_cd: float,
        epsilon_ca: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        return epsilon_cd + epsilon_ca
