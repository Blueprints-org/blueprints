"""Formula 5.5 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit states."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1993_5_2008 import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction
from blueprints.type_alias import DIMENSIONLESS, KN, MM2, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot5PlasticShearResistance(Formula):
    """Class representing formula 5.5 for the design plastic shear resistance for each web."""

    label = "5.5"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        a_v: MM2,
        f_y: MPA,
        gamma_m_0: DIMENSIONLESS,
    ) -> None:
        r"""([$V_{pl,Rd}$]) Calculate design plastic shear resistance for each web in [$kN$].

        NEN-EN 1993-5:2008(E) art.5.2.2(4) - Formula (5.5)

        Parameters
        ----------
        a_v : MM2
            ([$A_{v}$]) Projected shear area for each web, acting in the same direction as VEd in [$mm^2$].
        f_y : MPA
            ([$f_{y}$]) Yield strength in [$MPa$].
        gamma_m_0 : DIMENSIONLESS
            ([$\gamma_{M0}$]) Partial factor for material properties in [$-$].
        """
        super().__init__()
        self.a_v: float = a_v
        self.f_y: float = f_y
        self.gamma_m_0: DIMENSIONLESS = gamma_m_0

    @staticmethod
    def _evaluate(
        a_v: MM2,
        f_y: MPA,
        gamma_m_0: DIMENSIONLESS,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(a_v=a_v, f_y=f_y, gamma_m_0=gamma_m_0)
        return (a_v * f_y / (np.sqrt(3) * gamma_m_0)) * N_TO_KN

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.5."""
        return LatexFormula(
            return_symbol=r"V_{pl,Rd}",
            result=str(self),
            equation=latex_fraction(
                numerator="A_v f_y",
                denominator=r"\sqrt{3} \gamma_{M0}",
            ),
            numeric_equation=latex_fraction(
                numerator=rf"{self.a_v} \cdot {self.f_y}",
                denominator=rf"\sqrt{{3}} \cdot {self.gamma_m_0}",
            ),
            comparison_operator_label="=",
        )
