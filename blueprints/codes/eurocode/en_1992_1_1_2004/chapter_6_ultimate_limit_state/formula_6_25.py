"""Formula 6.25 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG, DIMENSIONLESS, MM2, MPA
from blueprints.validations import raise_if_greater_than_90, raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot25DesignShearResistance(Formula):
    r"""Class representing formula 6.25 for the calculation of the design shear resistance at the interface, [$v_{Rdi}$]."""

    label = "6.25"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        c: DIMENSIONLESS,
        mu: DIMENSIONLESS,
        f_ctd: MPA,
        sigma_n: MPA,
        a_s: MM2,
        a_i: MM2,
        f_yd: MPA,
        alpha: DEG,
        nu: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        r"""[$v_{Rdi}$] Design shear resistance at the interface [$MPa$].

        EN 1992-1-1:2004 art.6.2.5(1) - Formula (6.25)

        Parameters
        ----------
        c : DIMENSIONLESS
            [$c$] Factor which depends on the roughness of the interface, see (2) [$-$].
        mu : DIMENSIONLESS
            [$\mu$] Factor which depends on the roughness of the interface, see (2) [$-$].
        f_ctd : MPA
            [$f_{ctd}$] Design tensile strength of concrete, as defined in 3.1.6 (2)P [$MPa$].
        sigma_n : MPA
            [$\sigma_{n}$] Stress per unit area caused by the minimum external normal force across the interface [$MPa$].
        a_s : MM2
            [$A_{s}$] Area of reinforcement crossing the interface [$mm^2$].
        a_i : MM2
            [$A_{i}$] Area of the joint [$mm^2$].
        f_yd : MPA
            [$f_{yd}$] Design yield strength of reinforcement [$MPa$].
        alpha : DEG
            [$\alpha$] Angle of the interface, limited by 45° ≤ α ≤ 90° [$degrees$].
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor [$-$].
        f_cd : MPA
            [$f_{cd}$] Design compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.c = c
        self.mu = mu
        self.f_ctd = f_ctd
        self.sigma_n = sigma_n
        self.a_s = a_s
        self.a_i = a_i
        self.f_yd = f_yd
        self.alpha = alpha
        self.nu = nu
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        c: DIMENSIONLESS,
        mu: DIMENSIONLESS,
        f_ctd: MPA,
        sigma_n: MPA,
        a_s: MM2,
        a_i: MM2,
        f_yd: MPA,
        alpha: DEG,
        nu: DIMENSIONLESS,
        f_cd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            c=c,
            mu=mu,
            f_ctd=f_ctd,
            sigma_n=sigma_n,
            a_s=a_s,
            f_yd=f_yd,
            alpha=alpha,
            nu=nu,
            f_cd=f_cd,
        )
        raise_if_less_or_equal_to_zero(a_i=a_i)
        raise_if_greater_than_90(alpha=alpha)

        term1 = c * f_ctd + mu * sigma_n + (a_s / a_i) * f_yd * (mu * np.sin(np.deg2rad(alpha)) + np.cos(np.deg2rad(alpha)))
        term2 = 0.5 * nu * f_cd

        return min(term1, term2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.25."""
        return LatexFormula(
            return_symbol=r"v_{Rdi}",
            result=f"{self:.{n}f}",
            equation=r"\min \left( c \cdot f_{ctd} + \mu \cdot \sigma_{n} + \frac{A_{s}}{A_{i}} \cdot f_{yd} \cdot "
            r"(\mu \cdot \sin(\alpha) + \cos(\alpha)); 0.5 \cdot \nu \cdot f_{cd} \right)",
            numeric_equation=rf"\min \left( {self.c:.{n}f} \cdot {self.f_ctd:.{n}f} + {self.mu:.{n}f} \cdot {self.sigma_n:.{n}f} "
            rf"+ \frac{{{self.a_s:.{n}f}}}{{{self.a_i:.{n}f}}} \cdot {self.f_yd:.{n}f} \cdot ({self.mu:.{n}f} \cdot \sin({self.alpha:.{n}f}) "
            rf"+ \cos({self.alpha:.{n}f})); 0.5 \cdot {self.nu:.{n}f} \cdot {self.f_cd:.{n}f} \right)",
            comparison_operator_label="=",
            unit="MPa",
        )
