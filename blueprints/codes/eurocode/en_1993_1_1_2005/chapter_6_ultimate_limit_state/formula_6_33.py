"""Formula 6.33 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_negative


class Form6Dot33CheckAxialForceY(Formula):
    r"""Class representing formula 6.33 for checking axial force about the y-y axis."""

    label = "6.33"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        n_ed: N,
        n_pl_rd: N,
    ) -> None:
        r"""For doubly symmetrical I- and H-sections or other flanges sections,
        allowance need not be made for the effect of the axial force on the
        plastic resistance moment about the y-y axis when 6.33 and 6.34 are satisfied.

        EN 1993-1-1:2005 art.6.2.9(4) - Formula (6.33)

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design axial force [$N$].
        n_pl_rd : N
            [$N_{pl,Rd}$] Plastic resistance normal force [$N$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_pl_rd = n_pl_rd

    @staticmethod
    def _evaluate(
        n_ed: N,
        n_pl_rd: N,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(n_pl_rd=n_pl_rd)

        return n_ed <= 0.25 * n_pl_rd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.33."""
        _equation: str = r"N_{Ed} \leq 0.25 \cdot N_{pl,Rd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"N_{pl,Rd}": f"{self.n_pl_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"N_{pl,Rd}": rf"{self.n_pl_rd:.{n}f} \ N",
            },
            True,
        )
        return LatexFormula(
            return_symbol="CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="\\to",
            unit="",
        )
