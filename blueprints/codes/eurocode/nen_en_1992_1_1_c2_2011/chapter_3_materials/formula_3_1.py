"""Formula 3.1 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_negative


class Form3Dot1EstimationConcreteCompressiveStrength(Formula):
    """Class representing formula 3.1 for the estimation of the concrete compressive strength, fcm(t),  after t days
    with an average temperature of 20 degrees Celsius.
    """

    label = "3.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        beta_cc_t: float,
        f_cm: MPA,
    ) -> None:
        """[fcm(t)] The estimated concrete compressive strength [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.2(6) - Formula (3.1)

        Parameters
        ----------
        beta_cc_t : float
            [βcc(t)] Coefficient dependent of the age of concrete [-].
        f_cm : MPA
            [fcm] Average concrete compressive strength on day 28 based on table 3.1 [MPa].

        Returns
        -------
        None
        """
        super().__init__()
        self.beta_cc_t = beta_cc_t
        self.f_cm = f_cm

    @staticmethod
    def _evaluate(
        beta_cc_t: float,
        f_cm: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(beta_cc_t=beta_cc_t, f_cm=f_cm)
        return beta_cc_t * f_cm
