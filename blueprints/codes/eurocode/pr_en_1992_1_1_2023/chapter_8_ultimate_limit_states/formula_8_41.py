"""Formula 8.41 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import operator
from collections.abc import Callable
from typing import Any

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import DoubleComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot41InclinationCompressionField(DoubleComparisonFormula):
    """Class representing formula 8.41 for checking inclination of the compression field in the web carrying shear."""

    label = "8.41"
    source_document = PR_EN_1992_1_1_2023

    def __init__(self, theta: DEG, theta_min: DEG) -> None:
        r"""Checking inclination of the compression field in the web carrying shear.

        prEN 1992-1-1:2023 art 8.2.3 (4) - Formula (8.41)

        Parameters
        ----------
        theta : DEG
            [$\theta$] Angle compression field [$degrees$].
        theta_min : DEG
            [$\theta_{min}$] Minimum value of angle compression field [$degrees$].
            Minimal inclination of the compression field theta_min for shear reinforcement of ductility class B or C.
            - cot_theta_min = 2.5 (theta = 21.8 deg) for ordinary reinforced members without axial force;
            - cot_theta_min = 3.0 (theta = 18.4) for members subjected to significant axial compressive force (average
              axial compressive stress >= |3 MPa| and provided that the depth of the compression chord x determined
              from a sectional analysis according to 8.1.1 and 8.1.2 is less than 0.25d. Interpolated values between
              2.5 and 3.0 may be adopted for intermediate cases. For very high compressive forces (x > 0.25d), (11)
              can apply;
            - cot_theta_min = 2.5 - 0.1 * N_Ed / |V_Ed| >= 1.0 for members subjected to axial tension.
            For shear reinforcement of ductility class A, cot_theta_min shall be reduced by 20%.
        """
        super().__init__()
        self.theta = theta
        self.theta_min = theta_min

    @classmethod
    def _comparison_operator_lhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the left-hand side or lower bound."""
        return operator.le

    @classmethod
    def _comparison_operator_rhs(cls) -> Callable[[Any, Any], bool]:
        """Comparison operator of the right-hand side or upper bound."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(*_args, **_kwargs) -> float:
        """Evaluates the left-hand side of the double comparison; see __init__ for details."""
        return 1.0

    @staticmethod
    def _evaluate_val(theta: DEG, *_args, **_kwargs) -> float:
        """Evaluates the value part of the double comparison; see __init__ for details."""
        raise_if_less_or_equal_to_zero(theta=theta)
        return cot(theta)

    @staticmethod
    def _evaluate_rhs(theta_min: DEG, *_args, **_kwargs) -> float:
        """Evaluates the right-hand side of the double comparison; see __init__ for details."""
        raise_if_less_or_equal_to_zero(theta_min=theta_min)
        return cot(theta_min)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 8.41."""
        _equation: str = r"1 \le \cot \left( \theta \right) \le \cot \left( \theta_{\min} \right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta ": f"{self.theta:.{n}f} ",
                r"\theta_{\min} ": f"{self.theta_min:.{n}f} ",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta ": rf"{self.theta:.{n}f} ^\circ",
                r"\theta_{\min} ": rf"{self.theta_min:.{n}f} ^\circ",
            },
            unique_symbol_check=False,
        )
        intermediate_result = rf"1 \le {cot(self.theta):.{n}f} \le {cot(self.theta_min):.{n}f}"

        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if bool(self) else r"\text{Not OK}",
            intermediate_result=intermediate_result,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )
