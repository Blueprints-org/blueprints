"""Formula 7.15 from NEN-EN 1992-1-1+C2:2011: Chapter 7 - Serviceability Limit State."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_greater_than_90, raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot15MaximumCrackSpacing(Formula):
    r"""Class representing formula 7.15 for the calculation of [$S_{r,max}$]."""

    label = "7.15"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        theta: DIMENSIONLESS,
        sr_max_y: MM,
        sr_max_z: MM,
    ) -> None:
        r"""[$S_{r,max}$] Calculation of the maximum crack spacing [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.7.3.4(4) - Formula (7.15)

        Parameters
        ----------
        theta : DIMENSIONLESS
            [$\theta$] Angle between the reinforcement in the y direction and the direction of the principal tensile stress [$degrees$].
        sr_max_y : MM
            [$s_{r,max,y}$] Crack spacing in the y direction [$mm$].
        sr_max_z : MM
            [$s_{r,max,z}$] Crack spacing in the z direction [$mm$].
        """
        super().__init__()
        self.theta = theta
        self.sr_max_y = sr_max_y
        self.sr_max_z = sr_max_z

    @staticmethod
    def _evaluate(
        theta: DIMENSIONLESS,
        sr_max_y: MM,
        sr_max_z: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(sr_max_y=sr_max_y, sr_max_z=sr_max_z)
        raise_if_negative(theta=theta)
        raise_if_greater_than_90(theta=theta)

        return 1 / ((np.cos(np.deg2rad(theta)) / sr_max_y) + (np.sin(np.deg2rad(theta)) / sr_max_z))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 7.15."""
        _equation: str = r"\frac{1}{\left(\frac{\cos(\theta)}{s_{r,max,y}}\right) + \left(\frac{\sin(\theta)}{s_{r,max,z}}\right)}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\theta": f"{self.theta:.3f}",
                r"s_{r,max,y}": f"{self.sr_max_y:.3f}",
                r"s_{r,max,z}": f"{self.sr_max_z:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"s_{r,max}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm",
        )
