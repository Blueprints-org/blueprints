"""Formula 6.29 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import NM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot29CheckTorsionShearResistance(Formula):
    r"""Class representing formula 6.29 for checking the maximum resistance of a member subjected to torsion and shear."""

    label = "6.29"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        t_ed: NM,
        v_ed: N,
        t_rd_max: NM,
        v_rd_max: N,
    ) -> None:
        r"""Check the maximum resistance of a member subjected to torsion and shear.

        NEN-EN 1992-1-1+C2:2011 art.6.3.2(4) - Formula (6.29)

        Parameters
        ----------
        t_ed : NM
            [$T_{Ed}$] Design torsional moment [$Nm$].
        v_ed : N
            [$V_{Ed}$] Design transverse force [$N$].
        t_rd_max : NM
            [$T_{Rd,max}$] Design torsional resistance moment according to equation 6.30 [$Nm$].
        v_rd_max : N
            [$V_{Rd,max}$] Maximum design shear resistance according to Expressions (6.9) or (6.14) [$N$].
        """
        super().__init__()
        self.t_ed = t_ed
        self.v_ed = v_ed
        self.t_rd_max = t_rd_max
        self.v_rd_max = v_rd_max

    @staticmethod
    def _evaluate(
        t_ed: NM,
        v_ed: N,
        t_rd_max: NM,
        v_rd_max: N,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(t_ed=t_ed, v_ed=v_ed)
        raise_if_less_or_equal_to_zero(t_rd_max=t_rd_max, v_rd_max=v_rd_max)

        return (t_ed / t_rd_max + v_ed / v_rd_max) <= 1

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.29."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\left( \frac{T_{Ed}}{T_{Rd,max}} + \frac{V_{Ed}}{V_{Rd,max}} \leq 1 \right)",
            numeric_equation=rf"\left( \frac{{{self.t_ed:.3f}}}{{{self.t_rd_max:.3f}}} + "
            rf"\frac{{{self.v_ed:.3f}}}{{{self.v_rd_max:.3f}}} \leq 1 \right)",
            comparison_operator_label="\\to",
            unit="",
        )
