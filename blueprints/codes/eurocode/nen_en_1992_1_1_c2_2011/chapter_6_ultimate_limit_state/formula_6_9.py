"""Formula 6.9 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.math_helpers import cot
from blueprints.type_alias import DEG, DIMENSIONLESS, MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot9MaximumShearResistance(Formula):
    r"""Class representing formula 6.9 for the calculation of the maximum shear resistance, $V_{Rd,max}$."""

    label = "6.9"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        b_w: MM,
        z: MM,
        f_cd: MPA,
        nu_1: DIMENSIONLESS,
        alpha_cw: DIMENSIONLESS,
        theta: DEG,
    ) -> None:
        r"""[$V_{Rd,max}$] Maximum shear resistance [$N$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(3) - Formula (6.9)

        Parameters
        ----------
        b_w : MM
            [$b_{w}$] Width of the web of the beam [$mm$].
        z : MM
            [$z$] Lever arm [$mm$].
        f_cd : MPA
            [$f_{cd}$] Design value of concrete compressive strength [$MPa$].
        nu_1 : DIMENSIONLESS
            [$\nu_{1}$] Strength reduction factor for concrete cracked in shear [-].
        alpha_cw : DIMENSIONLESS
            [$\alpha_{cw}$] Coefficient taking account of the state of the stress in the compression chord [-].
        theta : DEG
            [$\theta$] Angle between the concrete compression strut and the beam axis perpendicular to the shear force [$degrees$].
        """
        super().__init__()
        self.b_w = b_w
        self.z = z
        self.f_cd = f_cd
        self.nu_1 = nu_1
        self.alpha_cw = alpha_cw
        self.theta = theta

    @staticmethod
    def _evaluate(
        b_w: MM,
        z: MM,
        f_cd: MPA,
        nu_1: DIMENSIONLESS,
        alpha_cw: DIMENSIONLESS,
        theta: DEG,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            b_w=b_w,
            z=z,
            f_cd=f_cd,
            nu_1=nu_1,
            alpha_cw=alpha_cw,
        )
        raise_if_less_or_equal_to_zero(theta=theta)

        return alpha_cw * b_w * z * nu_1 * f_cd / (cot(theta) + np.tan(np.deg2rad(theta)))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.9."""
        return LatexFormula(
            return_symbol=r"V_{Rd,max}",
            result=f"{self:.3f}",
            equation=r"\alpha_{cw} \cdot b_{w} \cdot z \cdot \nu_{1} \cdot \frac{f_{cd}}{\cot(\theta) + \tan(\theta)}",
            numeric_equation=rf"{self.alpha_cw:.3f} \cdot {self.b_w:.3f} \cdot {self.z:.3f} \cdot {self.nu_1:.3f} \cdot"
            rf" \frac{{{self.f_cd:.3f}}}{{\cot({self.theta:.3f}) + \tan({self.theta:.3f})}}",
            comparison_operator_label="=",
            unit="N",
        )
