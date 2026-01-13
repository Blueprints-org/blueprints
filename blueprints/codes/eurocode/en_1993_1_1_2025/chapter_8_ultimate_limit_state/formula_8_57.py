"""Formula 8.57 from EN 1993-1-1:2025: Chapter 8 - Ultimate limit state."""

import operator
from collections.abc import Callable
from typing import Any

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot57LongitudinalStressClass3CrossSections(ComparisonFormula):
    r"""Class representing formula 8.57 for Class 3 cross-sections: [$\sigma_{x,Ed} \leq \frac{f_y}{\gamma_{M0}}$]."""

    label = "8.57"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        sigma_x_ed: MPA,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""Longitudinal stress check for Class 3 cross-sections in the absence of shear force.
        The maximum longitudinal stress [$\sigma_{x,Ed}$] should not exceed the yield strength
        divided by the partial safety factor [$\frac{f_y}{\gamma_{M0}}$].

        EN 1993-1-1:2025 art. 8.2.9.2(1) - Formula (8.57)

        Parameters
        ----------
        sigma_x_ed : MPA
            [$\sigma_{x,Ed}$] Design value of the local longitudinal stress due to moment and axial force
            taking account of fastener holes where relevant [$MPa$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for resistance of cross-sections [-].
        """
        super().__init__()
        self.sigma_x_ed = sigma_x_ed
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @classmethod
    def _comparison_operator(cls) -> Callable[[Any, Any], bool]:
        """Returns the comparison operator for this formula.
        LHS should be less than or equal to RHS.
        """
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        sigma_x_ed: MPA,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the left-hand side of the comparison. see __init__ for details."""
        raise_if_negative(sigma_x_ed=sigma_x_ed)
        return sigma_x_ed

    @staticmethod
    def _evaluate_rhs(
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the right-hand side of the comparison. see __init__ for details."""
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0)
        raise_if_negative(f_y=f_y)
        return f_y / gamma_m0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.57."""
        _equation: str = r"\sigma_{x,Ed} \leq \frac{f_y}{\gamma_{M0}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\sigma_{x,Ed}": f"{self.sigma_x_ed:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"\sigma_{x,Ed}": rf"{self.sigma_x_ed:.{n}f} \ MPa",
                r"f_y": rf"{self.f_y:.{n}f} \ MPa",
                r"\gamma_{M0}": rf"{self.gamma_m0:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if bool(self) else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit=r"",
        )
