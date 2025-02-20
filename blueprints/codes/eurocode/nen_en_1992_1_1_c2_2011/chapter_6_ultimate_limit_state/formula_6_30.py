"""Formula 6.30 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DEG, DIMENSIONLESS, MM, MM2, MPA, NMM
from blueprints.validations import raise_if_negative


class Form6Dot30DesignTorsionalResistanceMoment(Formula):
    r"""Class representing formula 6.30 for the calculation of the design torsional resistance moment, [$T_{Rd,max}$]."""

    label = "6.30"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        nu: DIMENSIONLESS,
        alpha_cw: DIMENSIONLESS,
        f_cd: MPA,
        a_k: MM2,
        t_ef_i: MM,
        theta: DEG,
    ) -> None:
        r"""[$T_{Rd,max}$] Design torsional resistance moment [$Nmm$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(4) - Formula (6.30)

        Parameters
        ----------
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor for concrete cracked in shear, see 6.2.2 (6) [$-$].
        alpha_cw : DIMENSIONLESS
            [$\alpha_{cw}$] Coefficient taking account of the state of the stress in the compression chord, see Expression (6.9) [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of concrete compressive strength [$MPa$].
        a_k : MM2
            [$A_{k}$] Area enclosed by the centre-lines of the connecting walls, including inner hollow areas [$mm^2$].
        t_ef_i : MM
            [$t_{ef,i}$] Effective wall thickness [$mm$].
        theta : DEG
            [$\theta$] Angle of compression struts (see Figure 6.5) [$degrees$].
        """
        super().__init__()
        self.nu = nu
        self.alpha_cw = alpha_cw
        self.f_cd = f_cd
        self.a_k = a_k
        self.t_ef_i = t_ef_i
        self.theta = theta

    @staticmethod
    def _evaluate(
        nu: DIMENSIONLESS,
        alpha_cw: DIMENSIONLESS,
        f_cd: MPA,
        a_k: MM2,
        t_ef_i: MM,
        theta: DEG,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            nu=nu,
            alpha_cw=alpha_cw,
            f_cd=f_cd,
            a_k=a_k,
            t_ef_i=t_ef_i,
            theta=theta,
        )

        return 2 * nu * alpha_cw * f_cd * a_k * t_ef_i * np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(theta))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.30."""
        return LatexFormula(
            return_symbol=r"T_{Rd,max}",
            result=f"{self:.3f}",
            equation=r"2 \cdot \nu \cdot \alpha_{cw} \cdot f_{cd} \cdot A_{k} \cdot t_{ef,i} \cdot \sin(\theta) \cdot \cos(\theta)",
            numeric_equation=rf"2 \cdot {self.nu:.3f} \cdot {self.alpha_cw:.3f} \cdot {self.f_cd:.3f} \cdot {self.a_k:.3f} "
            rf"\cdot {self.t_ef_i:.3f} \cdot \sin({self.theta:.3f}) \cdot \cos({self.theta:.3f})",
            comparison_operator_label="=",
            unit="Nmm",
        )
