"""Formula 6.49 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA, N
from blueprints.validations import raise_if_negative


class Form6Dot49AppliedPunchingShearStress(Formula):
    r"""Class representing formula 6.49 for the calculation of applied punching shear stress [$v_{Ed}$] of slabs and column bases
    without shear reinforcement.
    """

    label = "6.49"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        v_ed_red: N,
        u: MM,
        d: MM,
    ) -> None:
        r"""[$v_{Ed}$] Calculation of applied punching shear stress [$v_{Ed}$] of slabs and column bases without shear reinforcement.

        EN 1992-1-1:2004 art.6.4.4(2) - Formula (6.49)

        Parameters
        ----------
        v_ed_red : N
            [$V_{Ed,red}$] Net applied punching force [$N$].
        u : MM
            [$u$] Punching perimeter [$mm$].
        d : MM
            [$d$] Effective depth [$mm$].
        """
        super().__init__()
        self.v_ed_red = v_ed_red
        self.u = u
        self.d = d

    @staticmethod
    def _evaluate(
        v_ed_red: N,
        u: MM,
        d: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed_red=v_ed_red, u=u, d=d)
        return v_ed_red / (u * d)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.49."""
        _equation: str = r"\frac{V_{Ed,red}}{u \cdot d}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"V_{Ed,red}": f"{self.v_ed_red:.{n}f}",
                r"u": f"{self.u:.{n}f}",
                r" d": f" {self.d:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"v_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
