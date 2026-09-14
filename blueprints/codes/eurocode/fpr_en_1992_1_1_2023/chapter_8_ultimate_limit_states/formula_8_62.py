"""Formula 8.62 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, MPA
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot62EnhancedShearStressResistanceInclinedShearReinforcement(Formula):
    """Class representing formula 8.62 for the calculation of the enhanced shear stress resistance where a
    concentrated load is applied close to a support, in members with inclined shear reinforcement.

    This replaces Formula (8.55) for such members.
    """

    label = "8.62"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        nu: DIMENSIONLESS,
        f_cd: MPA,
        theta: DEG,
        beta_incl: DEG,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
        alpha_w: DEG,
    ) -> None:
        r"""[$\tau_{Rd}$] Enhanced shear stress resistance for concentrated loads applied close to a support, in
        members with inclined shear reinforcement [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.3 (13) - Formula (8.62)

        The standard offers this enhancement in cases where concentrated loads are applied at a distance
        [$a_v = z \cdot \cot\beta_{incl}$] less than [$z \cdot \cot\theta$] from a support. That is a condition
        of application, not a bound on the result, so it is not enforced here.

        Parameters
        ----------
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor for concrete cracked in shear. A value of 0,5 may be adopted when
            using the angles of the compression field given in 8.2.3(4), see 8.2.3(6) [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        theta : DEG
            [$\theta$] Inclination of the compression field in the web, selected within the range of Formula
            (8.58), see Form8Dot58CheckCotangentInclinedShearReinforcement [$degrees$].
        beta_incl : DEG
            [$\beta_{incl}$] Angle that follows from the distance of the concentrated load to the support
            through [$a_v = z \cdot \cot\beta_{incl}$], so [$\beta_{incl} = \arctan(z/a_v)$] [$degrees$].
        rho_w : DIMENSIONLESS
            [$\rho_w$] Shear reinforcement ratio according to Formula (8.43) [$-$].
        f_ywd : MPA
            [$f_{ywd}$] Design value of the yield strength of the shear reinforcement. For compression field
            inclinations with [$\cot\theta < \tan(\alpha_w/2)$] the standard requires it to be replaced by the
            stress [$\sigma_{swd}$] according to Formula (8.63), see Form8Dot63StressInInclinedShearReinforcement.
            That stress carries no printed lower bound and is negative over much of its range, so this argument
            is not guarded against negative values [$MPa$].
        alpha_w : DEG
            [$\alpha_w$] Inclination of the shear reinforcement, measured positive as shown in Figure 8.11 b).
            The standard gives this clause for [$45 \leq \alpha_w < 90$] degrees, which is a condition of
            application and is not enforced. Angles above 90 degrees are rejected, since the standard says
            they should be avoided [$degrees$].
        """
        super().__init__()
        self.nu = nu
        self.f_cd = f_cd
        self.theta = theta
        self.beta_incl = beta_incl
        self.rho_w = rho_w
        self.f_ywd = f_ywd
        self.alpha_w = alpha_w

    @staticmethod
    def _evaluate(
        nu: DIMENSIONLESS,
        f_cd: MPA,
        theta: DEG,
        beta_incl: DEG,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
        alpha_w: DEG,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(nu=nu, f_cd=f_cd, rho_w=rho_w)
        raise_if_less_or_equal_to_zero(theta=theta, beta_incl=beta_incl, alpha_w=alpha_w)

        cot_theta, cot_beta_incl, cot_alpha_w = cot(theta), cot(beta_incl), cot(alpha_w)

        # The denominator 1 + cot^2(theta) is never zero, so it needs no guard of its own.
        enhanced = nu * f_cd * (cot_theta - cot_beta_incl) / (1 + cot_theta**2) + rho_w * f_ywd * (cot_beta_incl + cot_alpha_w) * np.sin(
            np.deg2rad(alpha_w)
        )
        limit = nu * f_cd * (cot_theta + cot_alpha_w) / (1 + cot_theta**2)
        return min(enhanced, limit)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.62."""
        _equation: str = (
            r"\min\left(\nu \cdot f_{cd} \cdot \frac{\cot(\theta) - \cot(\beta_{incl})}"
            r"{1 + \left(\cot(\theta)\right)^2} + \rho_w \cdot f_{ywd} \cdot "
            r"\left(\cot(\beta_{incl}) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w), "
            r"\nu \cdot f_{cd} \cdot \frac{\cot(\theta) + \cot(\alpha_w)}{1 + \left(\cot(\theta)\right)^2}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
                r"\beta_{incl}": f"{self.beta_incl:.{n}f}",
                r"\theta": f"{self.theta:.{n}f}",
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
                r"\alpha_w": f"{self.alpha_w:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
                r"\beta_{incl}": rf"{self.beta_incl:.{n}f} ^\circ",
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": rf"{self.f_ywd:.{n}f} \ MPa",
                r"\alpha_w": rf"{self.alpha_w:.{n}f} ^\circ",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
