"""Formula 6.3 from EN 1993-1-1:2005: Chapter 6 - Ultimate limit state."""

from collections.abc import Sequence

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_lists_differ_in_length, raise_if_negative


class Form6Dot3MinDeductionAreaStaggeredFastenerHoles(Formula):
    """Class representing formula 6.3 for the calculation of the minimum area deduction for staggered fastener holes [$A_{deduction}$]."""

    label = "6.3"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        t: MM,
        n: MM,
        d_0: MM,
        s: Sequence[MM],
        p: Sequence[MM],
    ) -> None:
        """[$A_{deduction}$] Calculation of the area deduction for staggered fastener holes [$mm^2$].

        EN 1993-1-1:2005 art.6.2.2.2 (4) b) - Formula (6.3)
        section (4) a) should be handled separately.

        Parameters
        ----------
        t : MM
            [$t$] Thickness [$mm$].
        n : MM
            [$n$] Number of holes extending in any diagonal or zig-zag line progressively across the member, see Figure 6.1 [$mm$].
        d_0 : MM
            [$d_0$] Diameter of hole [$mm$].
        s : Sequence[MM]
            [$s$] Staggered pitch, the spacing of the centres of two consecutive holes in the
            chain measured parallel to the member axis [$mm$].
        p : Sequence[MM]
            [$p$] Spacing of the centres of the same two holes measured perpendicular to the member axis [$mm$].
        """
        super().__init__()
        self.t = t
        self.n = n
        self.d_0 = d_0
        self.s = s
        self.p = p

    @staticmethod
    def _evaluate(
        t: MM,
        n: MM,
        d_0: MM,
        s: Sequence[MM],
        p: Sequence[MM],
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(t=t, n=n, d_0=d_0)
        raise_if_less_or_equal_to_zero(t=t, n=n, d_0=d_0)
        raise_if_lists_differ_in_length(s=s, p=p)
        for s_i, p_i in zip(s, p):
            raise_if_negative(s=s_i, p=p_i)
            raise_if_less_or_equal_to_zero(s=s_i, p=p_i)

        return t * (n * d_0 - sum((s_i**2) / (4 * p_i) for s_i, p_i in zip(s, p)))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.3."""
        _equation: str = r"t \left( n \cdot d_0 - \sum \frac{s^2}{4 \cdot p} \right)"
        _numeric_equation: str = (
            rf"{self.t:.{n}f} \left( {self.n:.{n}f} \cdot {self.d_0:.{n}f} - \left( \frac{{{self.s[0]:.{n}f}^2}}"
            rf"{{4 \cdot {self.p[0]:.{n}f}}}"
        )
        for s_i, p_i in zip(self.s[1:], self.p[1:]):
            _numeric_equation += rf" + \frac{{{s_i:.{n}f}^2}}{{4 \cdot {p_i:.{n}f}}}"
        _numeric_equation += r" \right) \right)"
        return LatexFormula(
            return_symbol=r"A_{deduction}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )
