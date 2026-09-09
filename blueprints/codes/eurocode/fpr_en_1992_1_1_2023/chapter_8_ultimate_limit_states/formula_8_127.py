"""Formula 8.127 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2
from blueprints.validations import raise_if_negative


class Form8Dot127ConcentricallyLoadedArea(Formula):
    r"""Class representing formula 8.127 for the calculation of a concentrically loaded area."""

    label = "8.127"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        a_0: MM,
        b_0: MM,
    ) -> None:
        r"""[$A_{c0}$] Concentrically loaded area [$mm^2$].

        FprEN 1992-1-1:2023 (E) art. 8.6(2) - Formula (8.127)

        Parameters
        ----------
        a_0 : MM
            [$a_0$] Length of the loaded area in the direction perpendicular to the closest edge of the load
            introduction block, see Figure 8.32 [$mm$].
        b_0 : MM
            [$b_0$] Width of the loaded area, see Figure 8.32 [$mm$].
        """
        super().__init__()
        self.a_0 = a_0
        self.b_0 = b_0

    @staticmethod
    def _evaluate(
        a_0: MM,
        b_0: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_0=a_0, b_0=b_0)

        return a_0 * b_0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.127."""
        _equation: str = r"a_0 \cdot b_0"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_0": f"{self.a_0:.{n}f}",
                r"b_0": f"{self.b_0:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_0": rf"{self.a_0:.{n}f} \ mm",
                r"b_0": rf"{self.b_0:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"A_{c0}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm^2",
        )
