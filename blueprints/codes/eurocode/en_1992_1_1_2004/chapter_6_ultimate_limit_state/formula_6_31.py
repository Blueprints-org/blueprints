"""Formula 6.31 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot31CheckTorsionShearResistanceRectangular(Formula):
    r"""Class representing formula 6.31 for checking the maximum resistance of a member subjected to torsion and shear."""

    label = "6.31"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        t_ed: NMM,
        t_rd_c: NMM,
        v_ed: N,
        v_rd_c: N,
    ) -> None:
        r"""Check the maximum resistance of a member subjected to torsion and shear.

        EN 1992-1-1:2004 art.6.3.2(4) - Formula (6.31)

        Parameters
        ----------
        t_ed : NMM
            [$T_{Ed}$] Design torsional moment [$Nmm$].
        t_rd_c : NMM
            [$T_{Rd,c}$] the torsional cracking moment, which may be determined by setting tau_t,i = fctd [$Nmm$].
        v_ed : N
            [$V_{Ed}$] Design transverse force [$N$].
        v_rd_c : N
            [$V_{Rd,c}$] follows from Expression (6.2) [$N$].
        """
        super().__init__()
        self.t_ed = t_ed
        self.t_rd_c = t_rd_c
        self.v_ed = v_ed
        self.v_rd_c = v_rd_c

    @staticmethod
    def _evaluate(
        t_ed: NMM,
        t_rd_c: NMM,
        v_ed: N,
        v_rd_c: N,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(t_ed=t_ed, v_ed=v_ed)
        raise_if_less_or_equal_to_zero(t_rd_c=t_rd_c, v_rd_c=v_rd_c)

        return (t_ed / t_rd_c + v_ed / v_rd_c) <= 1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.31."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\left( \frac{T_{Ed}}{T_{Rd,c}} + \frac{V_{Ed}}{V_{Rd,c}} \leq 1 \right)",
            numeric_equation=rf"\left( \frac{{{self.t_ed:.{n}f}}}{{{self.t_rd_c:.{n}f}}} + "
            rf"\frac{{{self.v_ed:.{n}f}}}{{{self.v_rd_c:.{n}f}}} \leq 1 \right)",
            comparison_operator_label="\\to",
            unit="",
        )
