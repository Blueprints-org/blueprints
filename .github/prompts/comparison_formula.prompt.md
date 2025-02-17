## Code notes

- Write an equation such as presented in the template. 
- Make sure the script returns a bool. 
- Keep all formatting and naming conventions such as they are presented in the template. 
- If variable descriptions are given or found, copy precisely and fully from input or Eurocode. 
- Variablenames are always lowercase.
- In the LaTeX formula, edit the return symbol such that it is the left hand side of the equation
- Edit the _equation variable such that it represents the right hand side of the equation
- LaTeX variables should be rounded to 3 decimals.  
- Import the necessary typehinting with type alias units found in type_alias.py and remove the unused imported type aliases. Forces in N, (Bending) moments in Nmm, distances in mm, areas in mm^2, Stress in MPa, angles in DEG, no unit is DIMENSIONLESS. When dealing with angles, use np.deg2rad.

## Template for service

```python
"""Formula 5.38a from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, DEG, KG, N, NMM, MM, MM2, MM3, MM4, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot38aCheckRelativeSlendernessRatio(Formula):
    r"""Class representing formula 5.38a for check of relative slenderness ratio."""

    label = "5.38a"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        lambda_y: DIMENSIONLESS,
        lambda_z: DIMENSIONLESS,
    ) -> None:
        r"""Check the ratio of the slenderness in y-direction and z-direction.

        NEN-EN 1992-1-1+C2:2011 art.5.8.XXXXXXX - Formula (5.38a)

        Parameters
        ----------
        lambda_y : DIMENSIONLESS
            [$$\lambda_{y}$$] Slenderness ratio in y-direction [-].
        lambda_z : DIMENSIONLESS
            [$$\lambda_{z}$$] Slenderness ratio in z-direction [$$N$$].
        """
        super().__init__()
        self.lambda_y = lambda_y
        self.lambda_z = lambda_z

    @staticmethod
    def _evaluate(
        lambda_y: DIMENSIONLESS,
        lambda_z: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(lambda_y=lambda_y, lambda_z=lambda_z)

        return (lambda_y / lambda_z <= 2) and (lambda_z / lambda_y <= 2)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.38a."""
        _equation: str = r"\left( \frac{\lambda_{y}}{\lambda_{z}} \leq 2 \text{ and } \frac{\lambda_{z}}{\lambda_{y}} \leq 2 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "lambda_y": f"{self.lambda_y:.3f}",
                "lambda_z": f"{self.lambda_z:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
        
```