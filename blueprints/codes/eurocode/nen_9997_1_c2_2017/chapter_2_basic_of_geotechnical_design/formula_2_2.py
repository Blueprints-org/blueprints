"""Formula 2.2 from NEN 9997-1+C2:2017: Chapter 2: Basis of geotechnical design."""

from blueprints.codes.eurocode.nen_9997_1_c2_2017 import NEN_9997_1_C2_2017
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form2Dot2DesignValueGeotechnicalParameter(Formula):
    """Class representing formula 2.2 for the calculation of the design value [$X_d$] of geotechnical parameter [$X$]."""

    label = "2.2"
    source_document = NEN_9997_1_C2_2017

    def __init__(self, x_k: DIMENSIONLESS, gamma_m: DIMENSIONLESS) -> None:
        r"""[$X_d$] Design value of geotechnical parameter [$X$].

        NEN 9997-1+C2:2017 art.2.4.6.2(1) - Formula (2.2)

        Parameters
        ----------
        x_k : DIMENSIONLESS
            [$X_{k}$] Characteristic value of geotechnical parameter [$X$].
        gamma_m : DIMENSIONLESS
            [$\gamma_M$] material partial factor [$-$].
        """
        super().__init__()
        self.x_k = x_k
        self.gamma_m = gamma_m

    @staticmethod
    def _evaluate(
        x_k: DIMENSIONLESS,
        gamma_m: DIMENSIONLESS,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m=gamma_m)
        return x_k / gamma_m

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 2.2."""
        numerator = f"{self.x_k:.3f}"
        denominator = f"{self.gamma_m:.3f}"
        return LatexFormula(
            return_symbol="X_d",
            result=f"{self:.3f}",
            equation=r"\frac{X_{k}}{\gamma_M}",
            numeric_equation=f"{latex_fraction(numerator=numerator, denominator=denominator)}",
            comparison_operator_label="=",
        )
