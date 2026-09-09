"""Formula 8.96 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot96PunchingShearGradientEnhancementCoefficient(Formula):
    r"""Class representing formula 8.96 for the calculation of the punching shear gradient enhancement
    coefficient.

    The standard prints this as an expression bounded both below and above, [$1 \leq k_{pb} \leq 2,5$], which is
    implemented as a minimum of a maximum.
    """

    label = "8.96"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        b_0: MM,
        b_0_5: MM,
    ) -> None:
        r"""[$k_{pb}$] Punching shear gradient enhancement coefficient [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.3(1) - Formula (8.96)

        Parameters
        ----------
        b_0 : MM
            [$b_0$] Length of the perimeter at the face of the supporting area (see Figure 8.18). Near to
            re-entrant corners of the supporting area and close to slab edges, the perimeter [$b_0$] should be
            placed parallel to [$b_{0,5}$] (see Figures 8.18c)-(e)). For large supporting areas, wall ends, wall
            corners, slabs with openings and with inserts, the rules of 8.4.2(3) apply (see Figure 8.19) [$mm$].
        b_0_5 : MM
            [$b_{0,5}$] Length of the control perimeter, taken at a distance [$0,5 d_v$] from the face of the
            supporting area according to 8.4.2(2) to (5) [$mm$].
        """
        super().__init__()
        self.b_0 = b_0
        self.b_0_5 = b_0_5

    @staticmethod
    def _evaluate(
        b_0: MM,
        b_0_5: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(b_0=b_0)
        raise_if_less_or_equal_to_zero(b_0_5=b_0_5)

        return min(max(3.6 * np.sqrt(1 - b_0 / b_0_5), 1), 2.5)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.96."""
        _equation: str = r"\min\left(\max\left(3.6 \cdot \sqrt{1 - \frac{b_0}{b_{0,5}}}, 1\right), 2.5\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_0": f"{self.b_0:.{n}f}",
                r"b_{0,5}": f"{self.b_0_5:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_0": rf"{self.b_0:.{n}f} \ mm",
                r"b_{0,5}": rf"{self.b_0_5:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"k_{pb}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
