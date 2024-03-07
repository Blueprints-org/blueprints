"""Formula 3.11 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula


class Form3Dot11AutogeneShrinkage(Formula):
    """Class representing formula 3.11, which calculates the autogene shrinkage."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.11"

    def __init__(
        self,
        beta_as_t: float,
        epsilon_ca_inf: float,
    ) -> None:
        """[εca(t)] Autogene shrinkage [-].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.11)

        Parameters
        ----------
        beta_as_t : float
            [βas(t)] Coefficient dependent on time in days for autogene shrinkage [-].
            = 1 - exp(-0.2 * t^0.5)
            Use your own implementation of this formula or use the Form3Dot13CoefficientTimeAutogeneShrinkage class
        epsilon_ca_inf : float
            [εca(∞)] Autogene shrinkage at infinity [-].
            = 2.5 * (fck - 10) E-6
            Use your own implementation of this formula or use the Form3Dot12AutogeneShrinkageInfinity class.

        Returns
        -------
        None
        """
        super().__init__()
        self.beta_as_t = beta_as_t
        self.epsilon_ca_inf = epsilon_ca_inf

    @staticmethod
    def _evaluate(
        beta_as_t: float,
        epsilon_ca_inf: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if beta_as_t < 0:
            raise ValueError(f"Invalid beta_as_t: {beta_as_t}. beta_as_t cannot be negative")
        return beta_as_t * epsilon_ca_inf
