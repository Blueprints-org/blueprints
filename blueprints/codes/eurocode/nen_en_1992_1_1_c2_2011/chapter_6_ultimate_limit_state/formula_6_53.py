"""Formula 6.53 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot53CheckPunchingShear(Formula):
    r"""Class representing formula 6.53 for the check of punching shear resistance.

    NEN-EN 1992-1-1+C2:2011 art.6.4.5(3) - Formula (6.53)

    Parameters
    ----------
    beta : DIMENSIONLESS
        [$\beta$] See 6.4.3 (3), (4) and (5) [$-$].
    v_ed : N
        [$V_{Ed}$] Design shear force [$N$].
    u_0 : MM
        [$u_{0}$] Perimeter of the critical section, differs for interior vs edge vs corner column [$mm$].
    d : MM
        [$d$] Mean effective depth of the slab [$mm$].
    v_rd_max : MPA
        [$v_{Rd,max}$] Maximum design shear stress [$MPa$].
    """

    label = "6.53"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        beta: DIMENSIONLESS,
        v_ed: N,
        u_0: MM,
        d: MM,
        v_rd_max: MPA,
    ) -> None:
        super().__init__()
        self.beta = beta
        self.v_ed = v_ed
        self.u_0 = u_0
        self.d = d
        self.v_rd_max = v_rd_max

    @staticmethod
    def _evaluate(
        beta: DIMENSIONLESS,
        v_ed: N,
        u_0: MM,
        d: MM,
        v_rd_max: MPA,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(u_0=u_0, d=d)
        raise_if_negative(beta=beta, v_ed=v_ed, v_rd_max=v_rd_max)

        return (beta * v_ed / (u_0 * d)) <= v_rd_max

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.53."""
        _equation: str = r"\frac{\beta \cdot V_{Ed}}{u_{0} \cdot d} \leq v_{Rd,max}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\beta": f"{self.beta:.3f}",
                r"V_{Ed}": f"{self.v_ed:.3f}",
                r"u_{0}": f"{self.u_0:.3f}",
                r" d": f" {self.d:.3f}",
                r"v_{Rd,max}": f"{self.v_rd_max:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label=r"\to",
            unit="",
        )
