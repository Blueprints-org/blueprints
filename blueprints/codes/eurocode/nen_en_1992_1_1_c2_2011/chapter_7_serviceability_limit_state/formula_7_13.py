"""Formula 7.13 from NEN-EN 1992-1-1+C2:2011: Chapter 7 - Serviceability limit state (SLS)."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot13CoefficientK2(Formula):
    r"""Class representing formula 7.13 for the calculation of [$k_2$]."""

    label = "7.13"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, epsilon_1: DIMENSIONLESS, epsilon_2: DIMENSIONLESS) -> None:
        r"""[$k_2$] Calculation of the coefficient for distribution of strain [$-$].

        NEN-EN 1992-1-1+C2:2011 art.7.3.4(3) - Formula (7.13)

        Parameters
        ----------
        epsilon_1 : DIMENSIONLESS
            [$\epsilon_1$] Greater tensile strain at the boundaries of the section considered [$-$].
        epsilon_2 : DIMENSIONLESS
            [$\epsilon_2$] Lesser tensile strain at the boundaries of the section considered [$-$].
        """
        super().__init__()
        self.epsilon_1 = epsilon_1
        self.epsilon_2 = epsilon_2

    @staticmethod
    def _evaluate(epsilon_1: DIMENSIONLESS, epsilon_2: DIMENSIONLESS) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(epsilon_1=epsilon_1)
        raise_if_negative(epsilon_2=epsilon_2)

        return (epsilon_1 + epsilon_2) / (2 * epsilon_1)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 7.13."""
        _equation: str = r"\frac{\epsilon_1 + \epsilon_2}{2 \cdot \epsilon_1}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\epsilon_1": f"{self.epsilon_1:.3f}",
                r"\epsilon_2": f"{self.epsilon_2:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"k_2",
            result=f"{self._evaluate(self.epsilon_1, self.epsilon_2):.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
