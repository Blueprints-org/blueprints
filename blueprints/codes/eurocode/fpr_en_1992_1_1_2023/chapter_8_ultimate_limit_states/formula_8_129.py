"""Formula 8.129 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2
from blueprints.validations import raise_if_negative


class Form8Dot129ContributingConcreteArea(Formula):
    r"""Class representing formula 8.129 for the calculation of the contributing concrete area."""

    label = "8.129"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        a: MM,
        a_0: MM,
        b_0: MM,
        b: MM,
    ) -> None:
        r"""[$A_{c1}$] Contributing concrete area [$mm^2$].

        FprEN 1992-1-1:2023 (E) art. 8.6(2) - Formula (8.129)

        [$a_1$] is taken equal to [$a$], the length of the load introduction block parallel to [$a_0$], and
        [$b_1 = \min\left(b_0 + \left(a_1 - a_0\right), b\right)$], see Figure 8.32. The minimum height of the
        load introduction block should be [$h \geq a_1$].

        Parameters
        ----------
        a : MM
            [$a$] Length of the load introduction block parallel to [$a_0$], see Figure 8.32 [$mm$].
        a_0 : MM
            [$a_0$] Length of the loaded area in the direction perpendicular to the closest edge of the load
            introduction block, see Figure 8.32 [$mm$].
        b_0 : MM
            [$b_0$] Width of the loaded area, see Figure 8.32 [$mm$].
        b : MM
            [$b$] Width of the load introduction block, see Figure 8.32 [$mm$].
        """
        super().__init__()
        self.a = a
        self.a_0 = a_0
        self.b_0 = b_0
        self.b = b

    @staticmethod
    def _evaluate(
        a: MM,
        a_0: MM,
        b_0: MM,
        b: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, a_0=a_0, b_0=b_0, b=b)

        a_1 = a
        b_1 = min(b_0 + (a_1 - a_0), b)
        return a_1 * b_1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.129."""
        _equation: str = r"a \cdot \min\left(b_0 + \left(a - a_0\right), b\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a - a_0": f"{self.a:.{n}f} - {self.a_0:.{n}f}",
                r"b_0": f"{self.b_0:.{n}f}",
                r", b\right)": f", {self.b:.{n}f}" + r"\right)",
                r"a \cdot": f"{self.a:.{n}f} \\cdot",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a - a_0": rf"{self.a:.{n}f} \ mm - {self.a_0:.{n}f} \ mm",
                r"b_0": rf"{self.b_0:.{n}f} \ mm",
                r", b\right)": f", {self.b:.{n}f} \\ mm" + r"\right)",
                r"a \cdot": rf"{self.a:.{n}f} \ mm \cdot",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"A_{c1}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm^2",
        )
