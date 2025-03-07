"""Formula 6.14 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.math_helpers import cot
from blueprints.type_alias import DEG, DIMENSIONLESS, MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot14MaxShearResistanceInclinedReinforcement(Formula):
    r"""Class representing formula 6.14 for the calculation of the maximum shear resistance for members with inclined
    shear reinforcement, [$V_{Rd,max}$].
    """

    label = "6.14"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_cw: DIMENSIONLESS,
        b_w: MM,
        z: MM,
        nu_1: DIMENSIONLESS,
        f_cd: MPA,
        theta: DEG,
        alpha: DEG,
    ) -> None:
        r"""[$V_{Rd,max}$] Maximum shear resistance for members with inclined shear reinforcement [$N$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(4) - Formula (6.14)

        Parameters
        ----------
        alpha_cw : DIMENSIONLESS
            [$\alpha_{cw}$] Coefficient taking account of the state of the stress in the compression chord [$-$].
        b_w : MM
            [$b_{w}$] Width of the web [$mm$].
        z : MM
            [$z$] Lever arm [$mm$].
        nu_1 : DIMENSIONLESS
            [$\nu_{1}$] Strength reduction factor for concrete [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of concrete compressive strength [$MPa$].
        theta : DEG
            [$\theta$] Angle between the concrete compression strut and the beam axis perpendicular to the
            shear force [$degrees$].
        alpha : DEG
            [$\alpha$] Angle between shear reinforcement and the beam axis perpendicular to the shear force [$degrees$].
        """
        super().__init__()
        self.alpha_cw = alpha_cw
        self.b_w = b_w
        self.z = z
        self.nu_1 = nu_1
        self.f_cd = f_cd
        self.theta = theta
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        alpha_cw: DIMENSIONLESS,
        b_w: MM,
        z: MM,
        nu_1: DIMENSIONLESS,
        f_cd: MPA,
        theta: DEG,
        alpha: DEG,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            alpha_cw=alpha_cw,
            b_w=b_w,
            z=z,
            nu_1=nu_1,
            f_cd=f_cd,
            theta=theta,
            alpha=alpha,
        )
        denominator = 1 + cot(theta) ** 2
        raise_if_less_or_equal_to_zero(denominator=denominator)

        return alpha_cw * b_w * z * nu_1 * f_cd * (cot(theta) + cot(alpha)) / (1 + cot(theta) ** 2)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.14."""
        return LatexFormula(
            return_symbol=r"V_{Rd,max}",
            result=f"{self:.3f}",
            equation=r"\alpha_{cw} \cdot b_{w} \cdot z \cdot \nu_{1} \cdot f_{cd} \cdot \frac{\cot(\theta) + \cot(\alpha)}{1 + \cot^2(\theta)}",
            numeric_equation=rf"{self.alpha_cw:.3f} \cdot {self.b_w:.3f} \cdot {self.z:.3f} \cdot {self.nu_1:.3f} \cdot {self.f_cd:.3f} \cdot "
            rf"\frac{{\cot({self.theta:.3f}) + \cot({self.alpha:.3f})}}{{1 + \cot^2({self.theta:.3f})}}",
            comparison_operator_label="=",
            unit="N",
        )
