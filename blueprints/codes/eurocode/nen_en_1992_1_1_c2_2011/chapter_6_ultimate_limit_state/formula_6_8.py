"""Formula 6.8 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG, MM, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot8ShearResistance(Formula):
    r"""Class representing formula 6.8 for the calculation of the shear resistance, :math:`V_{Rd,s}`."""

    label = "6.8"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_sw: MM2,
        s: MM,
        z: MM,
        f_ywd: MPA,
        theta: DEG,
    ) -> None:
        r"""[:math:`V_{Rd,s}`] Shear resistance [:math:`N`].

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(3) - Formula (6.8)

        Parameters
        ----------
        a_sw : MM2
            [:math:`A_{sw}`] Cross-sectional area of the shear reinforcement [:math:`mm^2`].
        s : MM
            [:math:`s`] Spacing of the stirrups [:math:`mm`].
        z : MM
            [:math:`z`] Lever arm [:math:`mm`].
        f_ywd : MPA
            [:math:`f_{ywd}`] Design yield strength of the shear reinforcement [:math:`MPa`].
        theta : DEG
            [:math:`\theta`] Angle between the concrete compression strut and the beam axis perpendicular to the shear force [:math:`degrees`].
        """
        super().__init__()
        self.a_sw = a_sw
        self.s = s
        self.z = z
        self.f_ywd = f_ywd
        self.theta = theta

    @staticmethod
    def _evaluate(
        a_sw: MM2,
        s: MM,
        z: MM,
        f_ywd: MPA,
        theta: DEG,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(s=s)
        raise_if_negative(theta=theta, f_ywd=f_ywd, z=z, a_sw=a_sw)

        def cot(theta: DEG) -> float:
            """Returns the cotangent of the given angle."""
            return 1 / np.tan(np.radians(theta))

        return (a_sw / s) * z * f_ywd * cot(theta)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.8."""
        return LatexFormula(
            return_symbol=r"V_{Rd,s}",
            result=f"{self:.3f}",
            equation=r"\frac{A_{sw}}{s} \cdot z \cdot f_{ywd} \cdot \cot(\theta)",
            numeric_equation=rf"\frac{{{self.a_sw:.3f}}}{{{self.s:.3f}}} \cdot {self.z:.3f} \cdot {self.f_ywd:.3f} \cdot \cot({self.theta:.3f})",
            comparison_operator_label="=",
            unit="N",
        )
