"""Formula 8.95 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form8Dot95LongitudinalReinforcementRatioPunchingShear(Formula):
    r"""Class representing formula 8.95 for the calculation of the longitudinal reinforcement ratio at a
    punching shear control perimeter, combined from the two reinforcement directions.
    """

    label = "8.95"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        rho_l_x: DIMENSIONLESS,
        rho_l_y: DIMENSIONLESS,
    ) -> None:
        r"""[$\rho_l$] Longitudinal reinforcement ratio at the control perimeter [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.3(1) - Formula (8.95)

        Parameters
        ----------
        rho_l_x : DIMENSIONLESS
            [$\rho_{l,x}$] Reinforcement ratio of bonded flexural reinforcement in the x-direction. The value
            should be calculated as a mean value over the width [$b_s$] defined in Figure 8.22. Reinforcement
            that does not extend at least [$2,5 d_v + 20 \phi$] beyond the control perimeter [$b_{0,5}$] or
            [$20 \phi$] beyond the line of contraflexure should not be considered [$-$].
        rho_l_y : DIMENSIONLESS
            [$\rho_{l,y}$] Reinforcement ratio of bonded flexural reinforcement in the y-direction. The value
            should be calculated as a mean value over the width [$b_s$] defined in Figure 8.22. Reinforcement
            that does not extend at least [$2,5 d_v + 20 \phi$] beyond the control perimeter [$b_{0,5}$] or
            [$20 \phi$] beyond the line of contraflexure should not be considered [$-$].
        """
        super().__init__()
        self.rho_l_x = rho_l_x
        self.rho_l_y = rho_l_y

    @staticmethod
    def _evaluate(
        rho_l_x: DIMENSIONLESS,
        rho_l_y: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(rho_l_x=rho_l_x, rho_l_y=rho_l_y)

        return np.sqrt(rho_l_x * rho_l_y)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.95."""
        _equation: str = r"\sqrt{\rho_{l,x} \cdot \rho_{l,y}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\rho_{l,x}": f"{self.rho_l_x:.{n}f}",
                r"\rho_{l,y}": f"{self.rho_l_y:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\rho_{l,x}": f"{self.rho_l_x:.{n}f}",
                r"\rho_{l,y}": f"{self.rho_l_y:.{n}f}",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\rho_l",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
