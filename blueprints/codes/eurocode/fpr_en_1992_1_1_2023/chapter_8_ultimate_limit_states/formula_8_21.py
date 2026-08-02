"""Formula 8.21 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import N_MM


class Form8Dot21DesignShearForcePerUnitWidth(Formula):
    """Class representing formula 8.21 for the calculation of the design shear force per unit width in planar members
    with out-of-plane shear forces acting in two directions.
    """

    label = "8.21"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, v_ed_x: N_MM, v_ed_y: N_MM) -> None:
        r"""[$v_{Ed}$] Design shear force per unit width in planar members [$N/mm$].

        FprEN 1992-1-1:2023 (E) art 8.2.1 (5) - Formula (8.21)

        Both components enter squared, so the sign of either of them does not reach the result. They are
        components of a shear force vector and the standard places no restriction on their sign, so a negative
        one is accepted and gives the same result as its positive counterpart.

        Parameters
        ----------
        v_ed_x : N_MM
            [$v_{Ed,x}$] Out-of-plane design shear force per unit width acting on the cross-section perpendicular
            to the x direction [$N/mm$].
        v_ed_y : N_MM
            [$v_{Ed,y}$] Out-of-plane design shear force per unit width acting on the cross-section perpendicular
            to the y direction [$N/mm$].
        """
        super().__init__()
        self.v_ed_x = v_ed_x
        self.v_ed_y = v_ed_y

    @staticmethod
    def _evaluate(v_ed_x: N_MM, v_ed_y: N_MM) -> N_MM:
        """Evaluates the formula, for more information see the __init__ method."""
        return float(np.sqrt(v_ed_x**2 + v_ed_y**2))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.21."""
        _equation: str = r"\sqrt{\left(v_{Ed,x}\right)^2 + \left(v_{Ed,y}\right)^2}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"v_{Ed,x}": f"{self.v_ed_x:.{n}f}",
                r"v_{Ed,y}": f"{self.v_ed_y:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"v_{Ed,x}": rf"{self.v_ed_x:.{n}f} \ N/mm",
                r"v_{Ed,y}": rf"{self.v_ed_y:.{n}f} \ N/mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"v_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N/mm",
        )
