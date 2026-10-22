"""Formula 8.76 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative

ALPHA_MIN: DEG = 35.0
ALPHA_MAX: DEG = 135.0


class Form8Dot76ShearStressResistanceAtInterface(Formula):
    r"""Class representing formula 8.76 for the calculation of the design shear stress resistance at an interface.

    It applies to situations without reinforcement across the interface, or where the required reinforcement
    across the interface is anchored for [$\sigma_{sd} = f_{yd}$]. In other cases Formula (8.77) applies
    according to 8.2.6(7).

    The printed line carries an upper bound, so the result is the smaller of the expression and that bound.
    The two rules the standard states in prose for [$\sigma_n$] are applied as well: a compressive stress is
    not taken larger than [$0.60 \cdot f_{cd}$], and for a tensile stress the term [$\mu_v \cdot \sigma_n$] is
    taken as zero.

    Note that the cap on [$\sigma_n$] can never govern the result as long as [$\mu_v$] comes from Table 8.2,
    where the smallest value is 0,5: with [$\sigma_n$] at its cap the term [$\mu_v \cdot \sigma_n$] is at
    least [$0.30 \cdot f_{cd}$], which already exhausts the first part of the upper bound, so the upper bound
    governs instead. The cap is implemented because the standard states it, not because it changes an answer.

    Two things this class deliberately does not do. It does not apply footnote a of Table 8.2, which sets
    [$c_{v1} = 0$] when the interface carries tensile stresses caused by an external axial force in
    perpendicular direction; that footnote belongs to the table, depends on the roughness class, and is
    applied by passing ``tension_perpendicular_to_interface`` to Table8Dot2CoefficientsSurfaceRoughness. And
    it puts no lower bound of zero on the result, because the standard prints none, even though the
    expression can turn negative for [$c_{v1} = 0$] combined with an angle beyond 90 degrees.

    The printed line is not dimensionally homogeneous: [$\sqrt{f_{ck}}$] carries [$MPa^{0.5}$] while the
    result is in [$MPa$], so [$c_{v1}$] absorbs the remaining [$MPa^{0.5}$]. Table 8.2 prints it as a bare
    number, so it is typed dimensionless here, and the representation with units shows the square root of a
    stress rather than a stress.
    """

    label = "8.76"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        c_v1: DIMENSIONLESS,
        f_ck: MPA,
        gamma_c: DIMENSIONLESS,
        mu_v: DIMENSIONLESS,
        sigma_n: MPA,
        rho_i: DIMENSIONLESS,
        f_yd: MPA,
        alpha: DEG,
        f_cd: MPA,
    ) -> None:
        r"""[$\tau_{Rdi}$] Design shear stress resistance at the interface [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.2.6(5) - Formula (8.76)

        Parameters
        ----------
        c_v1 : DIMENSIONLESS
            [$c_{v1}$] Factor which depends on the roughness of the interface, see Table 8.2 and art.
            8.2.6(6). The formula assumes the contact surface to be clean and free of laitance, dust or other
            adhesion-reducing particles [$-$].
        f_ck : MPA
            [$f_{ck}$] Lowest compressive strength of the concretes at the interface [$MPa$].
        gamma_c : DIMENSIONLESS
            [$\gamma_C$] Partial factor for concrete [$-$].
        mu_v : DIMENSIONLESS
            [$\mu_v$] Factor which depends on the roughness of the interface, see Table 8.2 and art.
            8.2.6(6) [$-$].
        sigma_n : MPA
            [$\sigma_n$] Compressive stress over the interface area [$A_i$] caused by the minimum external
            axial force across the interface that acts simultaneously with the shear force. Permanent stresses
            caused by confinement of surrounding structural parts may be taken into account. Compression is
            positive here: a positive value is capped at [$0.60 \cdot f_{cd}$] as the standard requires, and a
            negative value is a tensile stress, for which the standard takes the term
            [$\mu_v \cdot \sigma_n$] as 0 [$MPa$].
        rho_i : DIMENSIONLESS
            [$\rho_i$] Ratio [$A_{si} / A_i$], where [$A_{si}$] is the cross-sectional area of bonded
            reinforcement crossing the interface and anchored for [$\sigma_{sd} = f_{yd}$], including ordinary
            shear reinforcement if any, with adequate anchorage according to 11.4 at both sides of the
            interface. Tensile forces across interfaces shall be carried by reinforcement placed additional to
            the interface reinforcement [$A_{si}$] [$-$].
        f_yd : MPA
            [$f_{yd}$] Design value of the yield strength of the reinforcement crossing the interface [$MPa$].
        alpha : DEG
            [$\alpha$] Angle of the reinforcement crossing the interface as defined in Figure 8.15b), limited
            to [$35° \leq \alpha \leq 135°$]. For very smooth surfaces the standard limits it further to
            [$35° \leq \alpha \leq 90°$]; that tighter bound is not enforced here, because the roughness of
            the interface is not an input to this formula [$degrees$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.c_v1 = c_v1
        self.f_ck = f_ck
        self.gamma_c = gamma_c
        self.mu_v = mu_v
        self.sigma_n = sigma_n
        self.rho_i = rho_i
        self.f_yd = f_yd
        self.alpha = alpha
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        c_v1: DIMENSIONLESS,
        f_ck: MPA,
        gamma_c: DIMENSIONLESS,
        mu_v: DIMENSIONLESS,
        sigma_n: MPA,
        rho_i: DIMENSIONLESS,
        f_yd: MPA,
        alpha: DEG,
        f_cd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        # sigma_n is deliberately not guarded: a negative value is the tensile stress that the standard
        # explicitly allows for and neutralises below.
        raise_if_negative(c_v1=c_v1, f_ck=f_ck, mu_v=mu_v, rho_i=rho_i, f_yd=f_yd, f_cd=f_cd)
        raise_if_less_or_equal_to_zero(gamma_c=gamma_c)
        if not ALPHA_MIN <= alpha <= ALPHA_MAX:
            raise ValueError(f"Invalid angle alpha: {alpha}. The standard limits it to {ALPHA_MIN} <= alpha <= {ALPHA_MAX} degrees.")

        alpha_rad = np.deg2rad(alpha)
        sigma_n_effective = min(max(sigma_n, 0), 0.60 * f_cd)
        resistance = c_v1 * np.sqrt(f_ck) / gamma_c + mu_v * sigma_n_effective + rho_i * f_yd * (mu_v * np.sin(alpha_rad) + np.cos(alpha_rad))
        upper_bound = 0.30 * f_cd + rho_i * f_yd * np.cos(alpha_rad)

        return min(resistance, upper_bound)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.76."""
        _equation: str = (
            r"\min\left(c_{v1} \cdot \frac{\sqrt{f_{ck}}}{\gamma_C} + \mu_v \cdot "
            r"\min\left(\max\left(\sigma_n, 0\right), 0.60 \cdot f_{cd}\right) + "
            r"\rho_i \cdot f_{yd} \cdot \left(\mu_v \cdot \sin\alpha + \cos\alpha\right), "
            r"0.30 \cdot f_{cd} + \rho_i \cdot f_{yd} \cdot \cos\alpha\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"c_{v1}": f"{self.c_v1:.{n}f}",
                r"f_{ck}": f"{self.f_ck:.{n}f}",
                r"\gamma_C": f"{self.gamma_c:.{n}f}",
                r"\mu_v": f"{self.mu_v:.{n}f}",
                r"\sigma_n": f"{self.sigma_n:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
                r"\rho_i": f"{self.rho_i:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
                r"\alpha": f"{self.alpha:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                # The factors, the partial factor and the reinforcement ratio are dimensionless.
                r"c_{v1}": f"{self.c_v1:.{n}f}",
                r"f_{ck}": rf"{self.f_ck:.{n}f} \ MPa",
                r"\gamma_C": f"{self.gamma_c:.{n}f}",
                r"\mu_v": f"{self.mu_v:.{n}f}",
                r"\sigma_n": rf"{self.sigma_n:.{n}f} \ MPa",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
                r"\rho_i": f"{self.rho_i:.{n}f}",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
                r"\alpha": rf"{self.alpha:.{n}f} \ deg",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rdi}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
