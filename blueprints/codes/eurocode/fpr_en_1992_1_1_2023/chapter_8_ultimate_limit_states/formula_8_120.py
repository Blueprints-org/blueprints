"""Formula 8.120 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS


class Form8Dot120StrengthReductionFactorUncrackedStrut(Formula):
    """Class representing formula 8.120 for the calculation of the strength reduction factor for compression
    fields and struts in a region without transverse cracking.
    """

    label = "8.120"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self) -> None:
        r"""[$\nu$] Strength reduction factor for compression fields and struts in a region without transverse
        cracking, for example when transverse compressive stresses are present [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.5.2(4) - Formula (8.120)
        """
        super().__init__()

    @staticmethod
    def _evaluate() -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.120."""
        return LatexFormula(
            return_symbol=r"\nu",
            result=f"{self:.{n}f}",
            equation=r"1.0",
            numeric_equation=r"1.0",
            numeric_equation_with_units=r"1.0",
            comparison_operator_label="=",
            unit="-",
        )
