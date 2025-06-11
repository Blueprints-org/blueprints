"""Formula 12.1 from EN 1992-1-1:2004: Chapter 12 - Plain and Lightly Reinforced Concrete Structures."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form12Dot1PlainConcreteTensileStrength(Formula):
    r"""Class representing formula 12.1 for the calculation of the design tensile strength of plain concrete,
    :math:`f_{ctd,pl}`.

    EN 1992-1-1:2004 art.12.3.1(2) - Formula (12.1)
    """

    label = "12.1"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        alpha_ct: DIMENSIONLESS,
        f_ctk_0_05: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> None:
        r"""[:math:`f_{ctd,pl}`] Design tensile strength of plain concrete [:math:`MPa`].

        EN 1992-1-1:2004 art.12.3.1(2) - Formula (12.1)

        Parameters
        ----------
        alpha_ct : DIMENSIONLESS
            [:math:`\\alpha_{ct,pl}`] Reduction factor for plain concrete [-].
        f_ctk_0_05 : MPa
            [:math:`f_{ctk,0.05}`] Characteristic tensile strength of concrete [:math:`MPa`].
        gamma_c : DIMENSIONLESS
            [:math:`\\gamma_{C}`] Partial safety factor for concrete [-].
        """
        super().__init__()
        self.alpha_ct = alpha_ct
        self.f_ctk_0_05 = f_ctk_0_05
        self.gamma_c = gamma_c

    @staticmethod
    def _evaluate(
        alpha_ct: DIMENSIONLESS,
        f_ctk_0_05: MPA,
        gamma_c: DIMENSIONLESS,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            alpha_ct_pl=alpha_ct,
            f_ctk_0_05=f_ctk_0_05,
        )
        raise_if_less_or_equal_to_zero(gamma_c=gamma_c)
        return alpha_ct * f_ctk_0_05 / gamma_c

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 12.1."""
        return LatexFormula(
            return_symbol=r"f_{ctd,pl}",
            result=f"{self:.{n}f}",
            equation=r"\alpha_{ct,pl} \cdot \frac{f_{ctk,0.05}}{\gamma_{C}}",
            numeric_equation=rf"{self.alpha_ct:.{n}f} \cdot \frac{{{self.f_ctk_0_05:.{n}f}}}{{{self.gamma_c:.{n}f}}}",
            comparison_operator_label="=",
        )
