"""Formula 8.6 from EN 1995-1-1:2025: Chapter 8 - Design compressive stress perpendicular to grain."""

from blueprints.codes.eurocode.en_1995_1_1_2025 import EN_1995_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot6DesignCompressiveStressPerpendicularToGrain(Formula):
    r"""Class representing formula 8.6 for the calculation of the design compressive stress perpendicular to grain."""

    label = "8.6"
    source_document = EN_1995_1_1_2025

    def __init__(
        self,
        capital_f_90_d: N,
        a: MM2,
    ) -> None:
        r"""[$\sigma_{c,90,d}$] Design compressive stress perpendicular to grain [$MPa$].

        EN 1995-1-1:2025 art.8.6 - Formula (8.6)

        Parameters
        ----------
        capital_f_90_d : N
                [$F_{c,90,d}$] Design compressive force perpendicular to grain [$N$].
        a : MM2
                [$a$] Area of the applied force [$mm^2$].
        """
        super().__init__()
        self.capital_f_90_d = capital_f_90_d
        self.a = a

    @staticmethod
    def _evaluate(
        capital_f_90_d: N,
        a: MM2,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(capital_f_90_d=capital_f_90_d)
        raise_if_less_or_equal_to_zero(a=a)
        # Convert N/mm2 (MPa)
        return capital_f_90_d / a

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.6."""
        _equation: str = r"\frac{F_{c,90,d}}{A}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"F_{c,90,d}": f"{self.capital_f_90_d:.{n}f}",
                r"A": f"{self.a:.{n}f}",
            },
            True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "F_{c,90,d}": rf"{self.capital_f_90_d:.{n}f} \, N",
                "A": rf"{self.a:.{n}f} \, mm^2",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{c,90,d}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
