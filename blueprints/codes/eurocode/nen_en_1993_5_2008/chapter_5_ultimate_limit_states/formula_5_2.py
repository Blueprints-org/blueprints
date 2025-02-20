"""Formula 5.2 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit states."""

from blueprints.codes.eurocode.nen_en_1993_5_2008 import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KNM, MM3, MPA
from blueprints.unit_conversion import MM3_TO_M3, MPA_TO_KPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot2DesignMomentResistanceClass1Or2(Formula):
    """Class representing formula 5.2 for design moment resistance for Class 1 or 2 cross-sections."""

    label = "5.2"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        beta_b: DIMENSIONLESS,
        w_pl: MM3,
        f_y: MPA,
        gamma_m_0: DIMENSIONLESS,
    ) -> None:
        r"""[$M_{c,Rd}$] Calculate design moment resistance of the cross-section (class 1 or 2) in [$kNm/m$].

        NEN-EN 1993-5:2008(E) art.5.2.2(2) - Formula (5.2)

        Parameters
        ----------
        beta_b : DIMENSIONLESS
            [$\beta_{b}$] Reduction factor for the bending resistance of the cross-section in [$-$].
        w_pl : MM3
            [$W_{pl}$] Plastic section modulus in [$mm^3/m$].
        f_y : MPA
            [$f_{y}$] Yield strength in [$MPa$].
        gamma_m_0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial factor for material properties in [$-$].
        """
        super().__init__()
        self.beta_b = beta_b
        self.w_pl = w_pl
        self.f_y = f_y
        self.gamma_m_0 = gamma_m_0

    @staticmethod
    def _evaluate(
        beta_b: DIMENSIONLESS,
        w_pl: MM3,
        f_y: MPA,
        gamma_m_0: DIMENSIONLESS,
    ) -> KNM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(
            beta_b=beta_b,
            w_pl=w_pl,
            f_y=f_y,
            gamma_m_0=gamma_m_0,
        )
        return beta_b * (w_pl * MM3_TO_M3) * (f_y * MPA_TO_KPA) / gamma_m_0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.2."""
        return LatexFormula(
            return_symbol=r"M_{c,Rd}",
            result=str(self),
            equation=r"\beta_B W_{pl} f_y / \gamma_{M0}",
            numeric_equation=rf"{self.beta_b} \cdot {self.w_pl} \cdot {self.f_y} / {self.gamma_m_0} / 1000000",
            comparison_operator_label="=",
        )
