"""Formula 8.18 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.pr_en_1992_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, N
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot50AdditionalTensileForceDueToShear(Formula):
    """Class representing formula 8.50 for the calculation of the additional tensile force due to shear."""

    label = "8.50"
    source_document = PR_EN_1992_1_1_2023

    def __init__(self, v_ed: N, theta: DEG) -> None:
        r"""[$\N_{Vd}$] Additional tensile force due to shear [$N$].

        prEN 1992-1-1:2023 art 8.2.3 (8) - Formula (8.50)

        Parameters
        ----------
        v_ed : N
            [$V_{Ed}$] Design shear force
        theta : MM
            [$\theta$] Angle of the compression strut with the longitudinal axis of the member
        """
        super().__init__()
        self.v_ed = v_ed
        self.theta = theta

    @staticmethod
    def _evaluate(v_ed: N, theta: DEG) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed=v_ed)
        raise_if_less_or_equal_to_zero(theta=theta)
        return abs(v_ed) * cot(x=theta)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.50."""
        _equation: str = r"|V_{Ed}| \cdot \cot\theta"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={r"V_{Ed}": f"{self.v_ed:.{n}f}", r"\theta": f"{self.theta:.{n}f}"},
            unique_symbol_check=False,
        )

        return LatexFormula(
            return_symbol=r"N_{Vd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
