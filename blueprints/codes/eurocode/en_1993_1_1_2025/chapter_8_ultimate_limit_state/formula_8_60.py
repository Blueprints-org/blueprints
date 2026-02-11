"""Formula 8.60 from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot60ReducedYieldStrength(Formula):
    r"""Class representing formula 8.60 for the calculation of reduced yield strength for the shear area."""

    label = "8.60"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        rho: DIMENSIONLESS,
        f_y: MPA,
    ) -> None:
        r"""Reduced yield strength calculation for the shear area when shear force exceeds 50% of plastic shear resistance [$MPa$].

        EN 1993-1-1:2025 art.8.2.10(3) - Formula (8.60)

        Parameters
        ----------
        rho : DIMENSIONLESS
            [$\rho$] Factor where $\rho = (2V_{Ed} / V_{pl,Rd}-1)^2$ and $V_{pl,Rd}$ is obtained from 6.2.6(2) [-].
        f_y : MPA
            [$f_y$] Yield strength [$MPa$].
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
        raise_if_negative(rho=rho, f_y=f_y)

        return (1 - rho) * f_y

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.60."""
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
                r"\rho": f"{self.rho:.{n}f}",
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
