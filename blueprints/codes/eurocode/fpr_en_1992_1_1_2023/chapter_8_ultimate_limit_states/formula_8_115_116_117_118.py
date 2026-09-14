"""Formula 8.115, 8.116, 8.117 and 8.118 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot115To118StrengthReductionFactorCrossedByTie(Formula):
    """Class representing formulas 8.115, 8.116, 8.117 and 8.118 for the calculation of the strength reduction factor
    for compression fields and struts crossed or deviated by a tie at an angle.
    """

    label = "8.115/8.116/8.117/8.118"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        theta_cs: DEG,
    ) -> None:
        r"""[$\nu$] Strength reduction factor for compression fields and struts crossed or deviated by a tie at an
        angle [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.5.2(4) - Formula (8.115), (8.116), (8.117) and (8.118)

        Parameters
        ----------
        theta_cs : DEG
            [$\theta_{cs}$] Smallest angle between the strut representing the resultant of the compression field
            and any of the ties that cross with the strut, as defined in Figure 8.26 [$degrees$].
        """
        super().__init__()
        self.theta_cs = theta_cs

    @staticmethod
    def _evaluate(
        theta_cs: DEG,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(theta_cs=theta_cs)

        if 20 <= theta_cs < 30:
            return 0.4
        if 30 <= theta_cs < 40:
            return 0.55
        if 40 <= theta_cs < 60:
            return 0.7
        if 60 <= theta_cs < 90:
            return 0.85
        raise ValueError(f"theta_cs of {theta_cs} degrees is outside the range covered by formulas (8.115) to (8.118): 20 <= theta_cs < 90 degrees.")

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 8.115, 8.116, 8.117 and 8.118."""
        _equation: str = (
            r"\begin{cases} 0.4 & \text{if } 20^\circ \leq \theta_{cs} < 30^\circ \\ "
            r"0.55 & \text{if } 30^\circ \leq \theta_{cs} < 40^\circ \\ "
            r"0.7 & \text{if } 40^\circ \leq \theta_{cs} < 60^\circ \\ "
            r"0.85 & \text{if } 60^\circ \leq \theta_{cs} < 90^\circ \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta_{cs}": f"{self.theta_cs:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta_{cs}": rf"{self.theta_cs:.{n}f} ^\circ",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\nu",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
