"""Formula A.1 from NEN-EN 1993-1-9+C2:2012: Annex A - Determination of fatigue load parameters and verification formats."""

from blueprints.codes.eurocode.nen_en_1993_1_9_c2_2012 import NEN_EN_1993_1_9_C2_2012
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class FormADot2CriteriaBasedOnDamageAccumulation(Formula):
    """Class representing formula A.2 for the calculation of the damage during the design life."""

    label = "A.2"
    source_document = NEN_EN_1993_1_9_C2_2012

    def __init__(
        self,
        d_d: DIMENSIONLESS,
    ) -> None:
        r"""[$CHECK$] Criteria met, based on damage accumulation.

        NEN-EN 1993-1-9+C2:2012 art.A.5 - Formula (A.1)

        Parameters
        ----------
        d_d : DIMENSIONLESS
            [$D_d$] The damage during the design life [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.d_d = d_d

    @staticmethod
    def _evaluate(
        d_d: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d_d=d_d)
        return d_d <= 1.0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula A.2."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self <= 1 else r"NOT\;OK",
            equation=r"D_d \leq 1.0",
            numeric_equation=rf"{self.d_d:.3f} \leq 1.0",
            comparison_operator_label=r"\rightarrow",
        )
