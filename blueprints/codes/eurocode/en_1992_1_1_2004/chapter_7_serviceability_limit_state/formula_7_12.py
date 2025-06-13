"""Formula 7.12 from EN 1992-1-1:2004: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_negative


class Form7Dot12EquivalentDiameter(Formula):
    r"""Class representing formula 7.12 for the calculation of [$⌀_{eq}$]."""

    label = "7.12"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        n_1: DIMENSIONLESS,
        diam_1: MM,
        n_2: DIMENSIONLESS,
        diam_2: MM,
    ) -> None:
        r"""[$⌀_{eq}$] Calculation of the equivalent diameter [$mm$].

        EN 1992-1-1:2004 art.7.3.4(3) - Formula (7.12)

        Parameters
        ----------
        n_1 : DIMENSIONLESS
            [$n_1$] Number of bars with diameter $⌀_1$.
        diam_1 : MM
            [$⌀_1$] Diameter of the first set of bars [$mm$].
        n_2 : DIMENSIONLESS
            [$n_2$] Number of bars with diameter $⌀_2$.
        diam_2 : MM
            [$⌀_2$] Diameter of the second set of bars [$mm$].
        """
        super().__init__()
        self.n_1 = n_1
        self.diam_1 = diam_1
        self.n_2 = n_2
        self.diam_2 = diam_2

    @staticmethod
    def _evaluate(
        n_1: DIMENSIONLESS,
        diam_1: MM,
        n_2: DIMENSIONLESS,
        diam_2: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(n_1=n_1, diam_1=diam_1, n_2=n_2, diam_2=diam_2)

        return (n_1 * diam_1**2 + n_2 * diam_2**2) / (n_1 * diam_1 + n_2 * diam_2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.12."""
        _equation: str = r"\frac{n_1 \cdot ⌀_1^2 + n_2 \cdot ⌀_2^2}{n_1 \cdot ⌀_1 + n_2 \cdot ⌀_2}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"n_1": f"{self.n_1:.{n}f}",
                r"⌀_1": f"{self.diam_1:.{n}f}",
                r"n_2": f"{self.n_2:.{n}f}",
                r"⌀_2": f"{self.diam_2:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"⌀_{eq}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm",
        )
