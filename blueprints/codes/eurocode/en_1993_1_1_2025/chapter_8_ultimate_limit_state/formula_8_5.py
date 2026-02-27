"""Formula 8.5 from EN 1993-1-1:2025: Chapter 8 - Ultimate limit state."""

from collections.abc import Sequence

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_lists_differ_in_length, raise_if_negative


class Form8Dot5MinDeductionAreaStaggeredFastenerHoles(Formula):
    r"""Class representing formula 8.5 for the calculation of the minimum area deduction for staggered fastener holes [$\Delta A_{net,1}$]."""

    label = "8.5"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        t: MM,
        n_1: MM,
        d_0: MM,
        s: Sequence[MM],
        p_2: Sequence[MM],
    ) -> None:
        r"""[$\Delta A_{net,1}$] Calculation of the area deduction for staggered fastener holes [$mm^2$].

        EN 1993-1-1:2025 art.8.2.2.2 (4) b) - Formula (8.5)
        section (4) a) should be handled separately.

        Parameters
        ----------
        t : MM
            [$t$] Thickness [$mm$].
        n_1 : MM
            [$n_1$] Number of holes extending in any diagonal or zig-zag line progressively across the member, see Figure 8.1 [$mm$].
        d_0 : MM
            [$d_0$] Diameter of hole [$mm$].
        s : Sequence[MM]
            [$s$] Staggered pitch, the spacing of the centres of two consecutive holes in the
            chain measured parallel to the member axis [$mm$].
        p_2 : Sequence[MM]
            [$p_2$] Spacing of the centres of the same two holes measured perpendicular to the member axis [$mm$].
        """
        super().__init__()
        self.t = t
        self.n_1 = n_1
        self.d_0 = d_0
        self.s: Sequence[MM] = s
        self.p_2: Sequence[MM] = p_2

    @staticmethod
    def _evaluate(
        t: MM,
        n_1: MM,
        d_0: MM,
        s: Sequence[MM],
        p_2: Sequence[MM],
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(t=t, n_1=n_1, d_0=d_0)
        raise_if_less_or_equal_to_zero(t=t, n_1=n_1, d_0=d_0)
        raise_if_lists_differ_in_length(s=s, p_2=p_2)
        for s_i, p_2_i in zip(s, p_2):
            raise_if_negative(s=s_i, p_2=p_2_i)
            raise_if_less_or_equal_to_zero(s=s_i, p_2=p_2_i)

        return t * (n_1 * d_0 - sum((s_i**2) / (4 * p_2_i) for s_i, p_2_i in zip(s, p_2)))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.5."""
        _equation: str = r"t \left( n_1 \cdot d_0 - \sum \frac{s^2}{4 \cdot p_2} \right)"
        _numeric_equation: str = (
            rf"{self.t:.{n}f} \left( {self.n_1:.{n}f} \cdot {self.d_0:.{n}f} - \left( \frac{{{self.s[0]:.{n}f}^2}}"
            rf"{{4 \cdot {self.p_2[0]:.{n}f}}}"
        )
        for s_i, p_2_i in zip(self.s[1:], self.p_2[1:]):
            _numeric_equation += rf" + \frac{{{s_i:.{n}f}^2}}{{4 \cdot {p_2_i:.{n}f}}}"
        _numeric_equation += r" \right) \right)"
        return LatexFormula(
            return_symbol=r"\Delta A_{net,1}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )
