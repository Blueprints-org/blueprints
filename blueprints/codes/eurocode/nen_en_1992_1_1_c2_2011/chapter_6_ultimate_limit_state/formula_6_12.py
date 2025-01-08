"""Formula 6.12 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot12CheckMaxEffectiveCrossSectionalAreaShearReinf(Formula):
    r"""Class representing formula 6.12 for checking the maximum effective cross-sectional area of the shear reinforcement."""

    label = "6.12"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_sw_max: MM2,
        f_ywd: MPA,
        b_w: MM,
        s: MM,
        alpha_cw: DIMENSIONLESS,
        nu_1: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        r"""Check the maximum effective cross-sectional area of the shear reinforcement.

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(3) - Formula (6.12)

        Parameters
        ----------
        a_sw_max : MM2
            [:math:`A_{sw,max}`] Maximum effective cross-sectional area of the shear reinforcement [:math:`mm^2`].
        f_ywd : MPA
            [:math:`f_{ywd}`] Design yield strength of the shear reinforcement [:math:`MPa`].
        b_w : MM
            [:math:`b_{w}`] Width of the web [:math:`mm`].
        s : MM
            [:math:`s`] Spacing of the shear reinforcement [:math:`mm`].
        alpha_cw : DIMENSIONLESS
            [:math:`\alpha_{cw}`] Coefficient taking account of the state of stress in the compression chord [-].
        nu_1 : DIMENSIONLESS
            [:math:`\nu_{1}`] Strength reduction factor for concrete [-].
        f_cd : MPA
            [:math:`f_{cd}`] Design value of concrete compressive strength [:math:`MPa`].
        """
        super().__init__()
        self.a_sw_max = a_sw_max
        self.f_ywd = f_ywd
        self.b_w = b_w
        self.s = s
        self.alpha_cw = alpha_cw
        self.nu_1 = nu_1
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        a_sw_max: MM2,
        f_ywd: MPA,
        b_w: MM,
        s: MM,
        alpha_cw: DIMENSIONLESS,
        nu_1: DIMENSIONLESS,
        f_cd: MPA,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(
            b_w=b_w,
            s=s,
        )
        raise_if_negative(a_sw_max=a_sw_max, f_ywd=f_ywd, alpha_cw=alpha_cw, nu_1=nu_1, f_cd=f_cd)

        return (a_sw_max * f_ywd / (b_w * s)) <= (0.5 * alpha_cw * nu_1 * f_cd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.12."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\frac{A_{sw,max} \cdot f_{ywd}}{b_{w} \cdot s} \leq \frac{1}{2} \cdot \alpha_{cw} \cdot \nu_{1} \cdot f_{cd}",
            numeric_equation=rf"\frac{{{self.a_sw_max:.3f} \cdot {self.f_ywd:.3f}}}{{{self.b_w:.3f} \cdot {self.s:.3f}}}"
            rf" \leq \frac{{1}}{{2}} \cdot {self.alpha_cw:.3f} \cdot {self.nu_1:.3f} \cdot {self.f_cd:.3f}",
            comparison_operator_label="\\to",
            unit="",
        )
