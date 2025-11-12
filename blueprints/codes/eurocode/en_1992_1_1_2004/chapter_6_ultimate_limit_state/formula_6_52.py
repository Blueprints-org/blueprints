"""Formula 6.52 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, MM, MM2, MPA
from blueprints.validations import raise_if_negative


class Form6Dot52PunchingShearResistance(Formula):
    r"""Class representing formula 6.52 for the calculation of punching shear resistance.

    EN 1992-1-1:2004 art.6.4.5(1) - Formula (6.52)

    Parameters
    ----------
    v_rd_c : MPA
        [$v_{Rd,c}$] Design shear strength of concrete without shear reinforcement [$MPa$].
    d : MM
        [$d$] Mean effective depth of the slab [$mm$].
    s_r : MM
        [$s_r$] Radial spacing of perimeters of shear reinforcement [$mm$].
    a_sw : MM2
        [$A_{sw}$] Area of one perimeter of shear reinforcement around the column [$mm^2$].
    f_ywd_ef : MPA
        [$f_{ywd,ef}$] Effective design strength of the punching shear reinforcement [$MPa$].
    u_1 : MM
        [$u_{y1}$] Perimeter of the critical section [$mm$].
    alpha : DEG
        [$\alpha$] Angle between the shear reinforcement and the plane of the slab [$deg$].
    """

    label = "6.52"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        v_rd_c: MPA,
        d: MM,
        s_r: MM,
        a_sw: MM2,
        f_ywd_ef: MPA,
        u_1: MM,
        alpha: DEG,
    ) -> None:
        super().__init__()
        self.v_rd_c = v_rd_c
        self.d = d
        self.s_r = s_r
        self.a_sw = a_sw
        self.f_ywd_ef = f_ywd_ef
        self.u_1 = u_1
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        v_rd_c: MPA,
        d: MM,
        s_r: MM,
        a_sw: MM2,
        f_ywd_ef: MPA,
        u_1: MM,
        alpha: DEG,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_rd_c=v_rd_c, d=d, s_r=s_r, a_sw=a_sw, f_ywd_ef=f_ywd_ef, u_1=u_1, alpha=alpha)

        return 0.75 * v_rd_c + 1.5 * (d / s_r) * a_sw * f_ywd_ef * (1 / (u_1 * d)) * np.sin(np.deg2rad(alpha))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.52."""
        _equation: str = (
            r"0.75 \cdot v_{Rd,c} + 1.5 \cdot \frac{ d}{s_r} \cdot A_{sw} \cdot f_{ywd,ef} \cdot \frac{1}{u_{1} \cdot d} \cdot \sin(\alpha)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"v_{Rd,c}": f"{self.v_rd_c:.{n}f}",
                r"s_r": f"{self.s_r:.{n}f}",
                r"A_{sw}": f"{self.a_sw:.{n}f}",
                r"f_{ywd,ef}": f"{self.f_ywd_ef:.{n}f}",
                r"u_{1}": f"{self.u_1:.{n}f}",
                r"\alpha": f"{self.alpha:.{n}f}",
                r" d": f" {self.d:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"v_{Rd,cs}",
            result=f"{self._evaluate(self.v_rd_c, self.d, self.s_r, self.a_sw, self.f_ywd_ef, self.u_1, self.alpha):.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )


"""Formula 6.52sub1 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""


class Form6Dot52Sub1EffectiveYieldStrength(Formula):
    r"""Class representing formula 6.52sub1 for the calculation of [$f_{ywd,ef}$]."""

    label = "6.52sub1"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        d: MM,
        f_ywd: MPA,
    ) -> None:
        r"""[f_{ywd,ef}] Calculation of [$f_{ywd,ef}$].

        EN 1992-1-1:2004 art.6.4.5(1) - Formula (6.52sub1)

        Parameters
        ----------
        d : MM
            [$d$] Mean effective depth of the slab [$mm$].
        f_ywd : MPA
            [$f_{ywd}$] Design yield strength of the reinforcement [$MPa$].
        """
        super().__init__()
        self.d = d
        self.f_ywd = f_ywd

    @staticmethod
    def _evaluate(
        d: MM,
        f_ywd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(d=d, f_ywd=f_ywd)

        return min(250 + 0.25 * d, f_ywd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.52sub1."""
        _equation: str = r"\min\left(250 + 0.25 \cdot d, f_{ywd}\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
                r" d": f" {self.d:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"f_{ywd,ef}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
