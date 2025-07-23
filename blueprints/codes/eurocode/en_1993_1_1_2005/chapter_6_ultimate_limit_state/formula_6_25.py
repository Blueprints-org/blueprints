"""Formula 6.25 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot25CheckCombinedShearForceAndTorsionalMoment(Formula):
    r"""Class representing formula 6.25 for combined shear force and torsional moment."""

    label = "6.25"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        v_ed: N,
        v_pl_t_rd: N,
    ) -> None:
        r"""Check the combined shear force and torsional moment.

        EN 1993-1-1:2005 art.6.2.7(9) - Formula (6.25)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design shear force [$N$].
        v_pl_t_rd : N
            [$V_{pl,T,Rd}$] Plastic shear resistance accounting for torsional effects, derived from equation 6.26, 6.27 or 6.28 [$N$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.v_pl_t_rd = v_pl_t_rd

    @staticmethod
    def _evaluate(
        v_ed: N,
        v_pl_t_rd: N,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(v_pl_t_rd=v_pl_t_rd)
        raise_if_negative(v_ed=v_ed)

        return v_ed / v_pl_t_rd <= 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.25."""
        _equation: str = r"\left( \frac{V_{Ed}}{V_{pl,T,Rd}} \leq 1.0 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "V_{Ed}": f"{self.v_ed:.{n}f}",
                "V_{pl,T,Rd}": f"{self.v_pl_t_rd:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
