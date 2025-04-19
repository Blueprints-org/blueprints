"""Formula 6.65 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG
from blueprints.validations import raise_if_negative


class Form6Dot65ConcreteCompressionStrut(Formula):
    r"""Class representing formula 6.65 for the calculation of [$\theta_{fat}$]."""

    label = "6.65"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        theta: DEG,
    ) -> None:
        r"""[$\theta_{fat}$] Calculation of concrete compression struts angle for fatigue.

        NEN-EN 1992-1-1+C2:2011 art.6.8.2(2) - Formula (6.65)

        Parameters
        ----------
        theta : DEG
            [$\theta$] Angle of concrete compression struts to the beam axis assumed in ULS design [$degrees$].
        """
        super().__init__()
        self.theta = theta

    @staticmethod
    def _evaluate(
        theta: DEG,
    ) -> DEG:
        """Evaluates the formula, for more information see the __init__ method."""
        theta_rad = np.deg2rad(theta)
        tangent_theta = np.tan(theta_rad)
        raise_if_negative(tangent_theta=tangent_theta)

        theta_fat_rad = np.arctan(np.minimum(np.sqrt(np.tan(theta_rad)), 1))
        return np.rad2deg(theta_fat_rad)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.65."""
        _equation: str = r"\tan^{-1}\left(\min\left(\sqrt{\tan(\theta)}, 1\right)\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\theta": f"{self.theta:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\theta_{fat}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="degrees",
        )
