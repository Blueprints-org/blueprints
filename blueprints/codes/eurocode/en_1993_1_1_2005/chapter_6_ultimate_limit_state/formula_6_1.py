"""Formula 6.1 from NEN-EN 1993-1-1:2005: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot1ElasticVerification(Formula):
    r"""Class representing formula 6.1 for the elastic verification with the yield criterion."""

    label = "6.1"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        sigma_x_ed: MPA,
        sigma_z_ed: MPA,
        tau_ed: MPA,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""Elastic verification with the yield criterion.

        NEN-EN 1993-1-1+C2:2016 art.6.2.1(5) - Formula (6.1)

        Parameters
        ----------
        sigma_x_ed : MPA
            [$\sigma_{x,\text{Ed}}$] Design value of the longitudinal stress at the point of consideration [$MPa$].
        sigma_z_ed : MPA
            [$\sigma_{z,\text{Ed}}$] Design value of the transverse stress at the point of consideration [$MPa$].
        tau_ed : MPA
            [$\tau_{\text{Ed}}$] Design value of the shear stress at the point of consideration [$MPa$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for the material [dimensionless].
        """
        super().__init__()
        self.sigma_x_ed = sigma_x_ed
        self.sigma_z_ed = sigma_z_ed
        self.tau_ed = tau_ed
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @staticmethod
    def _evaluate(
        sigma_x_ed: MPA,
        sigma_z_ed: MPA,
        tau_ed: MPA,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sigma_x_ed=sigma_x_ed, sigma_z_ed=sigma_z_ed, tau_ed=tau_ed)
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0, f_y=f_y)

        term1 = (sigma_x_ed / (f_y / gamma_m0)) ** 2
        term2 = (sigma_z_ed / (f_y / gamma_m0)) ** 2
        term3 = (sigma_x_ed / (f_y / gamma_m0)) * (sigma_z_ed / (f_y / gamma_m0))
        term4 = 3 * (tau_ed / (f_y / gamma_m0)) ** 2

        return term1 + term2 - term3 + term4 <= 1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.1."""
        _equation: str = (
            r"\left( \frac{\sigma_{x,\text{Ed}}}{f_y / \gamma_{M0}} \right)^2 "
            r"+ \left( \frac{\sigma_{z,\text{Ed}}}{f_y / \gamma_{M0}} \right)^2 "
            r"- \left( \frac{\sigma_{x,\text{Ed}}}{f_y / \gamma_{M0}} \right) "
            r"\left( \frac{\sigma_{z,\text{Ed}}}{f_y / \gamma_{M0}} \right) "
            r"+ 3 \left( \frac{\tau_{\text{Ed}}}{f_y / \gamma_{M0}} \right)^2 \leq 1"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\sigma_{x,\text{Ed}}": f"{self.sigma_x_ed:.{n}f}",
                r"\sigma_{z,\text{Ed}}": f"{self.sigma_z_ed:.{n}f}",
                r"\tau_{\text{Ed}}": f"{self.tau_ed:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
