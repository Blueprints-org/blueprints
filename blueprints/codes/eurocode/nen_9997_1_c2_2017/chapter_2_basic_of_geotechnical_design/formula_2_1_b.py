"""Formula 2.1b from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

from blueprints.codes.eurocode.nen_9997_1_c2_2017 import NEN_9997_1_C2_2017
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form2Dot1bRepresentativeValue(Formula):
    """Class representing formula 2.1b for the calculation of the representative value :math:`F_{rep}` of actions."""

    label = "2.1b"
    source_document = NEN_9997_1_C2_2017

    def __init__(self, psi: DIMENSIONLESS, f_k: float) -> None:
        """[:math:`F_{rep}`] Representative value of actions.

        NEN 9997-1+C2:2017 art.2.4.6.1(2) - Formula (2.1b)

        Parameters
        ----------
        psi : DIMENSIONLESS
            [:math:`Ψ`] factor for converting the characteristic value to the representative value [-].
        f_k : float
            [:math:`F_{k}`] Characteristic value of actions.
        """
        super().__init__()
        self.psi = psi
        self.f_k = f_k

    @staticmethod
    def _evaluate(
        psi: DIMENSIONLESS,
        f_k: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(psi=psi)
        return psi * f_k
