"""Formula 6.50 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot50PunchingStressResistance(Formula):
    r"""Class representing formula 6.50 for the calculation of punching stress resistance [$v_{Rd}$] of slabs and
    column bases without shear reinforcement.
    """

    label = "6.50"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c_rd_c: DIMENSIONLESS,
        k: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        d: MM,
        a: MM,
        v_min: MPA,
    ) -> None:
        r"""[$v_{Rd}$] Calculation of punching stress resistance of slabs and column bases without shear reinforcement.

        NEN-EN 1992-1-1+C2:2011 art.6.4.4(2) - Formula (6.50)

        The values of $C_{Rd,c}$, $v_{min}$, and $k$ for use in a country may be found in its national annex.
        The recommended value for $C_{Rd,c}$ is $0.18 / \gamma_c$, for $v_{min}$ is given by Expression (6.3N),
        and that for $k$ is $1.0$.

        Parameters
        ----------
        c_rd_c : DIMENSIONLESS
            $C_{Rd,c}$ Coefficient for punching shear resistance, recommended value $0.18 / \gamma_c$ [-].
        k : DIMENSIONLESS
            $k$ Size effect factor, see equation SubForm6Dot47FactorK [-].
        rho_l : DIMENSIONLESS
            $\rho_l$ Longitudinal reinforcement ratio, see equation SubForm6Dot47FactorRhoL [-].
        f_ck : MPA
            $f_{ck}$ Characteristic compressive strength of concrete [$MPa$].
        d : MM
            $d$ Effective depth [$mm$].
        a : MM
            $a$ Distance from the periphery of the column to the control perimeter considered [$mm$].
        v_min : MPA
            $v_{min}$ Minimum shear stress capacity concrete, recommended value with Expression (6.3N) [$MPa$].
        """
        super().__init__()
        self.c_rd_c = c_rd_c
        self.k = k
        self.rho_l = rho_l
        self.f_ck = f_ck
        self.d = d
        self.a = a
        self.v_min = v_min

    @staticmethod
    def _evaluate(
        c_rd_c: DIMENSIONLESS,
        k: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        d: MM,
        a: MM,
        v_min: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(c_rd_c=c_rd_c, k=k, rho_l=rho_l, f_ck=f_ck, d=d, v_min=v_min)
        raise_if_less_or_equal_to_zero(a=a)

        term1 = c_rd_c * k * (100 * rho_l * f_ck) ** (1 / 3) * 2 * d / a
        term2 = v_min * 2 * d / a

        return max(term1, term2)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.50."""
        _equation: str = (
            r"\max \left( C_{Rd,c} \cdot k \cdot \left( 100 \cdot \rho_l \cdot f_{ck} \right)^{\frac{1}{3}} "
            r"\cdot \frac{2 \cdot d}{a}, v_{min} \cdot \frac{2 \cdot d}{a} \right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"C_{Rd,c}": f"{self.c_rd_c:.3f}",
                r"\rho_l": f"{self.rho_l:.3f}",
                r"f_{ck}": f"{self.f_ck:.3f}",
                r" d": f" {self.d:.3f}",
                r"{a": "{" + f"{self.a:.3f}",
                r"v_{min}": f"{self.v_min:.3f}",
                r"k": f"{self.k:.3f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"C_{Rd,c}": rf"{self.c_rd_c:.3f}",
                r"\rho_l": rf"{self.rho_l:.3f}",
                r"f_{ck}": rf"{self.f_ck:.3f} \ MPa",
                r" d": rf" {self.d:.3f} \ mm",
                r"{a": "{" + rf"{self.a:.3f} \ mm",
                r"v_{min}": rf"{self.v_min:.3f} \ MPa",
                r"k": rf"{self.k:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"v_{Rd}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
