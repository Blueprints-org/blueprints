"""Formula 7.9 from EN 1992-1-1:2004: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form7Dot9EpsilonSmMinusEpsilonCm(Formula):
    r"""Class representing formula 7.9 for the calculation of [$\epsilon_{sm} - \epsilon_{cm}$]."""

    label = "7.9"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        sigma_s: MPA,
        k_t: DIMENSIONLESS,
        f_ct_eff: MPA,
        rho_p_eff: DIMENSIONLESS,
        e_s: MPA,
        e_cm: MPA,
    ) -> None:
        r"""[$\epsilon_{sm} - \epsilon_{cm}$] Calculation of the strain difference [$\epsilon$].

        EN 1992-1-1:2004 art.7.3.4(2) - Formula (7.9)

        Parameters
        ----------
        sigma_s : MPA
            [$\sigma_s$] Stress in the reinforcement [$MPa$].
        k_t : DIMENSIONLESS
            [$k_t$] Factor dependent on the duration of the load, 0.6 for short term loading, 0.4 for long term loading [$-$].
        f_ct_eff : MPA
            [$f_{ct,eff}$] Effective tensile strength of concrete [$MPa$].
        rho_p_eff : DIMENSIONLESS
            [$\rho_{p,eff}$] Effective reinforcement ratio, see equation 7.10 [$-$].
        e_s : MPA
            [$e_s$] Modulus of elasticity of reinforcement [$MPa$].
        e_cm : MPA
            [$e_{cm}$] Modulus of elasticity of concrete [$MPa$].
        """
        super().__init__()
        self.sigma_s = sigma_s
        self.k_t = k_t
        self.f_ct_eff = f_ct_eff
        self.rho_p_eff = rho_p_eff
        self.e_s = e_s
        self.e_cm = e_cm
        self.alpha_e = e_s / e_cm

    @staticmethod
    def _evaluate(
        sigma_s: MPA,
        k_t: DIMENSIONLESS,
        f_ct_eff: MPA,
        rho_p_eff: DIMENSIONLESS,
        e_s: MPA,
        e_cm: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sigma_s=sigma_s, k_t=k_t, f_ct_eff=f_ct_eff, rho_p_eff=rho_p_eff, e_s=e_s, e_cm=e_cm)

        alpha_e = e_s / e_cm
        numerator = sigma_s - k_t * (f_ct_eff / rho_p_eff) * (1 + alpha_e * rho_p_eff)
        return max(numerator / e_s, 0.6 * sigma_s / e_s)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.9."""
        _equation: str = (
            r"\max\left("
            r"\frac{\sigma_s - k_t \cdot \frac{f_{ct,eff}}{\rho_{p,eff}} \cdot \left(1 + \frac{E_s}{E_{cm}} \cdot \rho_{p,eff}\right)}{E_s}; "
            r"\frac{0.6 \cdot \sigma_s}{E_s}"
            r"\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\sigma_s": f"{self.sigma_s:.{n}f}",
                r"k_t": f"{self.k_t:.{n}f}",
                r"f_{ct,eff}": f"{self.f_ct_eff:.{n}f}",
                r"\rho_{p,eff}": f"{self.rho_p_eff:.{n}f}",
                r"E_s": f"{self.e_s:.{n}f}",
                r"E_{cm}": f"{self.e_cm:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\epsilon_{sm} - \epsilon_{cm}",
            result=f"{self:.6f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
