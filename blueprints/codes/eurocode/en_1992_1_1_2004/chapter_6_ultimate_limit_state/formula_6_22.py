"""Formula 6.22 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG, DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form6Dot22CheckCrushingCompressionStruts(Formula):
    r"""Class representing formula 6.22 for checking the crushing of the compression struts in the flange."""

    label = "6.22"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        v_ed: MPA,
        nu: DIMENSIONLESS,
        f_cd: MPA,
        theta_f: DEG,
    ) -> None:
        r"""Check the crushing of the compression struts in the flange.

        EN 1992-1-1:2004 art.6.2.4(4) - Formula (6.22)

        Parameters
        ----------
        v_ed : MPA
            [$v_{Ed}$] Design shear force [$MPa$].
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of concrete compressive strength [$MPa$].
        theta_f : DEG
            [$\theta_{f}$] Angle of the compression struts [$-$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.nu = nu
        self.f_cd = f_cd
        self.theta_f = theta_f

    @staticmethod
    def _evaluate(
        v_ed: MPA,
        nu: DIMENSIONLESS,
        f_cd: MPA,
        theta_f: DEG,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed=v_ed, f_cd=f_cd, nu=nu, theta_f=theta_f)

        return v_ed <= nu * f_cd * np.sin(np.radians(theta_f)) * np.cos(np.radians(theta_f))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.22."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"v_{Ed} \leq \nu \cdot f_{cd} \cdot \sin(\theta_{f}) \cdot \cos(\theta_{f})",
            numeric_equation=rf"{self.v_ed:.{n}f} \leq {self.nu:.{n}f} \cdot {self.f_cd:.{n}f} \cdot \sin({self.theta_f:.{n}f}) "
            rf"\cdot \cos({self.theta_f:.{n}f})",
            comparison_operator_label="\\to",
            unit="",
        )
