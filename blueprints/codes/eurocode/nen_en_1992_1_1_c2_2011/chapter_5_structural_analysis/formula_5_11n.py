"""Formula 5.11N from NEN-EN 1992-1-1 C2:2011: Chapter 5 Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot11nShearSlendernessCorrectionFactor(Formula):
    """Class representing formula 5.11N for the calculation of the shear slenderness correction factor [$k_{λ}$]."""

    label = "5.11N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        lambda_factor: DIMENSIONLESS,
    ) -> None:
        r"""[$k_{λ}$] Shear slenderness correction factor.

        NEN-EN 1992-1-1+C2:2011 art.5.6.3(4) - Formula (5.11N)

        Parameters
        ----------
        lambda_factor : DIMENSIONLESS
            [$λ$] ratio of the distance between point of zero and maximum moment after redistribution and
        effective depth, d [$-$]

        Use your own implementation for this value or use :class:`Form5Dot12nRatioDistancePointZeroAndMaxMoment`.
        """
        super().__init__()
        self.lambda_factor = lambda_factor

    @staticmethod
    def _evaluate(
        lambda_factor: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(lambda_factor=lambda_factor)
        return (lambda_factor / 3) ** 0.5

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.11N."""
        return LatexFormula(
            return_symbol=r"k_{λ}",
            result=f"{self:.3f}",
            equation=r"\sqrt{\frac{λ}{3}}",
            numeric_equation=rf"\sqrt{latex_fraction(numerator=self.lambda_factor, denominator=3)}",
            comparison_operator_label="=",
        )
