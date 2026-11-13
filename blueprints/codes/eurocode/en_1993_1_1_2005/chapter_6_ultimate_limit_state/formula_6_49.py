"""Formula 6.49 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot49ReductionFactorForBuckling(Formula):
    r"""Class representing formula 6.49 for the calculation of the reduction factor [$\chi$] for the relevant
    buckling mode.
    """

    label = "6.49"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        phi: DIMENSIONLESS,
        lambda_bar: DIMENSIONLESS,
    ) -> None:
        r"""[$\chi$] Reduction factor for the relevant buckling mode, not larger than 1.0 [-].

        EN 1993-1-1:2005 art.6.3.1.2(1) - Formula (6.49)

        Parameters
        ----------
        phi : DIMENSIONLESS
            [$\Phi$] Value to determine the reduction factor [$\chi$], see SubForm6Dot49Phi [-].
        lambda_bar : DIMENSIONLESS
            [$\overline{\lambda}$] Non-dimensional slenderness [-].
        """
        super().__init__()
        self.phi = phi
        self.lambda_bar = lambda_bar

    @staticmethod
    def _evaluate(
        phi: DIMENSIONLESS,
        lambda_bar: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(phi=phi)
        raise_if_negative(lambda_bar=lambda_bar)

        # The term under the square root, which is negative when phi is smaller than lambda_bar
        phi_squared_minus_lambda_bar_squared = phi**2 - lambda_bar**2
        raise_if_negative(phi_squared_minus_lambda_bar_squared=phi_squared_minus_lambda_bar_squared)

        return min(1 / (phi + np.sqrt(phi_squared_minus_lambda_bar_squared)), 1.0)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.49."""
        _equation: str = r"\min\left(\frac{1}{\Phi + \sqrt{\Phi^2 - \overline{\lambda}^2}}, 1.0\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\Phi": f"{self.phi:.{n}f}",
                r"\overline{\lambda}": f"{self.lambda_bar:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\chi",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )


class SubForm6Dot49Phi(Formula):
    r"""Class representing the sub-formula of formula 6.49 for the calculation of [$\Phi$]."""

    label = "6.49"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        alpha: DIMENSIONLESS,
        lambda_bar: DIMENSIONLESS,
    ) -> None:
        r"""[$\Phi$] Value to determine the reduction factor [$\chi$] [-].

        EN 1993-1-1:2005 art.6.3.1.2(1) - Formula (6.49)

        Parameters
        ----------
        alpha : DIMENSIONLESS
            [$\alpha$] Imperfection factor [-].
        lambda_bar : DIMENSIONLESS
            [$\overline{\lambda}$] Non-dimensional slenderness [-].
        """
        super().__init__()
        self.alpha = alpha
        self.lambda_bar = lambda_bar

    @staticmethod
    def _evaluate(
        alpha: DIMENSIONLESS,
        lambda_bar: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(alpha=alpha, lambda_bar=lambda_bar)

        return 0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar**2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the sub-formula of formula 6.49."""
        _equation: str = r"0.5 \cdot \left[1 + \alpha \cdot \left(\overline{\lambda} - 0.2\right) + \overline{\lambda}^2\right]"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\alpha": f"{self.alpha:.{n}f}",
                r"\overline{\lambda}": f"{self.lambda_bar:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\Phi",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
