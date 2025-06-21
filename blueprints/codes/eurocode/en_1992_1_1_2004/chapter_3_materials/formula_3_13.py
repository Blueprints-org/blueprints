"""Formula 3.13 from EN 1992-1-1:2004: Chapter 3 - Materials."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DAYS, DIMENSIONLESS


class Form3Dot13CoefficientTimeAutogeneShrinkage(Formula):
    """Class representing formula 3.13, which calculates the coefficient dependent on time for the autogene shrinkage."""

    source_document = EN_1992_1_1_2004
    label = "3.13"

    def __init__(
        self,
        t: DAYS,
    ) -> None:
        r"""[$\beta_{as}(t)$] Coefficient dependent on time in days for autogene shrinkage [$-$].

        EN 1992-1-1:2004 art.3.1.4(6) - Formula (3.13)

        Parameters
        ----------
        t : DAYS
            [$t$] Time in days [$days$].

        Returns
        -------
        None
        """
        super().__init__()
        self.t = t

    @staticmethod
    def _evaluate(
        t: DAYS,
    ) -> DIMENSIONLESS:
        r"""Evaluates the formula, for more information see the __init__ method."""
        if t < 0:
            raise ValueError(f"Invalid t: {t}. t cannot be negative")
        return 1 - np.exp(-0.2 * t**0.5)

    def latex(self, n: int = 2) -> LatexFormula:
        r"""Returns LatexFormula object for formula 3.13."""
        return LatexFormula(
            return_symbol=r"\beta_{as}(t)",
            result=f"{self:.{n}f}",
            equation=r"1 - \exp(-0.2 \cdot t^{0.5})",
            numeric_equation=rf"1 - \exp(-0.2 \cdot {self.t:.{n}f}^{{0.5}})",
            comparison_operator_label="=",
        )
