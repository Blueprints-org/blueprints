"""Formula 12.2 from EN 1992-1-1:2004: Chapter 12 - Plain and Lightly Reinforced Concrete Structures."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form12Dot2PlainConcreteBendingResistance(Formula):
    r"""Class representing formula 12.2 for the calculation of the design bending resistance of plain concrete,
    :math:`N_{Rd}`.

    EN 1992-1-1:2004 art.12.6.1(3) - Formula (12.2)
    """

    label = "12.2"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        eta_f_cd_pl: MPA,
        b: MM,
        h_w: MM,
        e: MM,
    ) -> None:
        r"""[:math:`N_{Rd}`] Design bending resistance of plain concrete [:math:`N`].

        EN 1992-1-1:2004 art.12.6.1(3) - Formula (12.2)

        Parameters
        ----------
        eta_f_cd_pl : MPa
            [:math:`\eta f_{cd,pl}`] Effective design compressive strength [:math:`MPa`].
        b : mm
            [:math:`b`] Total width of the cross-section [:math:`mm`].
        h_w : mm
            [:math:`h_w`] Total height of the cross-section [:math:`mm`].
        e : mm
            [:math:`e`] Eccentricity of :math:`N_{Ed}` in the direction of :math:`h_w` [:math:`mm`].
        """
        super().__init__()
        self.eta_f_cd_pl = eta_f_cd_pl
        self.b = b
        self.h_w = h_w
        self.e = e

    @staticmethod
    def _evaluate(
        eta_f_cd_pl: MPA,
        b: MM,
        h_w: MM,
        e: MM,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            eta_f_cd_pl=eta_f_cd_pl,
            b=b,
            e=e,
        )
        raise_if_less_or_equal_to_zero(
            h_w=h_w,
        )
        return eta_f_cd_pl * b * h_w * (1 - 2 * e / h_w)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 12.2."""
        return LatexFormula(
            return_symbol=r"N_{Rd}",
            result=f"{self:.{n}f}",
            equation=r"\eta f_{cd,pl} \cdot b \cdot h_w \cdot \left(1 - \frac{2e}{h_w}\right)",
            numeric_equation=rf"{self.eta_f_cd_pl:.{n}f} \cdot {self.b:.{n}f} \cdot {self.h_w:.{n}f} "
            rf"\cdot \left(1 - \frac{{2 \cdot {self.e:.{n}f}}}{{{self.h_w:.{n}f}}}\right)",
            comparison_operator_label="=",
        )
