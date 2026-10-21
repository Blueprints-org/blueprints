"""Formula 8.121 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form8Dot121StrengthReductionFactorCrackedZone(Formula):
    """Class representing formula 8.121 for the calculation of the strength reduction factor for compression
    fields in cracked zones, based on the principal tensile strain.
    """

    label = "8.121"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        epsilon_1: DIMENSIONLESS,
    ) -> None:
        r"""[$\nu$] Strength reduction factor for compression fields in cracked zones [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.5.2(5) - Formula (8.121)

        The standard bounds this expression from above by 1,0. For [$\varepsilon_1 \geq 0$] the expression
        never exceeds 1,0, so the bound is always met and is not repeated here.

        Parameters
        ----------
        epsilon_1 : DIMENSIONLESS
            [$\varepsilon_1$] Value of the maximum principal tensile strain [$-$].
        """
        super().__init__()
        self.epsilon_1 = epsilon_1

    @staticmethod
    def _evaluate(
        epsilon_1: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(epsilon_1=epsilon_1)

        return 1 / (1.0 + 110 * epsilon_1)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.121."""
        _equation: str = r"\frac{1}{1.0 + 110 \cdot \varepsilon_1}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\varepsilon_1": f"{self.epsilon_1:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = _numeric_equation
        return LatexFormula(
            return_symbol=r"\nu",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
