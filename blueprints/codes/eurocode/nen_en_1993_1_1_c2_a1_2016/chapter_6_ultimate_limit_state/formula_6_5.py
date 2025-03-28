"""Formula 6.5 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot5UnityCheckTensileStrength(Formula):
    """Class representing formula 6.5 for the unity check for tensile strength."""

    label = "6.5"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        n_ed: N,
        n_t_rd: N,
    ) -> None:
        r"""[$N_{Ed}/N_{t,Rd} \leq 1$] Unity check for tensile strength of an element in tension.

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.3(1) - Formula (6.5)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design value of the normal tensile force [$N$].
        n_t_rd : N
            [$N_{t,Rd}$] Design value of the resistance against tensile force [$N$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_t_rd = n_t_rd

    @staticmethod
    def _evaluate(
        n_ed: N,
        n_t_rd: N,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_t_rd=n_t_rd)
        raise_if_negative(n_ed=n_ed)
        return (n_ed / n_t_rd) <= 1

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.5."""
        _equation: str = r"\left( \frac{N_{Ed}}{N_{t,Rd}} \leq 1 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "N_{Ed}": f"{self.n_ed:.3f}",
                "N_{t,Rd}": f"{self.n_t_rd:.3f}",
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
