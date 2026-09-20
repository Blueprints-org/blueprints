"""Formula 8.124 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot124SpreadingAngleTangent(Formula):
    r"""Class representing formula 8.124 for the calculation of the tangent of the spreading angle of a
    concentrated force introduced into a member.
    """

    label = "8.124"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        a: MM,
        b: MM,
        h: MM,
    ) -> None:
        r"""[$\tan\theta_{cf}$] Tangent of the spreading angle [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.5.5(2) - Formula (8.124)

        For the wide element case shown in Figures 8.30 c) and d), where [$b > a + H/2$], this formula is
        replaced by [$\tan\theta_{cf} = 0.5$].

        Parameters
        ----------
        a : MM
            [$a$] Length of the loaded area in the direction considered, as defined in Figure 8.30 a) [$mm$].
        b : MM
            [$b$] Width of the member in the direction considered, as defined in Figure 8.30 a) [$mm$].
        h : MM
            [$H$] Height of the member over which the concentrated force spreads, as defined in Figure
            8.30 c) and d) [$mm$].
        """
        super().__init__()
        self.a = a
        self.b = b
        self.h = h

    @staticmethod
    def _evaluate(
        a: MM,
        b: MM,
        h: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, h=h)
        raise_if_less_or_equal_to_zero(b=b)

        if b > a + h / 2:
            return 0.5
        return (1 - a / b) / 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.124."""
        _equation: str = r"\begin{cases} \dfrac{1 - a/b}{2} & \text{if } b \leq a + H/2 \\ 0.5 & \text{if } b > a + H/2 \end{cases}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a/b": f"{self.a:.{n}f}/{self.b:.{n}f}",
                r"a + H/2": f"{self.a:.{n}f} + {self.h:.{n}f}/2",
                r"b \leq": f"{self.b:.{n}f} \\leq",
                r"b >": f"{self.b:.{n}f} >",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = _numeric_equation
        return LatexFormula(
            return_symbol=r"\tan\theta_{cf}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
