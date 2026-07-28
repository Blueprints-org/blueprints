"""Formula 8.26 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, N_MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot26AngleBetweenPrincipalShearForceAndXAxis(Formula):
    """Class representing formula 8.26 for the calculation of the angle between the principal shear force
    and the x-axis in planar members.
    """

    label = "8.26"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, v_ed_x: N_MM, v_ed_y: N_MM) -> None:
        r"""[$\alpha_v$] Angle between the principal shear force and the x-axis [$degrees$].

        FprEN 1992-1-1:2023 (E) art 8.2.1 (5) - Formula (8.26)

        Both components are taken as magnitudes, consistent with Formulas (8.21) to (8.24), which use the same
        two quantities. The result therefore lies between 0 and 90 degrees. The standard gives no rule for
        [$v_{Ed,x} = 0$], for which the ratio is undefined, so that input is rejected.

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
    def _evaluate(v_ed_x: N_MM, v_ed_y: N_MM) -> DEG:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed_y=v_ed_y)
        raise_if_less_or_equal_to_zero(v_ed_x=v_ed_x)

        return np.rad2deg(np.arctan(v_ed_y / v_ed_x))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.26."""
        _equation: str = r"\arctan\left(\frac{v_{Ed,y}}{v_{Ed,x}}\right)"
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
            return_symbol=r"\alpha_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="degrees",
        )
