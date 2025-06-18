"""Formula 6.23 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot23CheckTorsionalMoment(Formula):
    r"""Class representing formula 6.23 for checking torsional moment."""

    label = "6.23"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        t_ed: NMM,
        t_rd: NMM,
    ) -> None:
        r"""Check the torsional moment at each cross-section.

        EN 1993-1-1:2005 art.6.2.7(1) - Formula (6.23)

        Parameters
        ----------
        t_ed : NMM
            [$T_{Ed}$] Design value of the torsional moment [$Nmm$].
        t_rd : NMM
            [$T_{Rd}$] Design torsional resistance of the cross section [$Nmm$].
        """
        super().__init__()
        self.t_ed = t_ed
        self.t_rd = t_rd

    @staticmethod
    def _evaluate(
        t_ed: NMM,
        t_rd: NMM,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(t_rd=t_rd)
        raise_if_negative(t_ed=t_ed)

        return t_ed / t_rd <= 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.23."""
        _equation: str = r"\left( \frac{T_{Ed}}{T_{Rd}} \leq 1.0 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "T_{Ed}": f"{self.t_ed:.{n}f}",
                "T_{Rd}": f"{self.t_rd:.{n}f}",
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
