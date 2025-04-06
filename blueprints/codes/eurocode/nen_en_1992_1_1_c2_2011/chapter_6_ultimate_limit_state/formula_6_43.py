"""Formula 6.43 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot43BetaRectangular(Formula):
    r"""Class representing formula 6.43 for the calculation of [$\beta$] for rectangular columns."""

    label = "6.43"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        ey: MM,
        ez: MM,
        by: MM,
        bz: MM,
    ) -> None:
        r"""[$\beta$] Calculation of [$\beta$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.3(3) - Formula (6.43)

        Parameters
        ----------
        ey : MM
            [$e_y$] Eccentricity along y-axis [$mm$].
        ez : MM
            [$e_z$] Eccentricity along z-axis [$mm$].
        by : MM
            [$b_y$] Dimension of the control perimeter along y-axis [$mm$].
        bz : MM
            [$b_z$] Dimension of the control perimeter along z-axis [$mm$].
        """
        super().__init__()
        self.ey = ey
        self.ez = ez
        self.by = by
        self.bz = bz

    @staticmethod
    def _evaluate(
        ey: MM,
        ez: MM,
        by: MM,
        bz: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(ey=ey, ez=ez)
        raise_if_less_or_equal_to_zero(by=by, bz=bz)

        return 1 + 1.8 * np.sqrt((ey / bz) ** 2 + (ez / by) ** 2)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.43."""
        _equation: str = r"1 + 1.8 \cdot \sqrt{\left(\frac{e_y}{b_z}\right)^2 + \left(\frac{e_z}{b_y}\right)^2}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"e_y": f"{self.ey:.3f}",
                r"e_z": f"{self.ez:.3f}",
                r"b_y": f"{self.by:.3f}",
                r"b_z": f"{self.bz:.3f}",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"\beta",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
