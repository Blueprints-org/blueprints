"""Formula 9.9 from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailling and specific rules."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DEG, MM
from blueprints.validations import raise_if_negative


class Form9Dot9MaximumSpacingSeriesOfLinks(Formula):
    """Class representing the formula 9.9 for the calculation of the maximum distance between successive series of links in longitudinal direction
    for slabs.
    """

    label = "9.9"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        d: MM,
        alpha: DEG,
    ) -> None:
        """[smax] Maximum distance between successive series of links in longitudinal direction for slabs [mm].

        NEN-EN 1992-1-1+C2:2011 art.9.3.2(4) - Formula (9.9)

        Parameters
        ----------
        d: MM
            [d] Effective height of the cross-section [mm].
        alpha: DEG
            [α] The angle between the shear reinforcement and the longitudinal axis of the slab (see 9.2.2(1)) [deg].
        """
        super().__init__()
        self.d = d
        self.alpha = alpha

    @staticmethod
    def _evaluate(d: MM, alpha: DEG) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(d=d)

        # Convert the angle from degrees to radians
        alpha_radians = np.deg2rad(alpha)

        # Calculate the cotangent
        cot_alpha = 1 / np.tan(alpha_radians)

        return 0.75 * d * (1 + cot_alpha)
