"""Formula 6.19 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG, MM2, MPA, N
from blueprints.validations import raise_if_negative


class Form6Dot19CheckShearForce(Formula):
    r"""Class representing formula 6.19 for checking the shear force."""

    label = "6.19"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        v_ed: N,
        a_sw: MM2,
        f_ywd: MPA,
        alpha: DEG,
    ) -> None:
        r"""Check the shear force with :math:`V_{Ed} \leq A_{sw} \cdot f_{ywd} \cdot \sin(\alpha)`.

        EN 1992-1-1:2004 art.6.2.3(8) - Formula (6.19)

        Parameters
        ----------
        v_ed : N
            [:math:`V_{Ed}`] Design value of the shear force [:math:`N`].
        a_sw : MM2
            [:math:`A_{sw}`] Cross-sectional area of the shear reinforcement [:math:`mm^2`].
        f_ywd : MPA
            [:math:`f_{ywd}`] Design yield strength of the shear reinforcement [:math:`MPa`].
        alpha : DEG
            [:math:`\alpha`] Angle between shear reinforcement and the beam axis perpendicular to the shear force [:math:`degrees`].
        """
        super().__init__()
        self.v_ed = v_ed
        self.a_sw = a_sw
        self.f_ywd = f_ywd
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        v_ed: N,
        a_sw: MM2,
        f_ywd: MPA,
        alpha: DEG,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(alpha=alpha, f_ywd=f_ywd, a_sw=a_sw, v_ed=v_ed)

        return v_ed <= a_sw * f_ywd * np.sin(np.deg2rad(alpha))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.19."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"V_{Ed} \leq A_{sw} \cdot f_{ywd} \cdot \sin(\alpha)",
            numeric_equation=rf"{self.v_ed:.{n}f} \leq {self.a_sw:.{n}f} \cdot {self.f_ywd:.{n}f} \cdot \sin({self.alpha:.{n}f})",
            comparison_operator_label="\\to",
            unit="",
        )
