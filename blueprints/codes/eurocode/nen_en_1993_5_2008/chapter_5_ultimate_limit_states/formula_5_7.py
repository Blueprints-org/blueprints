"""Formula 5.7 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_5_2008 import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction
from blueprints.type_alias import DIMENSIONLESS, KN, MM, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot7ShearBucklingResistance(Formula):
    """Class representing formula 5.7 for shear buckling resistance."""

    label = "5.7"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        h: MM,
        t_f: MM,
        t_w: MM,
        f_bv: MPA,
        gamma_m_0: DIMENSIONLESS,
    ) -> None:
        r"""[$V_{b,Rd}$] Calculate the shear buckling resistance [$kN$].

        NEN-EN 1993-5:2008(E) art.5.2.2(7) - Formula (5.7)

        Parameters
        ----------
        h : MM
            [$h$] Height of the web in [$mm$].
        t_f : MM
            [$t_{f}$] Thickness of the flange in [$mm$].
        t_w : MM
            [$t_{w}$] Thickness of the web in [$mm$].
        f_bv : MPA
            [$f_{bv}$] Shear buckling strength according to Table 6-1 of EN 1993-1-3 for a web without stiffening
            at the support and for a relative web slenderness [$MPa$].
        gamma_m_0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial factor for material properties [$-$].
        """
        super().__init__()
        self.h: float = h
        self.t_f: float = t_f
        self.t_w: float = t_w
        self.f_bv: float = f_bv
        self.gamma_m_0: float = gamma_m_0

    @staticmethod
    def _evaluate(
        h: MM,
        t_f: MM,
        t_w: MM,
        f_bv: MPA,
        gamma_m_0: DIMENSIONLESS,
    ) -> KN:
        """Evaluates the formula for shear buckling resistance."""
        raise_if_less_or_equal_to_zero(
            h=h,
            t_f=t_f,
            t_w=t_w,
            f_bv=f_bv,
            gamma_m_0=gamma_m_0,
        )
        if t_f >= h:
            raise ValueError("The thickness of the flange should be less than the height of the web.")
        return ((h - t_f) * t_w * f_bv / gamma_m_0) * N_TO_KN

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.7."""
        return LatexFormula(
            return_symbol=r"V_{b,Rd}",
            result=f"{self:.3f}",
            equation=latex_fraction(numerator=r"\left(h - t_f \right) t_w f_{bv}", denominator=r"\gamma_{M0}"),
            numeric_equation=latex_fraction(
                numerator=rf"({self.h:.2f} - {self.t_f:.2f}) \cdot {self.t_w} \cdot {self.f_bv:.3f}",
                denominator=self.gamma_m_0,
            ),
            comparison_operator_label="=",
        )
