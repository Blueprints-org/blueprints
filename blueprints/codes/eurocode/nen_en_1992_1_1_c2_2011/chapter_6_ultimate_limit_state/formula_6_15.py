"""Formula 6.15 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG, DIMENSIONLESS, MM, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot15ShearReinforcementResistance(Formula):
    r"""Class representing formula 6.15 for checking the shear reinforcement resistance."""

    label = "6.15"
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
        alpha: DEG,
    ) -> None:
        r"""Check the shear reinforcement resistance.

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(4) - Formula (6.15)

        Parameters
        ----------
        a_sw_max : MM2
            [$A_{sw,max}$] The cross-sectional area of the shear reinforcement [$mm^2$].
        f_ywd : MPA
            [$f_{ywd}$] Design yield strength of the shear reinforcement [$MPa$].
        b_w : MM
            [$b_{w}$] Width of the web [$mm$].
        s : MM
            [$s$] Spacing of the stirrups [$mm$].
        alpha_cw : DIMENSIONLESS
            [$\alpha_{cw}$] Coefficient taking account of the state of stress in the compression chord [$-$].
        nu_1 : DIMENSIONLESS
            [$\nu_{1}$] Strength reduction factor for concrete cracked in shear [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of concrete compressive strength [$MPa$].
        alpha : DEG
            [$\alpha$] Angle between shear reinforcement and the beam axis perpendicular to the shear force [$degrees$].
        """
        super().__init__()
        self.a_sw_max = a_sw_max
        self.f_ywd = f_ywd
        self.b_w = b_w
        self.s = s
        self.alpha_cw = alpha_cw
        self.nu_1 = nu_1
        self.f_cd = f_cd
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        a_sw_max: MM2,
        f_ywd: MPA,
        b_w: MM,
        s: MM,
        alpha_cw: DIMENSIONLESS,
        nu_1: DIMENSIONLESS,
        f_cd: MPA,
        alpha: DEG,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(b_w=b_w, s=s, alpha=alpha)
        raise_if_negative(a_sw_max=a_sw_max, f_ywd=f_ywd, alpha_cw=alpha_cw, nu_1=nu_1, f_cd=f_cd)

        left_side = (a_sw_max * f_ywd) / (b_w * s)
        right_side = (0.5 * alpha_cw * nu_1 * f_cd) / np.sin(np.deg2rad(alpha))

        return left_side <= right_side

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.15."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\frac{A_{sw,max} \cdot f_{ywd}}{b_{w} \cdot s} \leq \frac{\frac{1}{2} \cdot \alpha_{cw} "
            r"\cdot \nu_{1} \cdot f_{cd}}{\sin(\alpha)}",
            numeric_equation=rf"\frac{{{self.a_sw_max:.3f} \cdot {self.f_ywd:.3f}}}{{{self.b_w:.3f} \cdot "
            rf"{self.s:.3f}}} \leq \frac{{\frac{{1}}{{2}} \cdot {self.alpha_cw:.3f} \cdot {self.nu_1:.3f} "
            rf"\cdot {self.f_cd:.3f}}}{{\sin({self.alpha:.3f})}}",
            comparison_operator_label="\\to",
            unit="",
        )
