## Code notes

- Write an equation such as presented in the template. Public docstring on top. Then numpy import. Then project imports. Then classes.
- Make sure the script returns a bool. 
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
"""Formula 5.38a from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, DEG, KG, N, NMM, MM, MM2, MM3, MM4, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot38aCheckRelativeLengthRatio(Formula):
    r"""Class representing formula 5.38a for check of length ratio."""

    label = "5.38a"
    source_document = EN_1992_1_1_2004

    def __init__(
            self,
            length_y: MM,
            length_z: MM,
    ) -> None:
        r"""Check the ratio of the length in y-direction and z-direction.

        EN 1992-1-1:2004 art.5.8.XXXXXXX - Formula (5.38a)

        Parameters
        ----------
        length_y : MM
            [$L_{y}$] Length in y-direction [$mm$].
        length_z : MM
            [$L_{z}$] Length in z-direction [$mm$].
        """
        super().__init__()
        self.length_y = length_y
        self.length_z = length_z

    @staticmethod
    def _evaluate(
            length_y: MM,
            length_z: MM,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(length_y=length_y, length_z=length_z)

        return (length_y / length_z <= 2) and (length_z / length_y <= 2)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.38a."""
        _equation: str = r"\left( \frac{L_{y}}{L_{z}} \leq 2 \text{ and } \frac{L_{z}}{L_{y}} \leq 2 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "length_y": f"{self.length_y:.3f}",
                "length_z": f"{self.length_z:.3f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "length_y": rf"{self.length_y:.3f} \ mm",
                "length_z": rf"{self.length_z:.3f} \ mm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units
        comparison_operator_label = "\\to",
        unit = "",
        )

```