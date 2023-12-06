"""This package represents the Eurocode NEN-EN 1992-1-1+C2:2011 code - Chapter 9 - formula (9.3)."""
# pylint: disable=arguments-differ

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DEG, MM, MM2


class Form9Dot4ShearReinforcementRatio(Formula):
    """Class representing the formula 9.4 for the calculation of the shear reinforcement ratio"""

    label = "9.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_sw: MM2,
        s: MM,
        b_w: MM,
        alpha: DEG,
    ) -> None:
        """[ρw] Shear reinforcement ratio [-].

        NEN-EN 1992-1-1+C2:2011 art.9.2.2(5) - Formula (9.4)

        Parameters
        ----------
        a_sw: MM2
            [Asw] Area of shear reinforcement within length s [mm²].
        s: MM
            [s] The spacing between shear reinforcement along the longitudinal axis of the element [mm].
        b_w: MM
            [bw] The width of the web of the element [mm].
        alpha: DEG
            [α] The angle between the shear reinforcement and the longitudinal axis of the beam (see 9.2.2(1)) [deg].
        """
        super().__init__()
        self.a_sw = a_sw
        self.s = s
        self.b_w = b_w
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        a_sw: MM2,
        s: MM,
        b_w: MM,
        alpha: DEG,
    ) -> float:
        """For more detailed documentation see the class docstring."""
        if a_sw < 0:
            raise ValueError(f"Negative a_sw: {a_sw}. a_sw cannot be negative")
        if s < 0:
            raise ValueError(f"Negative s: {s}. s cannot be negative")
        if b_w < 0:
            raise ValueError(f"Negative b_w: {b_w}. b_w cannot be negative")
        return a_sw / (s * b_w * np.sin(alpha * np.pi / 180))
