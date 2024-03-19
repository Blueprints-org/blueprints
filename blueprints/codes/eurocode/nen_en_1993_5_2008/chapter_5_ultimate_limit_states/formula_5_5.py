"""Formula 5.5 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit state."""

import numpy as np

from blueprints.codes.eurocode import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, fraction
from blueprints.type_alias import DIMENSIONLESS, KNM, MM2, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot5PlasticShearResistance(Formula):
    """Class representing formula 5.5 for the design plastic shear resistance ."""

    label = "5.5"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        a_v: MM2,
        f_y: MPA,
        gamma_m_0: DIMENSIONLESS,
    ) -> None:
        """(Vpl,Rd) Calculate plastic shear resistance in [kN/m] based on formula 5.5 from NEN-EN 1993-5:2007(E) art. 5.2.2(4).

        Parameters
        ----------
        a_v : MM2
            (Av) Projected shear area for each web, acting in the same direction as VEd in [mm²/m].
        f_y : MPA
            (fy) Yield strength in [MPa].
        gamma_m_0 : DIMENSIONLESS
            (γ_M0) Partial factor for material properties in [-].
        """
        super().__init__()
        self.a_v: float = a_v
        self.f_y: float = f_y
        self.gamma_m_0: float = gamma_m_0

    @staticmethod
    def _evaluate(
        a_v: MM2,
        f_y: MPA,
        gamma_m_0: DIMENSIONLESS,
    ) -> KNM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(a_v=a_v, f_y=f_y, gamma_m_0=gamma_m_0)
        return (a_v * f_y / (np.sqrt(3) * gamma_m_0)) * N_TO_KN

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.5."""
        return LatexFormula(
            return_symbol=r"V_{pl,Rd}",
            result=str(self),
            equation=fraction("A_v f_y", r"\sqrt{3} \gamma_{M0}"),
            numeric_equation=fraction(rf"{self.a_v} \cdot {self.f_y}", rf"\sqrt{{3}} \cdot {self.gamma_m_0}"),
            comparison_operator_label="=",
        )
