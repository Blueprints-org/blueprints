"""Formula 8.51aw from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot51awHollowSections(Formula):
    r"""Class representing formula 8.51aw for [$a_w$] in hollow sections."""

    label = "8.51aw_hollow"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        a: MM2,
        b: MM,
        t: MM,
    ) -> None:
        r"""[$a_w$] Calculation of the reduction factor for hollow sections (dimensionless).

        EN 1993-1-1:2025 art.8.2.9.1(6) - Formula (8.51aw)

        Parameters
        ----------
        a : MM2
            [$A$] Total cross-sectional area [$mm^2$].
        b : MM
            [$b$] Width of the section [$mm$].
        t : MM
            [$t$] Thickness of the section [$mm$].
        """
        super().__init__()
        self.a = a
        self.b = b
        self.t = t

    @staticmethod
    def _evaluate(
        a: MM2,
        b: MM,
        t: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b=b, t=t)
        raise_if_less_or_equal_to_zero(denominator=a)

        return min((a - 2 * b * t) / a, 0.5)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.39aw."""
        _equation: str = r"\min \left( \frac{A - 2 \cdot b \cdot t}{A}, 0.5 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r"b": f"{self.b:.{n}f}",
                r" t": f" {self.t:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A": rf"{self.a:.{n}f} \ mm^2",
                r"b": rf"{self.b:.{n}f} \ mm",
                r" t": rf" {self.t:.{n}f} \ mm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"a_w",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"=",
            unit="-",
        )


class Form8Dot51awWeldedBoxSections(Formula):
    r"""Class representing formula 8.51aw for [$a_w$] in welded box sections."""

    label = "8.51aw_welded_box"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        a: MM2,
        b: MM,
        t_f: MM,
    ) -> None:
        r"""[$a_w$] Calculation of the reduction factor for welded box sections (dimensionless).

        EN 1993-1-1:2025 art.8.2.9.1(6) - Formula (8.51aw)

        Parameters
        ----------
        a : MM2
            [$A$] Total cross-sectional area [$mm^2$].
        b : MM
            [$b$] Width of the section [$mm$].
        t_f : MM
            [$t_f$] Flange thickness [$mm$].
        """
        super().__init__()
        self.a = a
        self.b = b
        self.t_f = t_f

    @staticmethod
    def _evaluate(
        a: MM2,
        b: MM,
        t_f: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, b=b, t_f=t_f)
        raise_if_less_or_equal_to_zero(denominator=a)

        return min((a - 2 * b * t_f) / a, 0.5)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.51aw."""
        _equation: str = r"\min \left( \frac{A - 2 \cdot b \cdot t_f}{A}, 0.5 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r"b": f"{self.b:.{n}f}",
                r"t_f": f"{self.t_f:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A": rf"{self.a:.{n}f} \ mm^2",
                r"b": rf"{self.b:.{n}f} \ mm",
                r"t_f": rf"{self.t_f:.{n}f} \ mm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"a_w",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"=",
            unit="-",
        )
