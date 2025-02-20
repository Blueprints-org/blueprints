"""Formula 6.54 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot54ControlPerimeter(Formula):
    r"""Class representing formula 6.54 for the calculation of the control perimeter at which shear reinforcement is not required."""

    label = "6.54"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        beta: DIMENSIONLESS,
        v_ed: N,
        v_rd_c: MPA,
        d: MM,
    ) -> None:
        r"""[u_out,ef] Calculation of the control perimeter at which shear reinforcement is not required.

        NEN-EN 1992-1-1+C2:2011 art.6.5.4(4) - Formula (6.54)

        Parameters
        ----------
        beta : DIMENSIONLESS
            [$\beta$] Factor as per 6.4.3 (3), (4) and (5) [$-$].
        v_ed : N
            [$V_{Ed}$] Design shear force [$N$].
        v_rd_c : MPA
            [$v_{Rd,c}$] Design shear strength of concrete [$MPa$].
        d : MM
            [$d$] Effective depth of the slab [$mm$].
        """
        super().__init__()
        self.beta = beta
        self.v_ed = v_ed
        self.v_rd_c = v_rd_c
        self.d = d

    @staticmethod
    def _evaluate(
        beta: DIMENSIONLESS,
        v_ed: N,
        v_rd_c: MPA,
        d: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(beta=beta, v_ed=v_ed)
        raise_if_less_or_equal_to_zero(v_rd_c=v_rd_c, d=d)

        return beta * v_ed / (v_rd_c * d)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.54."""
        _equation: str = r"\frac{\beta \cdot V_{Ed}}{v_{Rd,c} \cdot d}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\beta": f"{self.beta:.3f}",
                r"V_{Ed}": f"{self.v_ed:.3f}",
                r"v_{Rd,c}": f"{self.v_rd_c:.3f}",
                r" d": f" {self.d:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"u_{out,ef}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm",
        )
