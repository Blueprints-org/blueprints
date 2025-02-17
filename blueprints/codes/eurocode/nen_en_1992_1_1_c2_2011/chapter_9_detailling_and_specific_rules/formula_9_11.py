"""Formula 9.11 from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailing and specific rules."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, MM, MM2, MPA
from blueprints.validations import raise_if_greater_than_90, raise_if_less_or_equal_to_zero, raise_if_negative


class Form9Dot11MinimumShearReinforcement(Formula):
    """Class representing the formula 9.11 for the calculation of the minimum shear reinforcement."""

    label = "9.11"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha: DEG,
        s_r: MM,
        s_t: MM,
        f_ck: MPA,
        f_yk: MPA,
    ) -> None:
        r"""[$$A_{sw,min}$$] Minimum shear reinforcement [$$mm^2$$].

        The spirit of the equation is to calculate the shear reinforcement area. The formula is converted such that
        it actully does that, as opposed to the presentation in the Eurocode which only checks if the area is sufficient
        with a boolean result.

        NEN-EN 1992-1-1+C2:2011 art.9.4.3(2) - Formula (9.11)

        Parameters
        ----------
        alpha : DEG
            [$$\alpha$$] Angle between the shear reinforcement and the main steel [$$^\circ$$].
        s_r : MM
            [$$s_r$$] Spacing of shear links in the radial direction [$$mm$$].
        s_t : MM
            [$$s_t$$] Spacing of shear links in the tangential direction [$$mm$$].
        f_ck : MPA
            [$$f_{ck}$$] Characteristic compressive strength of concrete [$$MPa$$].
        f_yk : MPA
            [$$f_{yk}$$] Characteristic yield strength of reinforcement [$$MPa$$].
        """
        super().__init__()
        self.alpha = alpha
        self.s_r = s_r
        self.s_t = s_t
        self.f_ck = f_ck
        self.f_yk = f_yk

    @staticmethod
    def _evaluate(
        alpha: DEG,
        s_r: MM,
        s_t: MM,
        f_ck: MPA,
        f_yk: MPA,
    ) -> MM2:
        """For more detailed documentation see the class docstring."""
        raise_if_less_or_equal_to_zero(s_r=s_r, s_t=s_t, f_yk=f_yk)
        raise_if_negative(alpha=alpha, f_ck=f_ck)
        raise_if_greater_than_90(alpha=alpha)

        alpha_rad = np.deg2rad(alpha)
        lhs = (1.5 * np.sin(alpha_rad) + np.cos(alpha_rad)) / (s_r * s_t)
        rhs = 0.08 * np.sqrt(f_ck) / f_yk

        return rhs / lhs

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 9.11."""
        _equation: str = (
            r"\frac{0.08 \cdot \sqrt{f_{ck}}}{f_{yk}} \cdot \frac{s_r \cdot s_t}{1.5 \cdot "
            r"\sin(\alpha) + \cos(\alpha)}"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\alpha": f"{self.alpha:.3f}",
                "s_r": f"{self.s_r:.3f}",
                "s_t": f"{self.s_t:.3f}",
                "f_{ck}": f"{self.f_ck:.3f}",
                "f_{yk}": f"{self.f_yk:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"A_{sw,min}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm^2",
        )
