"""Formula 9.7N from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailing of members and particular rules."""

import numpy as np

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DEG, MM
from blueprints.validations import raise_if_greater_than_90, raise_if_negative


class Form9Dot7nMaximumDistanceBentUpBars(Formula):
    """Class representing the formula 9.7N for the calculation of the maximum distance between bent-up bars in longitudinal direction."""

    label = "9.7N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        d: MM,
        alpha: DEG,
    ) -> None:
        """[sb,max] Maximum distance between bent-up bars in longitudinal direction [mm].

        NEN-EN 1992-1-1+C2:2011 art.9.2.2(7) - Formula (9.7N)

        Parameters
        ----------
        d: MM
            [d] Effective height of the cross-section [mm].
        alpha: DEG
            [α] The angle between the shear reinforcement and the longitudinal axis of the beam (see 9.2.2(1)) [deg].
        """
        super().__init__()
        self.d = d
        self.alpha = alpha

    @staticmethod
    def _evaluate(d: MM, alpha: DEG) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(d=d, alpha=alpha)
        raise_if_greater_than_90(alpha=alpha)

        # Convert the angle from degrees to radians
        alpha_radians = np.deg2rad(alpha)

        # Calculate the cotangent
        cot_alpha = 1 / np.tan(alpha_radians)

        return 0.6 * d * (1 + cot_alpha)
