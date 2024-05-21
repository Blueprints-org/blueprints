"""Formula A.1 from NEN-EN 1993-1-9+C2:2012: Annex A - Determination of fatigue load parameters and verification formats."""

from blueprints.codes.eurocode.nen_en_1993_1_9_c2_2012 import NEN_EN_1993_1_9_C2_2012
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative, raise_if_less_or_equal_to_zero
from blueprints.validations import raise_if_lists_differ_in_length, raise_if_list_is_empty

class FormADot1DamageDuringDesignLife(Formula):
    """Class representing formula A.1 for the calculation of the damage during the design life, :math:`D_d`"""

    label = "A.1"
    source_document = NEN_EN_1993_1_9_C2_2012

    def __init__(
        self,
        n_E: list[DIMENSIONLESS],
        N_R: list[DIMENSIONLESS]

    ) -> None:
        """[:math:`D_d`] The calculation of the damage during the design life [:math:`-`].

        NEN-EN 1993-1-9+C2:2012 art.A.5 - Formula (A.1)

        Parameters
        ----------
        n_E : list[DIMENSIONLESS]
            [:math:`n_E`] Contains number of cycles associated with the stress range γ_Ff·Δδ_i for each band i in the factored spectrum [:math:`-`].
        N_R : list[DIMENSIONLESS]
            [:math:`N_R`] Contains the endurance (in cycles) obtained from the factored Δδ_C/γ_Mf-N_r curve for each stress range of γ_Ff·Δδ_i [:math:`-`]

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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula A.1."""
        return LatexFormula(
            return_symbol=r"D_d",
            result=f"{self:.3f}",
            equation=r"\sum_{i}^{n} \frac{n_{Ei}}{N_Ri}",
            numeric_equation="".join(rf"\frac{{{self.n_E[i]:.3f}}}{{{self.N_R[i]:.3f}}} + " for i in range(len(self.N_R)))[:-3],
            comparison_operator_label="=",
        )