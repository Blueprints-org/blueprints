"""Formula 8.45 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import math

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot45StrengthReductionFactor(Formula):
    r"""Class representing formula 8.45 for the strength reduction factor nu based on the state of strains.

    Strength reduction factor nu based on the state of strains of the member according to:
    [$\nu = \frac{1}{1.0 + 110 \cdot (\varepsilon_x + (\varepsilon_x + 0.001) \cdot \cot^2 \theta)} \leq 1.0$]
    """

    label = "8.45"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        epsilon_x: DIMENSIONLESS,
        theta: DEG,
    ) -> None:
        r"""Strength reduction factor nu based on the state of strains of the member.
        The factor may be calculated according to formula (8.45) when the inclination of the compression field is
        lower than theta_min given in 8.2.3 (4) and the ductility class of the reinforcement is B or C.

        prEN 1992-1-1:2023 art. 8.2.3 (7) - Formula (8.45)

        Parameters
        ----------
        epsilon_x : DIMENSIONLESS
            [$\varepsilon_x$] Average strain of the bottom and top chords (dimensionless). The average strain may
            be calculated according to formulae (8.46).
        theta : DEG
            [$\theta$] Angle of the compression field inclination to the member axis [$°$].
        """
        super().__init__()
        self.epsilon_x = epsilon_x
        self.theta = theta

    @staticmethod
    def _evaluate_pt1(
        epsilon_x: DIMENSIONLESS,
        theta: DEG,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates part 1 of the formula, for more information see the __init__ method."""
        raise_if_negative(epsilon_x=epsilon_x)
        raise_if_less_or_equal_to_zero(theta=theta)
        cot_theta = math.cos(math.radians(theta)) / math.sin(math.radians(theta))
        denominator = 1.0 + 110 * (epsilon_x + (epsilon_x + 0.001) * cot_theta**2)
        return 1 / denominator

    @staticmethod
    def _evaluate_pt2(
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates part 2 of the formula, for more information see the __init__ method."""
        return 1.0

    @staticmethod
    def _evaluate(
        epsilon_x: DIMENSIONLESS,
        theta: DEG,
        *_args,
        **_kwargs,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        eval_pt1 = Form8Dot45StrengthReductionFactor._evaluate_pt1(
            epsilon_x=epsilon_x,
            theta=theta,
        )
        eval_pt2 = Form8Dot45StrengthReductionFactor._evaluate_pt2()
        return min(eval_pt1, eval_pt2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.45."""
        cot_theta = math.cos(math.radians(self.theta)) / math.sin(math.radians(self.theta))
        _equation: str = r"\frac{1}{1.0 + 110 \cdot (\varepsilon_x + (\varepsilon_x + 0.001) \cdot \cot^2 \theta)} \leq limit"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\varepsilon_x": f"{self.epsilon_x:.{n}f}",
                r"\cot^2 \theta": f"{cot_theta**2:.{n}f}",
                r"limit": f"{self._evaluate_pt2():.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"\varepsilon_x": f"{self.epsilon_x:.{n}f}",
                r"\cot^2 \theta": f"{cot_theta**2:.{n}f}",
                r"limit": f"{self._evaluate_pt2():.{n}f}",
            },
            False,
        )

        intermediate_result = rf"{self._evaluate_pt1(epsilon_x=self.epsilon_x, theta=self.theta):.{n}f} \leq {self._evaluate_pt2():.{n}f}"
        return LatexFormula(
            return_symbol=r"\nu",
            result=f"{self:.{n}f}",
            intermediate_result=intermediate_result,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"=",
            unit="",
        )
