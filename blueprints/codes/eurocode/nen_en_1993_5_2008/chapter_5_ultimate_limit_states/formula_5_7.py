"""Formula 5.7 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, fraction
from blueprints.type_alias import KN, MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot7ShearBucklingResistance(Formula):
    """Class representing formula 5.7 for shear buckling resistance."""

    label = "5.7"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        h: MM,  # Height of the web
        tf: MM,  # Thickness of the flange
        tw: MM,  # Thickness of the web
        f_bv: KN,  # Shear buckling strength
        gamma_m_0: float,  # Partial factor for material properties
    ) -> None:
        """[Vb,Rd] Calculate the shear buckling resistance based on formula 5.7 from NEN-EN 1993-5:2007(E) art. 5.2.2(7).

        Parameters
        ----------
        h : MM
            [h] Height of the web in [mm].
        tf : MM
            [tf] Thickness of the flange in [mm].
        tw : MM
            [tw] Thickness of the web in [mm].
        f_bv : KN
            [fbv] Shear buckling strength in [kN].
        gamma_m_0 : float
            [γM0] Partial factor for material properties.
        """
        super().__init__()
        self.h: float = h
        self.tf: float = tf
        self.tw: float = tw
        self.f_bv: float = f_bv
        self.gamma_m_0: float = gamma_m_0

    @staticmethod
    def _evaluate(
        h: MM,
        tf: MM,
        tw: MM,
        f_bv: KN,
        gamma_m_0: float,
    ) -> KN:
        """Evaluates the formula for shear buckling resistance."""
        raise_if_less_or_equal_to_zero(h=h, tf=tf, tw=tw, f_bv=f_bv, gamma_m_0=gamma_m_0)
        return (h - tf) * tw * f_bv / gamma_m_0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.7."""
        return LatexFormula(
            return_symbol=r"V_{b,Rd}",
            result=str(self),
            equation=fraction(r"\left(h - t_f \right) t_w f_{bv}", r"\gamma_{M0}"),
            numeric_equation=fraction(rf"({self.h} - {self.tf}) \cdot {self.tw} \cdot {self.f_bv}", self.gamma_m_0),
            comparison_operator_label="=",
        )
