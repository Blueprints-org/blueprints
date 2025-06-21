"""Formula 6.9 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot9CheckCompressionForce(Formula):
    r"""Class representing formula 6.9 for the test of the compression force."""

    label = "6.9"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        n_ed: N,
        n_c_rd: N,
    ) -> None:
        r"""Check the compression force.

        EN 1993-1-1:2005 art.6.2.4(1) - Formula (6.9)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design value of the compression force [N].
        n_c_rd : N
            [$N_{c,Rd}$] Design resistance of the cross-section for uniform compression [N].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_c_rd = n_c_rd

    @staticmethod
    def _evaluate(
        n_ed: N,
        n_c_rd: N,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_c_rd=n_c_rd)
        raise_if_negative(n_ed=n_ed)

        return n_ed / n_c_rd <= 1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.9."""
        _equation: str = r"\left( \frac{N_{Ed}}{N_{c,Rd}} \leq 1 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "N_{Ed}": f"{self.n_ed:.{n}f}",
                "N_{c,Rd}": f"{self.n_c_rd:.{n}f}",
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
