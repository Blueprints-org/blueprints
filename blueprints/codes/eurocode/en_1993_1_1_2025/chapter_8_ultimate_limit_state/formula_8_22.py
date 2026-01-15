"""Formula 8.22 from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot22CheckShearForce(Formula):
    r"""Class representing formula 8.22 for checking the design value of the shear force."""

    label = "8.22"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        v_ed: N,
        v_c_rd: N,
    ) -> None:
        r"""Check the design value of the shear force at each cross section.

        EN 1993-1-1:2025 art.8.2.6(1) - Formula (8.22)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design value of the shear force [$N$].
        v_c_rd : N
            [$V_{c,Rd}$] Design shear resistance [$N$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.v_c_rd = v_c_rd

    @staticmethod
    def _evaluate(
        v_ed: N,
        v_c_rd: N,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(v_c_rd=v_c_rd)
        raise_if_negative(v_ed=v_ed)

        return v_ed / v_c_rd <= 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.22."""
        _equation: str = r"\left( \frac{V_{Ed}}{V_{c,Rd}} \leq 1.0 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "V_{Ed}": f"{self.v_ed:.{n}f}",
                "V_{c,Rd}": f"{self.v_c_rd:.{n}f}",
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
