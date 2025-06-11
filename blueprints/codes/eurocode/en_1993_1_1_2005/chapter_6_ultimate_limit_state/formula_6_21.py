"""Formula 6.21 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot21ShearStressIOrHSection(Formula):
    r"""Class representing formula 6.21 for the calculation of [$\tau_{Ed}$]."""

    label = "6.21"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        v_ed: N,
        a_w: MM2,
        a_f: MM2,
    ) -> None:
        r"""[$\tau_{Ed}$] Calculation of the design elastic shear stress [$MPa$].
        For I- or H-sections the shear stress in the web may be taken with this equation.

        EN 1993-1-1:2005 art.6.2.6(5) - Formula (6.21)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design shear force [$N$].
        a_w : MM2
            [$A_w$] Area of the web [$mm^2$].
        a_f : MM2
            [$A_f$] Area of one flange [$mm^2$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.a_w = a_w
        self.a_f = a_f

    @staticmethod
    def _evaluate(
        v_ed: N,
        a_w: MM2,
        a_f: MM2,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed=v_ed, a_f=a_f)
        raise_if_less_or_equal_to_zero(a_w=a_w)
        if not a_f / a_w >= 0.6:
            raise ValueError("A_f / A_w must be greater than or equal to 0.6")

        return v_ed / a_w

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.21."""
        _equation: str = r"\frac{V_{Ed}}{A_w} \text{ if } A_f / A_w \ge 0.6"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"V_{Ed}": f"{self.v_ed:.3f}",
                r"A_w": f"{self.a_w:.3f}",
                r"A_f": f"{self.a_f:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Ed}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
