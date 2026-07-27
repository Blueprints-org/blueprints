"""Formula 8.27 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot27DesignShearStressResistance(Formula):
    """Class representing formula 8.27 for the calculation of the design value of the shear stress resistance
    of members without shear reinforcement.
    """

    label = "8.27"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        gamma_v: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        d_dg: MM,
        d: MM,
        tau_rdc_min: MPA,
    ) -> None:
        r"""[$\tau_{Rd,c}$] Design value of the shear stress resistance of members without shear reinforcement [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (2) - Formula (8.27)

        The standard writes this as an expression bounded from below by [$\tau_{Rdc,min}$], which is implemented
        as the maximum of the two.

        Parameters
        ----------
        gamma_v : DIMENSIONLESS
            [$\gamma_V$] Partial factor for shear design according to Table 4.3 (NDP) or Tables A.1 (NDP)
            and A.2 (NDP) [$-$].
        rho_l : DIMENSIONLESS
            [$\rho_l$] Longitudinal tensile reinforcement ratio according to Formula (8.28), see
            Form8Dot28LongitudinalReinforcementRatio [$-$].
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        d_dg : MM
            [$d_{dg}$] Size parameter describing the failure zone roughness, which depends on the concrete type
            and its aggregate properties. The standard gives it as [$16 + D_{lower} \leq 40$] for concrete with
            [$f_{ck} \leq 60$] MPa, and as [$16 + D_{lower} \cdot \left(60/f_{ck}\right)^2 \leq 40$] for concrete
            with [$f_{ck} > 60$] MPa, both in millimetres. [$D_{lower}$] is the smallest value of the upper sieve
            size [$D$] in an aggregate for the coarsest fraction of aggregates in the concrete permitted by the
            specification of concrete according to EN 206; where [$D_{max}$] is known it may replace
            [$D_{lower}$], see the NOTE 2 to 8.2.1(4) [$mm$].
        d : MM
            [$d$] Effective depth [$d_{nom}$]. The value [$d$] may be refined according to 8.2.2(3) and 8.2.2(4) for
            non-slender members and members with axial force, by replacing it with the mechanical shear span
            [$a_v$] or by multiplying it with [$k_{vp}$]. That refinement is the responsibility of the caller,
            which passes the already adjusted value [$mm$].
        tau_rdc_min : MPA
            [$\tau_{Rdc,min}$] Minimum shear stress resistance according to Formula (8.20), see
            Form8Dot20MinimumShearStressResistance [$MPa$].
        """
        super().__init__()
        self.gamma_v = gamma_v
        self.rho_l = rho_l
        self.f_ck = f_ck
        self.d_dg = d_dg
        self.d = d
        self.tau_rdc_min = tau_rdc_min

    @staticmethod
    def _evaluate(
        gamma_v: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        d_dg: MM,
        d: MM,
        tau_rdc_min: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(rho_l=rho_l, f_ck=f_ck, d_dg=d_dg, tau_rdc_min=tau_rdc_min)
        raise_if_less_or_equal_to_zero(gamma_v=gamma_v, d=d)

        return max((0.66 / gamma_v) * (100 * rho_l * f_ck * (d_dg / d)) ** (1 / 3), tau_rdc_min)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.27."""
        _equation: str = (
            r"\max\left(\frac{0.66}{\gamma_V} \cdot \left(100 \cdot \rho_l \cdot f_{ck} \cdot "
            r"\frac{d_{dg}}{d}\right)^{\frac{1}{3}}, \tau_{Rdc,min}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\gamma_V": f"{self.gamma_v:.{n}f}",
                r"\rho_l": f"{self.rho_l:.{n}f}",
                r"f_{ck}": f"{self.f_ck:.{n}f}",
                r"d_{dg}": f"{self.d_dg:.{n}f}",
                r"{d}": "{" + f"{self.d:.{n}f}" + "}",
                r"\tau_{Rdc,min}": f"{self.tau_rdc_min:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\gamma_V": f"{self.gamma_v:.{n}f}",
                r"\rho_l": f"{self.rho_l:.{n}f}",
                r"f_{ck}": rf"{self.f_ck:.{n}f} \ MPa",
                r"d_{dg}": rf"{self.d_dg:.{n}f} \ mm",
                r"{d}": "{" + rf"{self.d:.{n}f} \ mm" + "}",
                r"\tau_{Rdc,min}": rf"{self.tau_rdc_min:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rd,c}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
