"""Formula 6.29 from NEN-EN 1993-1-1+A1:2016: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form6Dot29ReducedYieldStrength(Formula):
    r"""Class representing formula 6.29 for the calculation of reduced yield strength."""

    label = "6.29"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        rho: DIMENSIONLESS,
        f_y: MPA,
    ) -> None:
        r"""[$f_{y,red}$] Calculation of reduced yield strength [$MPa$].

        NEN-EN 1993-1-1+A1:2016 art.6.2.8(3) - Formula (6.29)

        Parameters
        ----------
        rho : DIMENSIONLESS
            [$\rho$] Reduction factor for shear force, see equation 6.29rho (dimensionless).
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        """
        super().__init__()
        self.rho = rho
        self.f_y = f_y

    @staticmethod
    def _evaluate(
        rho: DIMENSIONLESS,
        f_y: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        one_minus_rho = 1 - rho
        raise_if_negative(rho=rho, f_y=f_y, one_minus_rho=one_minus_rho)

        return (1 - rho) * f_y

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.29."""
        _equation: str = r"(1 - \rho) \cdot f_y"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\rho": f"{self.rho:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"\rho": rf"{self.rho:.{n}f}",
                r"f_y": rf"{self.f_y:.{n}f} \ MPa",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"f_{y,red}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
