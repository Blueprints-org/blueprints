"""Formula 2.2 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 2: Basis of design."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form2Dot2CharacteristicValueResistance(Formula):
    """Class representing formula 2.2 for the calculation of the characteristic value of the resistance :math:`R_k`."""

    label = "2.2"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(self, r_d: float, gamma_mi: DIMENSIONLESS) -> None:
        """[:math:`R_k`] Characteristic value of the resistance [:math:`kN`].

        NEN-EN 1993-1-1+C2+A1:2016 art.2.5(2) - Formula (2.2)

        Parameters
        ----------
        r_d : float
            [:math:`R_d`] Design value of the resistance according to Annex D of EN 1990.
        gamma_mi : DIMENSIONLESS
            [:math:`γ_{Mi}`] Recommended partial factors for the resistance.
        """
        super().__init__()
        self.r_d = r_d
        self.gamma_mi = gamma_mi

    @staticmethod
    def _evaluate(r_d: float, gamma_mi: DIMENSIONLESS) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(r_d=r_d, gamma_mi=gamma_mi)
        return r_d * gamma_mi
