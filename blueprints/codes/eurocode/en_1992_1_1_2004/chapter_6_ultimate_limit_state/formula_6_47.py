"""Formula 6.47 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form6Dot47PunchingShearResistance(Formula):
    r"""Class representing formula 6.47 for the calculation of punching shear resistance, $v_{Rd,c}$ of slabs and column bases
    without shear reinforcement.
    """

    label = "6.47"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        c_rd_c: DIMENSIONLESS,
        k: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        k_1: DIMENSIONLESS,
        sigma_cp: MPA,
        v_min: MPA,
    ) -> None:
        r"""$v_{Rd,c}$ Calculation of punching shear resistance of slabs and column bases without shear reinforcement.

        EN 1992-1-1:2004 art.6.4.4(1) - Formula (6.47).

        The values of $C_{Rd,c}$, $v_{min}$, and $k_1$ for use in a country may be found in its national annex.
        The recommended value for $C_{Rd,c}$ is $0.18 / \gamma_c$, for $v_{min}$ is given by Expression (6.3N),
        and that for $k_1$ is $0.1$.

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
        k_1 : DIMENSIONLESS
            $k_1$ Coefficient for concrete strength, recommended value 0.1 [-].
        sigma_cp : MPA
            $\sigma_{cp}$ Stress in the critical section as average of the two perpendicular directions, see
             equation SubForm6Dot47FactorSigmaCp [$MPa$].
        v_min : MPA
            $v_{min}$ Minimum shear stress capacity concrete, recommended value with Expression (6.3N) [$MPa$].
        """
        super().__init__()
        self.c_rd_c = c_rd_c
        self.k = k
        self.rho_l = rho_l
        self.f_ck = f_ck
        self.k_1 = k_1
        self.sigma_cp = sigma_cp
        self.v_min = v_min

    @staticmethod
    def _evaluate(
        c_rd_c: DIMENSIONLESS,
        k: DIMENSIONLESS,
        rho_l: DIMENSIONLESS,
        f_ck: MPA,
        k_1: DIMENSIONLESS,
        sigma_cp: MPA,
        v_min: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(c_rd_c=c_rd_c, k=k, rho_l=rho_l, f_ck=f_ck, k_1=k_1, sigma_cp=sigma_cp, v_min=v_min)

        term1 = c_rd_c * k * (100 * rho_l * f_ck) ** (1 / 3) + k_1 * sigma_cp
        term2 = v_min + k_1 * sigma_cp
        return max(term1, term2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.47."""
        _equation: str = (
            r"\max \left( C_{Rd,c} \cdot k \cdot (100 \cdot \rho_l \cdot f_{ck})^{1/3} "
            r"+ k_1 \cdot \sigma_{cp}, v_{min} + k_1 \cdot \sigma_{cp} \right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"C_{Rd,c}": f"{self.c_rd_c:.{n}f}",
                r"\rho_l": f"{self.rho_l:.{n}f}",
                r"f_{ck}": f"{self.f_ck:.{n}f}",
                r"k_1": f"{self.k_1:.{n}f}",
                r"\sigma_{cp}": f"{self.sigma_cp:.{n}f}",
                r"v_{min}": f"{self.v_min:.{n}f}",
                r"k": f"{self.k:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"v_{Rd,c}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
