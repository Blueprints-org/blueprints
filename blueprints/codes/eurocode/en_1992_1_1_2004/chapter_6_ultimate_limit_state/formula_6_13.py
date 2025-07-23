"""Formula 6.13 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.math_helpers import cot
from blueprints.type_alias import DEG, MM, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot13ShearResistanceInclinedReinforcement(Formula):
    r"""Class representing formula 6.13 for the calculation of the shear resistance for members with inclined
    shear reinforcement, [$V_{Rd,s}$].
    """

    label = "6.13"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        a_sw: MM2,
        s: MM,
        z: MM,
        f_ywd: MPA,
        theta: DEG,
        alpha: DEG,
    ) -> None:
        r"""[$V_{Rd,s}$] Shear resistance for members with inclined shear reinforcement [$N$].

        EN 1992-1-1:2004 art.6.2.3(4) - Formula (6.13)

        Parameters
        ----------
        a_sw : MM2
            [$A_{sw}$] Area of shear reinforcement [$mm^2$].
        s : MM
            [$s$] Spacing of the shear reinforcement [$mm$].
        z : MM
            [$z$] Lever arm [$mm$].
        f_ywd : MPA
            [$f_{ywd}$] Design yield strength of the shear reinforcement [$MPa$].
        theta : DEG
            [$\theta$] angle between the concrete compression strut and the beam axis perpendicular to the
            shear force [$degrees$].
        alpha : DEG
            [$\alpha$] angle between shear reinforcement and the beam axis perpendicular to the shear force [$degrees$].
        """
        super().__init__()
        self.a_sw = a_sw
        self.s = s
        self.z = z
        self.f_ywd = f_ywd
        self.theta = theta
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        a_sw: MM2,
        s: MM,
        z: MM,
        f_ywd: MPA,
        theta: DEG,
        alpha: DEG,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            a_sw=a_sw,
            z=z,
            f_ywd=f_ywd,
            theta=theta,
            alpha=alpha,
        )
        raise_if_less_or_equal_to_zero(
            s=s,
        )

        return (a_sw / s) * z * f_ywd * (cot(theta) + cot(alpha)) * np.sin(np.deg2rad(alpha))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.13."""
        return LatexFormula(
            return_symbol=r"V_{Rd,s}",
            result=f"{self:.{n}f}",
            equation=r"\frac{A_{sw}}{s} \cdot z \cdot f_{ywd} \cdot \left(\cot(\theta) + \cot(\alpha)\right) \cdot \sin(\alpha)",
            numeric_equation=rf"\frac{{{self.a_sw:.{n}f}}}{{{self.s:.{n}f}}} \cdot {self.z:.{n}f} \cdot {self.f_ywd:.{n}f} \cdot "
            rf"\left(\cot({self.theta:.{n}f}) + \cot({self.alpha:.{n}f})\right) \cdot \sin({self.alpha:.{n}f})",
            comparison_operator_label="=",
            unit="N",
        )
