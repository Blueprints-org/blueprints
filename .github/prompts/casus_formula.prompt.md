## Code notes

- Write an equation such as presented in the template. Public docstring on top. Then numpy import. Then project imports. Then classes.
- Make sure the if statements are presented in the LaTeX fully. 
- Keep all formatting and naming conventions such as they are presented in the template. 
- If variable descriptions are given or found, copy precisely and fully from input or Eurocode. 
- Variablenames are always lowercase.
- In the LaTeX formula, edit the return symbol such that it is the left hand side of the equation only
- Edit the _equation variable such that it represents the right hand side of the equation only
- LaTeX variables should be rounded to 3 decimals.  
- The LaTex _numeric_equation_with_units should include units, except when its dimensionless
- Import the necessary typehinting with type alias units found in type_alias.py and remove the unused imported type aliases. Forces in N, (Bending) moments in Nmm, distances in mm, areas in mm^2, Stress in MPa, angles in DEG, no unit is DIMENSIONLESS. When dealing with angles, use np.deg2rad.
- Test the value of denominators with raise_if_less_or_equal_to_zero. For all others, test with raise_if_negative.

## Template for service

```python
"""Formula 6.10a/bN from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, DEG, KG, N, NMM, MM, MM2, MM3, MM4, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot10abNStrengthReductionFactor(Formula):
    r"""Class representing formula 6.10a/bN for the calculation of the strength reduction factor for concrete cracked in shear."""

    label = "6.10a/bN"
    source_document = EN_1992_1_1_2004

    def __init__(
            self,
            f_ck: MPA,
    ) -> None:
        r"""[$\nu_{1}$] Strength reduction factor for concrete cracked in shear [-].

        EN 1992-1-1:2004 art.6.2.2(1) - Formula (6.10.aN and 6.10.bN)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
            f_ck: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ck=f_ck)

        f_ck = 100
        output = 0
        match f_ck:
            case f_ck if f_ck <= 60:
                output = 0.6
            case f_ck if f_ck > 60:
                output = max(0.9 - f_ck / 200, 0.5)

    return output


def latex(self, n: int = 3) -> LatexFormula:
    """Returns LatexFormula object for formula 6.10a/bN."""
    _equation: str = r"\begin{cases} 0.600 & \text{if } f_{ck} \leq 60 \ MPa \\ \max\left(0.9 - \frac{f_{ck}}{200}, 0.5\right) & \text{if } f_{ck} > 60 \ MPa \end{cases}"
    _numeric_equation: str = latex_replace_symbols(
        _equation,
        {
            "f_{ck}": f"{self.f_ck:.{n}f}",
        },
        False,
    )
    _numeric_equation_with_units: str = latex_replace_symbols(
        _equation,
        {
            "f_{ck}": rf"{self.f_ck:.{n}f} \ MPa",
        },
        False,
    )
    return LatexFormula(
        return_symbol=r"\nu_{1}",
        result=f"{self:.{n}f}",
        equation=_equation,
        numeric_equation=_numeric_equation,
        numeric_equation_with_units=_numeric_equation_with_units
    comparison_operator_label = "=",
    unit = "-",
    )

```