"""Formula 8.27 from EN 1993-1-1:2022: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.en_1993_1_1_2022 import EN_1993_1_1_2022
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot27CheckShearBucklingResistance(ComparisonFormula):
    r"""Class representing formula 8.27 for checking shear buckling resistance for webs without intermediate stiffeners."""

    label = "8.27"
    source_document = EN_1993_1_1_2022

    def __init__(
        self,
        h_w: MM,
        t_w: MM,
        epsilon: DIMENSIONLESS,
        eta: DIMENSIONLESS = 1.0,
    ) -> None:
        r"""Check the shear buckling resistance for webs without intermediate stiffeners.

        EN 1993-1-1:2022 art.8.2.6(6) - Formula (8.27)

        Parameters
        ----------
        h_w : MM
            [$h_{w}$] Web height [mm].
        t_w : MM
            [$t_{w}$] Web thickness [mm].
        epsilon : DIMENSIONLESS
            [$\epsilon$] Coefficient depending on $f_y$ [-].
        eta : DIMENSIONLESS, optional
            [$\eta$] See section 5 of EN 1993-1-5, conservatively taken as 1.0 [-].
        """
        super().__init__()
        self.h_w = h_w
        self.t_w = t_w
        self.epsilon = epsilon
        self.eta = eta

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.gt

    @staticmethod
    def _evaluate_lhs(
        h_w: MM,
        t_w: MM,
        epsilon: DIMENSIONLESS,
        eta: DIMENSIONLESS,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the left-hand side of the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(t_w=t_w, eta=eta)
        raise_if_negative(h_w=h_w, epsilon=epsilon)

        return h_w / t_w

    @staticmethod
    def _evaluate_rhs(
        epsilon: DIMENSIONLESS,
        eta: DIMENSIONLESS,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the right-hand side of the formula, for more information see the __init__ method."""
        return 72 * (epsilon / eta)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.27."""
        _equation: str = r"\frac{h_w}{t_w} > 72 \cdot \frac{\epsilon}{\eta}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"h_w": f"{self.h_w:.{n}f}",
                r"t_w": f"{self.t_w:.{n}f}",
                r"\epsilon": f"{self.epsilon:.{n}f}",
                r"\eta": f"{self.eta:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"h_w": rf"{self.h_w:.{n}f} \ mm",
                r"t_w": rf"{self.t_w:.{n}f} \ mm",
                r"\epsilon": f"{self.epsilon:.{n}f}",
                r"\eta": f"{self.eta:.{n}f}",
            },
            False,
        )
        _intermediate_result: str = rf"\left( {self.lhs:.{n}f} > {self.rhs:.{n}f} \right)"
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if bool(self) else r"\text{Not OK}",
            intermediate_result=_intermediate_result,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )
