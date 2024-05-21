"""Formula A.1 from NEN-EN 1993-1-9+C2:2012: Annex A - Determination of fatigue load parameters and verification formats."""

from blueprints.codes.eurocode.nen_en_1993_1_9_c2_2012 import NEN_EN_1993_1_9_C2_2012
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative, raise_if_less_or_equal_to_zero
from blueprints.validations import raise_if_lists_differ_in_length, raise_if_list_is_empty

class FormADot1DamageDuringDesignLife(Formula):
    """Class representing formula A.1 for the calculation of the damage during the design life, D_d"""

    label = "A.1"
    source_document = NEN_EN_1993_1_9_C2_2012

    def __init__(
        self,
        n_E: list[DIMENSIONLESS],
        N_R: list[DIMENSIONLESS]

    ) -> None:
        """[fcm(t)] The calculation of the damage during the design life [-].

        NEN-EN 1993-1-9+C2:2012 art.A.5 - Formula (A.1)

        Parameters
        ----------
        n_E : list[DIMENSIONLESS]
            [n_E] Contains number of cycles associated with the stress range γ_Ff·Δδ_i for each band i in the factored spectrum [-].
        N_R : list[DIMENSIONLESS]
            [N_R] Contains the endurance (in cycles) obtained from the factored Δδ_C/γ_Mf-N_r curve for each stress range of γ_Ff·Δδ_i [-]

        Returns
        -------
        None
        """
        super().__init__()
        self.n_E = n_E
        self.N_R = N_R

    @staticmethod
    def _evaluate(
        n_E: list[DIMENSIONLESS],
        N_R: list[DIMENSIONLESS],
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_list_is_empty(n_E=n_E, N_R=N_R)
        raise_if_lists_differ_in_length(n_E=n_E, N_R=N_R)
        raise_if_negative(n_E_min=min(n_E))
        raise_if_less_or_equal_to_zero(N_R_min=min(N_R))
        return sum([n_E[i] / N_R[i] for i in range(len(n_E))])
