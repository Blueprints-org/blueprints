"""Formula 8.63 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, MPA
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot63StressInInclinedShearReinforcement(Formula):
    """Class representing formula 8.63 for the calculation of the stress in inclined shear reinforcement that
    replaces the yield strength for shallow compression field inclinations.

    This replaces Formula (8.56) for members with inclined shear reinforcement.
    """

    label = "8.63"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, e_s: MPA, epsilon_x: DIMENSIONLESS, theta: DEG, alpha_w: DEG, f_ywd: MPA) -> None:
        r"""[$\sigma_{swd}$] Stress in the inclined shear reinforcement [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.3 (13) - Formula (8.63)

        Compression field inclinations with [$\cot\theta < \tan(\alpha_w/2)$] are allowed if the yield strength
        [$f_{ywd}$] in Formula (8.62) is replaced by this stress. That is a condition of application, not a
        bound, so it is not enforced here. The standard prints no lower bound on the result either, so a
        combination that gives a negative stress returns that value unchanged.

        Parameters
        ----------
        e_s : MPA
            [$E_s$] Modulus of elasticity of the reinforcing steel [$MPa$].
        epsilon_x : DIMENSIONLESS
            [$\varepsilon_x$] Longitudinal strain, which may be calculated according to 8.2.3(7) for a
            cross-section located midway between the support and the load [$-$].
        theta : DEG
            [$\theta$] Inclination of the compression field in the web. This formula covers the case
            [$\cot\theta < \tan(\alpha_w/2)$], which lies outside the range of Formula (8.58) [$degrees$].
        alpha_w : DEG
            [$\alpha_w$] Inclination of the shear reinforcement, measured positive as shown in Figure 8.11 b).
            The standard gives this clause for [$45 \leq \alpha_w < 90$] degrees, which is a condition of
            application and is not enforced. Angles above 90 degrees are rejected, since the standard says
            they should be avoided [$degrees$].
        f_ywd : MPA
            [$f_{ywd}$] Design value of the yield strength of the shear reinforcement, which the stress may not
            exceed [$MPa$].
        """
        super().__init__()
        self.e_s = e_s
        self.epsilon_x = epsilon_x
        self.theta = theta
        self.alpha_w = alpha_w
        self.f_ywd = f_ywd

    @staticmethod
    def _evaluate(e_s: MPA, epsilon_x: DIMENSIONLESS, theta: DEG, alpha_w: DEG, f_ywd: MPA) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(e_s=e_s, epsilon_x=epsilon_x, f_ywd=f_ywd)
        raise_if_less_or_equal_to_zero(theta=theta, alpha_w=alpha_w)

        cot_alpha_w = cot(alpha_w)

        # The denominator 1 + cot^2(alpha_w) is never zero, so it needs no guard of its own.
        stress = e_s * ((epsilon_x + 0.001) * (cot(theta) + cot_alpha_w) ** 2 / (1 + cot_alpha_w**2) - 0.001)
        return min(stress, f_ywd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.63."""
        _equation: str = (
            r"\min\left(E_s \cdot \left[\left(\varepsilon_x + 0.001\right) \cdot "
            r"\frac{\left(\cot(\theta) + \cot(\alpha_w)\right)^2}{1 + \left(\cot(\alpha_w)\right)^2} "
            r"- 0.001\right], f_{ywd}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"E_s": f"{self.e_s:.{n}f}",
                r"\varepsilon_x": f"{self.epsilon_x:.{n}f}",
                r"\theta": f"{self.theta:.{n}f}",
                r"\alpha_w": f"{self.alpha_w:.{n}f}",
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"E_s": rf"{self.e_s:.{n}f} \ MPa",
                r"\varepsilon_x": f"{self.epsilon_x:.{n}f}",
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
                r"\alpha_w": rf"{self.alpha_w:.{n}f} ^\circ",
                r"f_{ywd}": rf"{self.f_ywd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{swd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
