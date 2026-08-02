"""Formula 8.55 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, MPA
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot55EnhancedShearStressResistance(Formula):
    """Class representing formula 8.55 for the calculation of the enhanced shear stress resistance where a
    concentrated load is applied close to a support.
    """

    label = "8.55"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        nu: DIMENSIONLESS,
        f_cd: MPA,
        theta: DEG,
        beta_incl: DEG,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
    ) -> None:
        r"""[$\tau_{Rd}$] Enhanced shear stress resistance for concentrated loads applied close to a support [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.3 (12) - Formula (8.55)

        The standard offers this enhancement in cases where concentrated loads are applied at a distance
        [$a_v = z \cdot \cot\beta_{incl}$] less than [$z \cdot \cot\theta$] from a support. That is a condition
        of application, not a bound on the result, so it is not enforced here.

        Parameters
        ----------
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor for concrete cracked in shear. A value of 0,5 may be adopted when
            using the angles of the compression field given in 8.2.3(4), see 8.2.3(6). A higher value may be
            adopted under the conditions of 8.2.3(7), calculated according to Formula (8.45) [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        theta : DEG
            [$\theta$] Inclination of the compression field in the web, selected within the range of Formula
            (8.41). A flatter field, [$\cot\theta < 1$], is allowed under 8.2.3(11), but only if [$f_{ywd}$] is
            replaced by [$\sigma_{swd}$] of Formula (8.56); making that substitution is left to the caller
            [$degrees$].
        beta_incl : DEG
            [$\beta_{incl}$] Angle that follows from the distance of the concentrated load to the support
            through [$a_v = z \cdot \cot\beta_{incl}$], so [$\beta_{incl} = \arctan(z/a_v)$] [$degrees$].
        rho_w : DIMENSIONLESS
            [$\rho_w$] Shear reinforcement ratio according to Formula (8.43) [$-$].
        f_ywd : MPA
            [$f_{ywd}$] Design value of the yield strength of the shear reinforcement [$MPa$].
        """
        super().__init__()
        self.nu = nu
        self.f_cd = f_cd
        self.theta = theta
        self.beta_incl = beta_incl
        self.rho_w = rho_w
        self.f_ywd = f_ywd

    @staticmethod
    def _evaluate(
        nu: DIMENSIONLESS,
        f_cd: MPA,
        theta: DEG,
        beta_incl: DEG,
        rho_w: DIMENSIONLESS,
        f_ywd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(nu=nu, f_cd=f_cd, rho_w=rho_w, f_ywd=f_ywd)
        raise_if_less_or_equal_to_zero(theta=theta, beta_incl=beta_incl)

        cot_theta, cot_beta_incl = cot(theta), cot(beta_incl)

        # The denominator 1 + cot^2(theta) is never zero, so it needs no guard of its own.
        enhanced = nu * f_cd * (cot_theta - cot_beta_incl) / (1 + cot_theta**2) + rho_w * f_ywd * cot_beta_incl
        limit = nu * f_cd * cot_theta / (1 + cot_theta**2)
        return min(enhanced, limit)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.55."""
        _equation: str = (
            r"\min\left(\nu \cdot f_{cd} \cdot \frac{\cot(\theta) - \cot(\beta_{incl})}"
            r"{1 + \left(\cot(\theta)\right)^2} + \rho_w \cdot f_{ywd} \cdot \cot(\beta_{incl}), "
            r"\nu \cdot f_{cd} \cdot \frac{\cot(\theta)}{1 + \left(\cot(\theta)\right)^2}\right)"
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
