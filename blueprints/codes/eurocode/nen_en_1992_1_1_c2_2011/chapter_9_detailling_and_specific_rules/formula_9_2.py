"""This package represents the Eurocode NEN-EN 1992-1-1+C2:2011 code - Chapter 9 - formula (9.2)."""
# pylint: disable=arguments-differ

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DEG, MM


class Form9Dot2ShiftInMomentDiagram(Formula):
    """Class representing the formula 9.2 for the calculation of the shift in the moment diagram for elements with shear reinforcement"""

    label = "9.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        z: MM,
        theta: DEG,
        alpha: DEG,
    ) -> None:
        """[al] Shift in the moment diagram of an element with shear reinforcement [mm].

        NEN-EN 1992-1-1+C2:2011 art.9.2.1.3(2) - Formula (9.2)

        Parameters
        ----------
        z: MM
            [z] The internal lever arm for an element with constant height, corresponding to the bending moment in the considered element. In the
            shear force calculation of reinforced concrete without axial force, the approximate value z = 0.9d may generally be used [mm].
        alpha: DEG
            [α] The angle between the shear reinforcement and the longitudinal axis of the beam (see 9.2.2(1)) [deg].
        theta: DEG
            [θ] The angle between the shear compression strut and the axis of the beam 6.2.3 [C1] [deg].
        """
        super().__init__()
        self.z = z
        self.theta = theta
        self.alpha = alpha

    @staticmethod
    def _evaluate(
        z: MM,
        theta: DEG,
        alpha: DEG,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        if z < 0:
            raise ValueError(f"Negative z: {z}. z cannot be negative")
        if alpha == 0:
            raise ValueError("Alpha = 0. alpha cannot be zero")
        if theta == 0:
            raise ValueError("Theta = 0. theta cannot be zero")
        return z * ((1 / np.tan(theta * np.pi / 180)) - (1 / np.tan(alpha * np.pi / 180))) / 2
