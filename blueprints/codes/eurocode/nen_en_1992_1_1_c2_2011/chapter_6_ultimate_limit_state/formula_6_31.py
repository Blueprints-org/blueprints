"""Formula 6.31 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot31CheckTorsionShearResistanceRectangular(Formula):
    r"""Class representing formula 6.31 for checking the maximum resistance of a member subjected to torsion and shear."""

    label = "6.31"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        t_ed: NMM,
        t_rd_c: NMM,
        v_ed: N,
        v_rd_c: N,
    ) -> None:
        r"""Check the maximum resistance of a member subjected to torsion and shear.

        NEN-EN 1992-1-1+C2:2011 art.6.3.2(4) - Formula (6.31)

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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.31."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\left( \frac{T_{Ed}}{T_{Rd,c}} + \frac{V_{Ed}}{V_{Rd,c}} \leq 1 \right)",
            numeric_equation=rf"\left( \frac{{{self.t_ed:.3f}}}{{{self.t_rd_c:.3f}}} + "
            rf"\frac{{{self.v_ed:.3f}}}{{{self.v_rd_c:.3f}}} \leq 1 \right)",
            comparison_operator_label="\\to",
            unit="",
        )
