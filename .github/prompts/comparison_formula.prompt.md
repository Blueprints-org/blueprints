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
"""Formula 5.17 from EN 1993-5:2007: Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1993_5_2007 import EN_1993_5_2007
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot17CompressionCheckZProfilesClass1And2(ComparisonFormula):
    r"""Class representing formula 5.17 for Z-profiles of class 1 and 2: [$\frac{N_{Ed}}{N_{pl,Rd}} \leq 0.1$]."""

    label = "5.17"
    source_document = EN_1993_5_2007

    def __init__(
        self,
        n_ed: KN,
        n_pl_rd: KN,
    ) -> None:
        r"""Compression check for Z-profiles of class 1 and 2.
        Design axial force [$N_{Ed}$] should not exceed 10% of plastic resistance [$N_{pl,Rd}$].

        EN 1993-5:2007 art. 5.2.3 (10) - Formula (5.17)

        Parameters
        ----------
        n_ed : KN
            [$N_{Ed}$] Design value of the compression force [$kN$].
        n_pl_rd : KN
            [$N_{pl,Rd}$] Plastic design resistance of the cross-section [$kN$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_pl_rd = n_pl_rd

    @staticmethod
    def _evaluate_lhs(
        n_ed: KN,
        n_pl_rd: KN,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the left-hand side of the comparison. see __init__ for details."""
        raise_if_less_or_equal_to_zero(n_pl_rd=n_pl_rd)
        return n_ed / n_pl_rd

    @staticmethod
    def _evaluate_rhs(*_, **_kwargs) -> float:
        """Evaluates the right-hand side of the comparison. see __init__ for details."""
        return 0.1

    @property
    def unity_check(self) -> float:
        """Returns the unity check value."""
        return self.lhs

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.17."""
        _equation: str = r"\frac{N_{Ed}}{N_{pl,Rd}} \leq 0.1"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"N_{pl,Rd}": f"{self.n_pl_rd:.{n}f}",
            },
            False,
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ kN",
                r"N_{pl,Rd}": rf"{self.n_pl_rd:.{n}f} \ kN",
            },
            False,
        )
        _intermediate_result: str = rf"\left( {self.unity_check:.{n}f} \leq 0.1 \right)"
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if bool(self) else r"\text{Not OK}",
            intermediate_result=_intermediate_result,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )


```