"""Formula 3.13 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DAYS, DIMENSIONLESS


class Form3Dot13CoefficientTimeAutogeneShrinkage(Formula):
    """Class representing formula 3.13, which calculates the coefficient dependent on time for the autogene shrinkage."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.13"

    def __init__(
        self,
        t: DAYS,
    ) -> None:
        r"""[$\beta_{as}(t)$] Coefficient dependent on time in days for autogene shrinkage [$-$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.13)

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

    def latex(self) -> LatexFormula:
        r"""Returns LatexFormula object for formula 3.13."""
        return LatexFormula(
            return_symbol=r"\beta_{as}(t)",
            result=f"{self:.3f}",
            equation=r"1 - \exp(-0.2 \cdot t^{0.5})",
            numeric_equation=rf"1 - \exp(-0.2 \cdot {self.t:.2f}^{{0.5}})",
            comparison_operator_label="=",
        )
