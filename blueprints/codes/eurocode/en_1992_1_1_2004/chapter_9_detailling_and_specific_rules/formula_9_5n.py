"""Formula 9.5N from EN 1992-1-1:2004: Chapter 9 - Detailing of members and particular rules."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form9Dot5nMinimumShearReinforcementRatio(Formula):
    """Class representing the formula 9.5N for the calculation of the minimum shear reinforcement ratio for beams."""

    label = "9.5N"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_ck: MPA,
        f_yk: MPA,
    ) -> None:
        r"""[$\rho_{w,min}$] Minimum shear reinforcement ratio for beams [$-$].

        EN 1992-1-1:2004 art.9.2.2(5) - Formula (9.5N)

        Parameters
        ----------
        f_ck: MPA
            [$f_{ck}$] Characteristic concrete compressive cylinder strength at 28 days [$MPa$].
        f_yk: MPA
            [$f_{yk}$] Characteristic yield strength reinforcement steel [$MPa$].
        """
        super().__init__()
        self.f_ck = f_ck
        self.f_yk = f_yk

    @staticmethod
    def _evaluate(f_ck: MPA, f_yk: MPA) -> DIMENSIONLESS:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(f_ck=f_ck, f_yk=f_yk)
        return (0.08 * np.sqrt(f_ck)) / f_yk

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 9.5N."""
        return LatexFormula(
            return_symbol=r"\rho_{w,min}",
            result=f"{self:.6f}",
            equation=r"\left( 0.08 \cdot \sqrt{f_{ck}} \right) / f_{yk}",
            numeric_equation=rf"\left( 0.08 \cdot \sqrt{{{self.f_ck:.{n}f}}} \right) / {self.f_yk:.{n}f}",
            comparison_operator_label="=",
        )
