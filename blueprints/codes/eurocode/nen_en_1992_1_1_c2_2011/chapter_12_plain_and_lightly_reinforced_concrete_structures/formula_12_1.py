"""Formula 12.1 from NEN-EN 1992-1-1+C2:2011: Chapter 12 - Plain and Lightly Reinforced Concrete Structures."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form12Dot1PlainConcreteTensileStrength(Formula):
    r"""Class representing formula 12.1 for the calculation of the design tensile strength of plain concrete,
    :math:`f_{ctd,pl}`.

    NEN-EN 1992-1-1+C2:2011 art.12.3.1 - Formula (12.1)
    """

    label = "12.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_ct_pl: DIMENSIONLESS,
        f_ctk_0_05: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> None:
        r"""[:math:`f_{ctd,pl}`] Design tensile strength of plain concrete [:math:`MPa`].

        NEN-EN 1992-1-1+C2:2011 art.12.3.1 - Formula (12.1)

        Parameters
        ----------
        alpha_ct_pl : DIMENSIONLESS
            [:math:`\\alpha_{ct,pl}`] Reduction factor for plain concrete [-].
        f_ctk_0_05 : MPa
            [:math:`f_{ctk,0.05}`] Characteristic tensile strength of concrete [:math:`MPa`].
        gamma_c : DIMENSIONLESS
            [:math:`\\gamma_{C}`] Partial safety factor for concrete [-].
        """
        super().__init__()
        self.alpha_ct_pl = alpha_ct_pl
        self.f_ctk_0_05 = f_ctk_0_05
        self.gamma_c = gamma_c

    @staticmethod
    def _evaluate(
        alpha_ct_pl: DIMENSIONLESS,
        f_ctk_0_05: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            alpha_ct_pl=alpha_ct_pl,
            f_ctk_0_05=f_ctk_0_05,
        )
        raise_if_less_or_equal_to_zero(gamma_c=gamma_c)
        return alpha_ct_pl * f_ctk_0_05 / gamma_c

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 12.1."""
        return LatexFormula(
            return_symbol=r"f_{ctd,pl}",
            result=f"{self:.3f}",
            equation=r"\alpha_{ct,pl} \cdot \frac{f_{ctk,0.05}}{\gamma_{C}}",
            numeric_equation=rf"{self.alpha_ct_pl:.3f} \cdot \frac{{{self.f_ctk_0_05:.3f}}}{{{self.gamma_c:.3f}}}",
            comparison_operator_label="=",
        )
