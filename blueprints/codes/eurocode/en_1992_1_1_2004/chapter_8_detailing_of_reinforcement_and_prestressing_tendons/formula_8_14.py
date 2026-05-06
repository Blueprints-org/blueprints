"""Formula 8.14 from EN 1992-1-1:2004: Chapter 8: Detailing of reinforcement and prestressing tendons."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_negative


class Form8Dot14EquivalentDiameterBundledBars(Formula):
    """Class representing formula 8.14 for the calculation of the equivalent diameter of bundled bars, [$Ø_{n}$]."""

    label = "8.14"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        diameter: MM,
        n_b: DIMENSIONLESS,
    ) -> None:
        r"""[$Ø_{n}$] Equivalent diameter of bundled bars [$mm$].

        EN 1992-1-1:2004 art.8.9.1(2) - Formula (8.14)

        Parameters
        ----------
        diameter : MM
            [$Ø$] Diameter of the bars [$mm$]
        n_b : DIMENSIONLESS
            [$n_{b}$] Number of bars in the bundle [$-$].

            ≤ 4 for vertical bars in compression and for bars in a lapped joint.

            ≤ 3 for all other cases.
        """
        super().__init__()
        self.diameter = diameter
        self.n_b = n_b

    @staticmethod
    def _evaluate(diameter: MM, n_b: DIMENSIONLESS) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            diameter=diameter,
            n_b=n_b,
        )
        return min(diameter * np.sqrt(n_b), 55)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 8.14."""
        _equation: str = r"\min \left(55 \ \text{mm}, Ø \cdot \sqrt{n_b} \right)"
        _equation_no_unit: str = r"\min \left(55, Ø \cdot \sqrt{n_b} \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation_no_unit,
            {
                r"Ø": f"{self.diameter:.{n}f}",
                r"n_b": f"{self.n_b:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"Ø": rf"{self.diameter:.{n}f} \ mm",
                r"n_b": f"{self.n_b:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"Ø_n",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )

