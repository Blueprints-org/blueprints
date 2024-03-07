"""Formula 3.5 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MPA


class Form3Dot5ApproximationVarianceElasticModulusOverTime(Formula):
    """Class representing formula 3.5 for the approximation of the elastic modulus, Ecm(t) at day t."""

    label = "3.5"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_cm_t: MPA,
        f_cm: MPA,
        e_cm: MPA,
    ) -> None:
        """[Ecm(t)] The approximated elastic modulus at day t [MPa].

        NEN-EN 1992-1-1+C2:2011 art.3.1.3(3) - Formula (3.5)

        Parameters
        ----------
        f_cm_t : MPA
            [fcm(t)] Compressive strength concrete at t days [MPa].
        f_cm : MPA
            [fcm] Average concrete compressive strength on day 28 based on table 3.1 [MPa].
        e_cm : MPA
            [Ecm] Average elastic modulus on day 28 [MPa].

        Returns
        -------
        None
        """
        super().__init__()
        self.f_cm_t = f_cm_t
        self.f_cm = f_cm
        self.e_cm = e_cm

    @staticmethod
    def _evaluate(
        f_cm_t: MPA,
        f_cm: MPA,
        e_cm: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        if f_cm_t < 0:
            raise ValueError(f"Negative f_cm_t: {f_cm_t}. f_cm_t cannot be negative")
        if f_cm < 0:
            raise ValueError(f"Negative f_cm: {f_cm}. f_cm cannot be negative")
        if e_cm < 0:
            raise ValueError(f"Negative e_cm: {e_cm}. e_cm cannot be negative")
        return (f_cm_t / f_cm) ** 0.3 * e_cm
