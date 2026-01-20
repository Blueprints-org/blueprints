"""Formula 8.52af from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot52afHollowSections(Formula):
    r"""Class representing formula 8.52af for [$a_f$] in hollow sections."""

    label = "8.52af_hollow"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        a: MM2,
        h: MM,
        t: MM,
    ) -> None:
        r"""[$a_f$] Calculation of the reduction factor for hollow sections (dimensionless).

        EN 1993-1-1:2025 art.8.2.9.1(6) - Formula (8.52af)

        Parameters
        ----------
        a : MM2
            [$A$] Total cross-sectional area [$mm^2$].
        h : MM
            [$h$] Height of the section [$mm$].
        t : MM
            [$t$] Thickness of the section [$mm$].
        """
        super().__init__()
        self.a = a
        self.h = h
        self.t = t

    @staticmethod
    def _evaluate(
        a: MM2,
        h: MM,
        t: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, h=h, t=t)
        raise_if_less_or_equal_to_zero(denominator=a)

        return min((a - 2 * h * t) / a, 0.5)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.40af."""
        _equation: str = r"\min \left( \frac{A - 2 \cdot h \cdot t}{A}, 0.5 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r" h": f" {self.h:.{n}f}",
                r" t": f" {self.t:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A": rf"{self.a:.{n}f} \ mm^2",
                r" h": rf" {self.h:.{n}f} \ mm",
                r" t": rf" {self.t:.{n}f} \ mm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"a_f",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"=",
            unit="-",
        )


class Form8Dot52afWeldedBoxSections(Formula):
    r"""Class representing formula 8.52af for [$a_f$] in welded box sections."""

    label = "8.52af_welded_box"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        a: MM2,
        h: MM,
        t_w: MM,
    ) -> None:
        r"""[$a_f$] Calculation of the reduction factor for welded box sections (dimensionless).

        EN 1993-1-1:2025 art.8.2.9.1(6) - Formula (8.52af)

        Parameters
        ----------
        a : MM2
            [$A$] Total cross-sectional area [$mm^2$].
        h : MM
            [$h$] Height of the section [$mm$].
        t_w : MM
            [$t_w$] Web thickness [$mm$].
        """
        super().__init__()
        self.a = a
        self.h = h
        self.t_w = t_w

    @staticmethod
    def _evaluate(
        a: MM2,
        h: MM,
        t_w: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, h=h, t_w=t_w)
        raise_if_less_or_equal_to_zero(denominator=a)

        return min((a - 2 * h * t_w) / a, 0.5)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.52af."""
        _equation: str = r"\min \left( \frac{A - 2 \cdot h \cdot t_w}{A}, 0.5 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r" h": f" {self.h:.{n}f}",
                r"t_w": f"{self.t_w:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"A": rf"{self.a:.{n}f} \ mm^2",
                r" h": rf" {self.h:.{n}f} \ mm",
                r"t_w": rf"{self.t_w:.{n}f} \ mm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"a_f",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"=",
            unit="-",
        )
