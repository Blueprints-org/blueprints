## Code notes

- Write an equation such as presented in the template. Public docstring on top. Then numpy import. Then project imports. Then classes.
- Keep all formatting and naming conventions such as they are presented in the template. 
- If variable descriptions are given or found, copy precisely and fully from input or Eurocode. 
- Variablenames are always lowercase.
- In the LaTeX formula, edit the return symbol such that it is the left hand side of the equation
- Edit the _equation variable such that it represents the right hand side of the equation
- LaTeX variables should be rounded to 3 decimals.  
- The LaTex _numeric_equation_with_units should include units, except when its dimensionless
- Import the necessary typehinting with type alias units found in type_alias.py and remove the unused imported type aliases. Forces in N, (Bending) moments in Nmm, distances in mm, areas in mm^2, Stress in MPa, angles in DEG, no unit is DIMENSIONLESS. When dealing with angles, use np.deg2rad.
- Test the value of denominators with raise_if_less_or_equal_to_zero. For all others, test with raise_if_negative.

## Template for service

```python
"""Formula 6.41 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, DEG, KG, N, NMM, MM, MM2, MM3, MM4, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot41W1Rectangular(Formula):
    r"""Class representing formula 6.41 for the calculation of [$W_1$]."""

    label = "6.41"
    source_document = EN_1992_1_1_2004

    def __init__(
            self,
            c_1: MM,
            c_2: MM,
            d: MM,
    ) -> None:
        r"""[$W_1$] Calculation of the area [$mm^2$].

        EN 1992-1-1:2004 art.6.4.3(3) - Formula (6.41)

        Parameters
        ----------
        c_1 : MM
            [$c_1$] Column dimension parallel to the eccentricity of the load [$mm$].
        c_2 : MM
            [$c_2$] Column dimension perpendicular to the eccentricity of the load [$mm$].
        d : MM
            [$d$] Mean effective depth of the slab [$mm$].
        """
        super().__init__()
        self.c_1 = c_1
        self.c_2 = c_2
        self.d = d

    @staticmethod
    def _evaluate(
            c_1: MM,
            c_2: MM,
            d: MM,
    ) -> MM2:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(c_1=c_1, c_2=c_2, d=d)

        return (c_1 ** 2) / 2 + c_1 * c_2 + 4 * c_2 * d + 16 * d ** 2 + 2 * np.pi * d * c_1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.41."""
        _equation: str = r"\frac{c_1^2}{2} + c_1 \cdot c_2 + 4 \cdot c_2 \cdot d + 16 \cdot d^2 + 2 \cdot \pi \cdot d \cdot c_1"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"c_1": f"{self.c_1:.{n}f}",
                r"c_2": f"{self.c_2:.{n}f}",
                r"d": f"{self.d:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"c_1": rf"{self.c_1:.3f} \ mm",
                r"c_2": rf"{self.c_2:.3f} \ mm",
                r"d": rf"{self.d:.3f} \ mm",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"W_1",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units
        comparison_operator_label = "=",
        unit = "mm^2",
        )

```