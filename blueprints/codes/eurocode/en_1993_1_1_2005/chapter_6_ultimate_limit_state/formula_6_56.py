"""Formula 6.56 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM3, MPA, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot56NonDimensionalSlendernessLT(Formula):
    r"""Class representing formula 6.56 for the calculation of [$\overline{\lambda}_{LT}$]."""

    label = "6.56"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        w_y: MM3,
        f_y: MPA,
        m_cr: NMM,
    ) -> None:
        r"""[$\overline{\lambda}_{LT}$] Non-dimensional slenderness for lateral-torsional buckling [-].

        EN 1993-1-1:2005 art.6.3.2.2(1) - Formula (6.56)

        Parameters
        ----------
        w_y : MM3
            [$W_y$] Section modulus [$mm^3$].
        f_y : MPA
            [$f_y$] Yield strength [$MPa$].
        m_cr : NMM
            [$M_{cr}$] Elastic critical moment for lateral-torsional buckling [$Nmm$].
        """
        super().__init__()
        self.w_y = w_y
        self.f_y = f_y
        self.m_cr = m_cr

    @staticmethod
    def _evaluate(
        w_y: MM3,
        f_y: MPA,
        m_cr: NMM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(w_y=w_y, f_y=f_y)
        raise_if_less_or_equal_to_zero(m_cr=m_cr)

        return np.sqrt((w_y * f_y) / m_cr)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.56."""
        _equation: str = r"\sqrt{\frac{W_y \cdot f_y}{M_{cr}}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"W_y": f"{self.w_y:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"M_{cr}": f"{self.m_cr:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"W_y": rf"{self.w_y:.{n}f} \ mm^3",
                r"f_y": rf"{self.f_y:.{n}f} \ MPa",
                r"M_{cr}": rf"{self.m_cr:.{n}f} \ Nmm",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"\overline{\lambda}_{LT}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="",
        )


class Form6Dot56LateralTorsionalIntermediateFactor(Formula):
    r"""Class representing formula 6.56 for the calculation of [$\Phi_{LT}$]."""

    label = "6.56"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        alpha_lt: DIMENSIONLESS,
        lambda_bar_lt: DIMENSIONLESS,
    ) -> None:
        r"""[$\Phi_{LT}$] Intermediate factor for lateral-torsional buckling [-].

        EN 1993-1-1:2005 art.6.3.2.2(1) - Formula (6.56)

        Parameters
        ----------
        alpha_lt : DIMENSIONLESS
            [$\alpha_{LT}$] Imperfection factor [-].
        lambda_bar_lt : DIMENSIONLESS
            [$\overline{\lambda}_{LT}$] Non-dimensional slenderness for lateral-torsional buckling [-].
        """
        super().__init__()
        self.alpha_lt = alpha_lt
        self.lambda_bar_lt = lambda_bar_lt

    @staticmethod
    def _evaluate(
        alpha_lt: DIMENSIONLESS,
        lambda_bar_lt: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(alpha_lt=alpha_lt, lambda_bar_lt=lambda_bar_lt)

        return 0.5 * (1 + alpha_lt * (lambda_bar_lt - 0.2) + lambda_bar_lt**2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.56."""
        _equation: str = r"0.5 \cdot \left[ 1 + \alpha_{LT} \cdot \left( \overline{\lambda}_{LT} - 0.2 \right) + \overline{\lambda}_{LT}^2 \right]"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\alpha_{LT}": f"{self.alpha_lt:.{n}f}",
                r"\overline{\lambda}_{LT}": f"{self.lambda_bar_lt:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = _numeric_equation
        return LatexFormula(
            return_symbol=r"\Phi_{LT}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="",
        )


class Form6Dot56ReductionFactorLateralTorsionalBuckling(Formula):
    r"""Class representing formula 6.56 for the calculation of [$\chi_{LT}$]."""

    label = "6.56"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        phi_lt: DIMENSIONLESS,
        lambda_bar_lt: DIMENSIONLESS,
    ) -> None:
        r"""[$\chi_{LT}$] Reduction factor for lateral-torsional buckling [-].

        EN 1993-1-1:2005 art.6.3.2.2(1) - Formula (6.56)

        Parameters
        ----------
        phi_lt : DIMENSIONLESS
            [$\Phi_{LT}$] Intermediate factor for lateral-torsional buckling [-].
        lambda_bar_lt : DIMENSIONLESS
            [$\overline{\lambda}_{LT}$] Non-dimensional slenderness for lateral-torsional buckling [-].
        """
        super().__init__()
        self.phi_lt = phi_lt
        self.lambda_bar_lt = lambda_bar_lt

    @staticmethod
    def _evaluate(
        phi_lt: DIMENSIONLESS,
        lambda_bar_lt: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(lambda_bar_lt=lambda_bar_lt)
        raise_if_less_or_equal_to_zero(phi_lt=phi_lt)

        under_sqrt = phi_lt**2 - lambda_bar_lt**2
        if under_sqrt < 0:
            raise_if_negative(under_sqrt=under_sqrt)  # This will raise an error if the value under the square root is negative

        chi_lt = 1 / (phi_lt + np.sqrt(phi_lt**2 - lambda_bar_lt**2))
        return min(1.0, chi_lt)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.56."""
        _equation: str = r"\frac{1}{\Phi_{LT} + \sqrt{\Phi_{LT}^2 - \overline{\lambda}_{LT}^2}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\Phi_{LT}": f"{self.phi_lt:.{n}f}",
                r"\overline{\lambda}_{LT}": f"{self.lambda_bar_lt:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = _numeric_equation
        return LatexFormula(
            return_symbol=r"\chi_{LT}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="",
        )
