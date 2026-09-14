"""Formula 8.71 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS


class Form8Dot71StrengthReductionFactor(Formula):
    r"""Class representing formula 8.71 for the strength reduction factor of the compression field in the flange.

    The standard prints a bare value rather than an expression, so this class takes no arguments. It exists to
    give the value the same label, source reference and representation as every other numbered formula, and to
    be passed to Formula (8.70) instead of a loose 0,5 in calling code. Lower angles of the inclined compression
    field in the tensile flange than those of 8.2.5(3) require [$\nu$] to be calculated on the basis of the state
    of strains of the member according to 8.2.5(5), which is a separate route and not this value.
    """

    label = "8.71"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self) -> None:
        r"""[$\nu$] Strength reduction factor that may be used in Formula (8.70) [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.2.5(4) - Formula (8.71)
        """
        super().__init__()

    @staticmethod
    def _evaluate() -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        return 0.5

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.71."""
        return LatexFormula(
            return_symbol=r"\nu",
            result=f"{self:.{n}f}",
            equation=r"0.5",
            # There is nothing to substitute in a printed constant, so the numeric representations are left
            # empty rather than repeating the same number twice.
            comparison_operator_label="=",
            unit="-",
        )
