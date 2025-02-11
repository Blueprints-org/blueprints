"""Formula 7.9 from NEN-EN 1992-1-1+C2:2011: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form7Dot9EpsilonSmMinusEpsilonCm(Formula):
    r"""Class representing formula 7.9 for the calculation of [$$\epsilon_{sm} - \epsilon_{cm}$$]."""

    label = "7.9"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        sigma_s: MPA,
        k_t: DIMENSIONLESS,
        f_ct_eff: MPA,
        rho_p_eff: DIMENSIONLESS,
        e_s: MPA,
        e_c: MPA,
    ) -> None:
        r"""[$$\epsilon_{sm} - \epsilon_{cm}$$] Calculation of the strain difference [$$\epsilon$$].

        NEN-EN 1992-1-1+C2:2011 art.7.3.4(2) - Formula (7.9)

        Parameters
        ----------
        sigma_s : MPA
            [$$\sigma_s$$] Stress in the reinforcement [$$MPa$$].
        k_t : DIMENSIONLESS
            [$$k_t$$] Factor dependent on the duration of the load, 0.6 for short term loading, 0.4 for long term loading [$$-$$].
        f_ct_eff : MPA
            [$$f_{ct,eff}$$] Effective tensile strength of concrete [$$MPa$$].
        rho_p_eff : DIMENSIONLESS
            [$$\rho_{p,eff}$$] Effective reinforcement ratio, see equation 7.10 [$$-$$].
        e_s : MPA
            [$$e_s$$] Modulus of elasticity of reinforcement [$$MPa$$].
        e_c : MPA
            [$$e_c$$] Modulus of elasticity of concrete [$$MPa$$].
        """
        super().__init__()
        self.sigma_s = sigma_s
        self.k_t = k_t
        self.f_ct_eff = f_ct_eff
        self.rho_p_eff = rho_p_eff
        self.e_s = e_s
        self.e_c = e_c
        self.alpha_e = e_s / e_c

    @staticmethod
    def _evaluate(
        sigma_s: MPA,
        k_t: DIMENSIONLESS,
        f_ct_eff: MPA,
        rho_p_eff: DIMENSIONLESS,
        e_s: MPA,
        e_c: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sigma_s=sigma_s, k_t=k_t, f_ct_eff=f_ct_eff, rho_p_eff=rho_p_eff, e_s=e_s, e_c=e_c)

        alpha_e = e_s / e_c
        return max((sigma_s - k_t * (f_ct_eff / rho_p_eff) * (1 + alpha_e * rho_p_eff)) / e_s, 0.6 * sigma_s / e_s)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 7.9."""
        _equation: str = (
            r"\max\left("
            r"\frac{\sigma_s - k_t \cdot \frac{f_{ct,eff}}{\rho_{p,eff}} \cdot \left(1 + \frac{E_s}{E_c} \cdot \rho_{p,eff}\right)}{E_s}; "
            r"\frac{0.6 \cdot \sigma_s}{E_s}"
            r"\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\sigma_s": f"{self.sigma_s:.3f}",
                r"k_t": f"{self.k_t:.3f}",
                r"f_{ct,eff}": f"{self.f_ct_eff:.3f}",
                r"\rho_{p,eff}": f"{self.rho_p_eff:.3f}",
                r"E_s": f"{self.e_s:.3f}",
                r"E_c": f"{self.e_c:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\epsilon_{sm} - \epsilon_{cm}",
            result=f"{self:.6f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="",
        )
