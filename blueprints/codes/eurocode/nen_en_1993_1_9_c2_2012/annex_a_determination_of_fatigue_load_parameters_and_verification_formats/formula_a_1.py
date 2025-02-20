"""Formula A.1 from NEN-EN 1993-1-9+C2:2012: Annex A - Determination of fatigue load parameters and verification formats."""

from blueprints.codes.eurocode.nen_en_1993_1_9_c2_2012 import NEN_EN_1993_1_9_C2_2012
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_lists_differ_in_length, raise_if_negative


class FormADot1DamageDuringDesignLife(Formula):
    """Class representing formula A.1 for the calculation of the damage during the design life [$D_d$]."""

    label = "A.1"
    source_document = NEN_EN_1993_1_9_C2_2012

    def __init__(self, n_e: list[DIMENSIONLESS], n_r: list[DIMENSIONLESS]) -> None:
        r"""[$D_d$] The calculation of the damage during the design life [$-$].

        NEN-EN 1993-1-9+C2:2012 art.A.5 - Formula (A.1)

        Parameters
        ----------
        n_e : list[DIMENSIONLESS]
            [$n_E$] Contains number of cycles associated with the stress range [$\gamma_{Ff} \cdot \Delta\sigma_i$]
            for each band i in the factored spectrum [$-$].
        n_r : list[DIMENSIONLESS]
            [$N_R$] Contains the endurance (in cycles) obtained from the factored [$\Delta\sigma_C / \gamma_{Mf} - n_r$] curve for
            each stress range of [$\gamma_{Ff} \cdot \Delta_i$] [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.n_e = n_e
        self.n_r = n_r

    @staticmethod
    def _evaluate(
        n_e: list[DIMENSIONLESS],
        n_r: list[DIMENSIONLESS],
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_lists_differ_in_length(n_e=n_e, n_r=n_r)
        raise_if_negative(n_e_min=min(n_e))
        raise_if_less_or_equal_to_zero(n_r_min=min(n_r))
        return sum([n_e[i] / n_r[i] for i in range(len(n_e))])

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula A.1."""
        return LatexFormula(
            return_symbol=r"D_d",
            result=f"{self:.3f}",
            equation=r"\sum_{i}^{n} \frac{n_{Ei}}{N_Ri}",
            numeric_equation="".join(rf"\frac{{{self.n_e[i]:.3f}}}{{{self.n_r[i]:.3f}}} + " for i in range(len(self.n_r)))[:-3],
            comparison_operator_label="=",
        )
