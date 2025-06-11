"""Formula 6.5 from EN 1993-1-1:2005: Chapter 6 - Ultimate limit state."""

# pylint: disable=arguments-differ
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, RATIO
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot5UnityCheckTensileStrength(Formula):
    """Class representing formula 6.5 for the unity check for tensile strength."""

    label = "6.5"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        n_ed: KN,
        n_t_rd: KN,
    ) -> None:
        r"""[$N_{Ed}/N_{t,Rd}$] Unity check for tensile strength of an element in tension.

        EN 1993-1-1:2005 art.6.2.3(1) - Formula (6.5)

        Parameters
        ----------
        n_ed : KN
            [$N_{Ed}$] Design value of the normal tensile force [kN].
        n_t_rd : KN
            [$N_{t,Rd}$] Design value of the resistance against tensile force [kN].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_t_rd = n_t_rd

    @staticmethod
    def _evaluate(
        n_ed: KN,
        n_t_rd: KN,
    ) -> RATIO:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_t_rd=n_t_rd)
        raise_if_negative(n_ed=n_ed)
        return n_ed / n_t_rd

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.5."""
        return LatexFormula(
            return_symbol=r"N_{Ed}/N_{t,Rd}",
            result=f"{self:.2f}",
            equation=r"N_{Ed} / N_{t,Rd}",
            numeric_equation=rf"{self.n_ed:.2f} / {self.n_t_rd:.2f}",
            comparison_operator_label="=",
        )
