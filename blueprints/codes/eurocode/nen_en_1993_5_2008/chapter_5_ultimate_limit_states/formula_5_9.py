"""Formula 5.9 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1993_5_2008 import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction, latex_min_curly_brackets
from blueprints.type_alias import DEG, DIMENSIONLESS, KNM, MM, MM2, MM3, MPA
from blueprints.unit_conversion import NMM_TO_KNM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot9ReducedBendingMomentResistance(Formula):
    """Class representing formula 5.9 for reduced design bending moment resistance of the cross-section."""

    label = "5.9"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        beta_b: DIMENSIONLESS,
        w_pl: MM3,
        rho: DIMENSIONLESS,
        a_v: MM2,
        t_w: MM,
        alpha: DEG,
        f_y: MPA,
        gamma_m_0: DIMENSIONLESS,
        mc_rd: KNM,
    ) -> None:
        r"""[$M_{V,Rd}$] Calculate reduced design bending moment resistance of the cross-section allowing for the shear force in [$kNm$].

        This calculation is specifically for sheet pile cross-sections, particularly U-profiles and Z-profiles.

        NEN-EN 1993-5:2008(E) art.5.2.2(9) - Formula (5.9)

        Parameters
        ----------
        beta_b : DIMENSIONLESS
            [$β_{b}$] Reduction factor for the bending resistance of the cross-section, which takes account of
            possible lack of shear force transmission in the interlocks [$-$].
            Defined in NEN-EN 1993-5:2008(E) art. 5.2.2(2) or CUR166, part 2, par. 3.3.2.
        w_pl : MM3
            [$W_{pl}$] Plastic section modulus in [$mm^3$].
        rho : DIMENSIONLESS
            [$ρ$] Reduction factor for shear resistance of the cross-section, according NEN-EN 1993-5:2008(E) art. 5.2.2(9) formula 5.10 [$-$].
        a_v : MM2
            [$A_{V}$] Projected shear area for each web, acting in the same direction as VEd in [$mm^2$].
        t_w : MM
            [$t_{w}$] Thickness of the web in [$mm$].
        alpha : DEG
            [$α$] the inclination of the web according to NEN-EN 1993-5:2008(E) Figure 5-1 in [$degrees$].
        f_y : MPA
            [$f_{y}$] Yield strength in [$MPa$].
        gamma_m_0 : DIMENSIONLESS
            [$γ_{M0}$] Partial factor for material properties in [$-$].
        mc_rd : KNM
            [$M_{c,Rd}$] Design moment resistance of the cross-section in [$kNm$].

            The `mc_rd` parameter represents the design moment resistance of the cross-section.
            In the context of the formula for reduced bending moment resistance, it serves as an upper bound.
            The formula calculates the reduced design bending moment resistance (`m_v_rd`) and then returns the minimum of `m_v_rd` and `mc_rd`.
            This means that the result of the formula will never exceed `mc_rd`, making `mc_rd` an upper bound for this formula.

            [$M_{v,Rd} \leq M_{c,Rd}$]
        """
        super().__init__()
        self.beta_b: DIMENSIONLESS = beta_b
        self.w_pl: MM3 = w_pl
        self.rho: DIMENSIONLESS = rho
        self.a_v: MM2 = a_v
        self.t_w: MM = t_w
        self.alpha: DEG = alpha
        self.f_y: MPA = f_y
        self.gamma_m_0: DIMENSIONLESS = gamma_m_0
        self.mc_rd: KNM = mc_rd

    @staticmethod
    def _evaluate(
        beta_b: DIMENSIONLESS,
        w_pl: MM3,
        rho: DIMENSIONLESS,
        a_v: MM2,
        t_w: MM,
        alpha: DEG,
        f_y: MPA,
        gamma_m_0: DIMENSIONLESS,
        mc_rd: KNM,
    ) -> KNM:
        """Evaluates the formula for reduced bending moment resistance."""
        raise_if_less_or_equal_to_zero(beta_b=beta_b, w_pl=w_pl, rho=rho, a_v=a_v, t_w=t_w, alpha=alpha, f_y=f_y, gamma_m_0=gamma_m_0, mc_rd=mc_rd)
        m_v_rd = ((beta_b * w_pl) - ((rho * a_v**2) / (4.0 * t_w * np.sin(np.deg2rad(alpha))))) * (f_y / gamma_m_0) * NMM_TO_KNM
        return min(m_v_rd, mc_rd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.9."""
        latex_equation = latex_min_curly_brackets(
            r"\left(\beta_b \cdot W_{pl} - \frac{\rho \cdot A_v^2}{4 \cdot t_w \cdot \sin(\alpha)}\right) \cdot \frac{f_y}{\gamma_{M0}}, M_{c,Rd}"
        )
        fraction = latex_fraction(numerator=f"{self.f_y:.2f}", denominator=f"{self.gamma_m_0:.2f}")
        return LatexFormula(
            return_symbol=r"M_{V,Rd}",
            result=f"{self:.3f}",
            equation=latex_equation,
            numeric_equation=(
                latex_min_curly_brackets(
                    rf"\left({self.beta_b:.2f} \cdot {self.w_pl:.2f} - \frac{{{self.rho:.2f} \cdot {self.a_v:.2f}^2}}{{4 \cdot {self.t_w:.2f} \cdot "
                    rf"\sin({self.alpha:.2f})}}\right) \cdot "
                    rf"{fraction} \cdot 10^{{-6}}, {self.mc_rd:.2f}"
                )
            ),
            comparison_operator_label="=",
        )
