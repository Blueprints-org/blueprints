"""Formula 8.102 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form8Dot102CoefficientAccountingForAxialForcesTwoDirections(Formula):
    r"""Class representing formula 8.102 for the calculation of the coefficient [$k_{pp}$] accounting for axial
    forces, combined as an average geometric value where different axial stresses act in the x- and
    y-directions.
    """

    label = "8.102"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        k_pp_x: DIMENSIONLESS,
        k_pp_y: DIMENSIONLESS,
    ) -> None:
        r"""[$k_{pp}$] Coefficient accounting for the presence of axial forces, combined from the x- and
        y-directions [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.3(4) - Formula (8.102)

        Parameters
        ----------
        k_pp_x : DIMENSIONLESS
            [$k_{pp,x}$] Coefficient accounting for the presence of axial stresses in the x-direction,
            according to Formula (8.99), (8.100) or (8.103) [$-$].
        k_pp_y : DIMENSIONLESS
            [$k_{pp,y}$] Coefficient accounting for the presence of axial stresses in the y-direction,
            according to Formula (8.99), (8.100) or (8.103) [$-$].
        """
        super().__init__()
        self.k_pp_x = k_pp_x
        self.k_pp_y = k_pp_y

    @staticmethod
    def _evaluate(
        k_pp_x: DIMENSIONLESS,
        k_pp_y: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(k_pp_x=k_pp_x, k_pp_y=k_pp_y)

        return np.sqrt(k_pp_x * k_pp_y)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.102."""
        _equation: str = r"\sqrt{k_{pp,x} \cdot k_{pp,y}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"k_{pp,x}": f"{self.k_pp_x:.{n}f}",
                r"k_{pp,y}": f"{self.k_pp_y:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"k_{pp,x}": f"{self.k_pp_x:.{n}f}",
                r"k_{pp,y}": f"{self.k_pp_y:.{n}f}",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"k_{pp}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
