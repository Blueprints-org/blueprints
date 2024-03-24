"""Formula 5.9 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1993_5_2008 import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction, min_curly_brackets
from blueprints.type_alias import CM3, DEG, DIMENSIONLESS, KNM, MM, MM2, MPA
from blueprints.unit_conversion import CM3_TO_MM3, NMM_TO_KNM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot9ReducedBendingMomentResistance(Formula):
    """Class representing formula 5.9 for reduced design bending moment resistance of the cross-section."""

    label = "5.9"
    source_document = NEN_EN_1993_5_2008

    def __init__(  # noqa: PLR0913
        self,
        beta_b: DIMENSIONLESS,
        w_pl: CM3,
        rho: DIMENSIONLESS,
        a_v: MM2,
        t_w: MM,
        alpha: DEG,
        f_y: MPA,
        gamma_m_0: DIMENSIONLESS,
        mc_rd: KNM,
    ) -> None:
        """(:math:`M_{V,Rd}`) Calculate reduced design bending moment resistance of the cross-section allowing for the shear force in [:math:`kNm`].

        NEN-EN 1993-5:2008(E) art.5.2.2(9) - Formula (5.9)

        Parameters
        ----------
        beta_b : DIMENSIONLESS
            (:math:`β_{b}`) Reduction factor for the bending resistance of the cross-section in [-].
            Defined in NEN-EN 1993-5:2007(E) art. 5.2.2(2) or CUR166, part 2, par. 3.3.2.
        w_pl : CM3
            (:math:`W_{pl}`) Plastic section modulus in [:math:`cm³`].
        rho : DIMENSIONLESS
            (:math:`ρ`) Reduction factor for shear resistance of the cross-section, according NEN-EN 1993-5:2007(E) art. 5.2.2(9) formula 5.10 [-].
        a_v : MM2
            (:math:`A_{V}`) Projected shear area for each web, acting in the same direction as VEd in [:math:`mm²`].
        t_w : MM
            (:math:`t_{w}`) Thickness of the web in [:math:`mm`].
        alpha : DEGREE
            (:math:`α`) the inclination of the web according to NEN-EN 1993-5:2007(E) Figure 5-1 in [degrees].
        f_y : MPA
            (:math:`f_{y}`) Yield strength in [:math:`MPa`].
        gamma_m_0 : DIMENSIONLESS
            (:math:`γ_{M0}`) Partial factor for material properties in [-].
        mc_rd : KNM
            (:math:`M_{c,Rd}`) Design moment resistance of the cross-section in [:math:`kNm`].

            :math:`M_{v,Rd} <= M_{c,Rd}`
        """
        super().__init__()
        self.beta_b: float = beta_b
        self.w_pl: float = w_pl
        self.rho: float = rho
        self.a_v: float = a_v
        self.t_w: float = t_w
        self.alpha: float = alpha
        self.f_y: float = f_y
        self.gamma_m_0: float = gamma_m_0
        self.mc_rd: float = mc_rd

    @staticmethod
    def _evaluate(  # noqa: PLR0913
        beta_b: DIMENSIONLESS,
        w_pl: CM3,
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
        m_v_rd = ((beta_b * w_pl * CM3_TO_MM3) - ((rho * a_v**2) / (4.0 * t_w * np.sin(np.deg2rad(alpha))))) * (f_y / gamma_m_0) * NMM_TO_KNM
        return min(m_v_rd, mc_rd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.9."""
        latex_equation = min_curly_brackets(
            r"\left(\beta_b \cdot W_{pl} - \frac{\rho \cdot A_v^2}{4 \cdot t_w \cdot \sin(\alpha)}\right) \cdot \frac{f_y}{\gamma_{M0}}, M_{c,Rd}"
        )
        return LatexFormula(
            return_symbol=r"M_{V,Rd}",
            result=str(self),
            equation=latex_equation,
            numeric_equation=(
                min_curly_brackets(
                    rf"\left({self.beta_b} \cdot {self.w_pl} \cdot 10^3 - \frac{{{self.rho} \cdot {self.a_v}^2}}{{4 \cdot {self.t_w} \cdot "
                    rf"\sin({self.alpha})}}\right) \cdot {latex_fraction(self.f_y, self.gamma_m_0)} \cdot 10^{{-6}}, {self.mc_rd}"
                )
            ),
            comparison_operator_label="=",
        )
