"""Formula 1.0.1 from NEN 9997-1+C2:2017: Chapter 1: General rules."""

import numpy as np

from blueprints.codes.eurocode.nen_9997_1_c2_2017 import NEN_9997_1_C2_2017
from blueprints.codes.formula import Formula
from blueprints.type_alias import M
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form1Dot0Dot1EquivalentPilePointCenterline(Formula):
    """Class representing formula 1.0.1 for the calculation of the equivalent pile point centerline :math:`D_{eq}` in [m]."""

    label = "1.0.1"
    source_document = NEN_9997_1_C2_2017

    def __init__(self, a: M, b: M) -> None:
        """[:math:`D_{eq}`] Equivalent pile point centerline.

        NEN 9997-1+C2:2017 art.1.5.2.106a - Formula (1.0.1)

        Parameters
        ----------
        a : M
            [:math:`a`] minor dimension of the largest cross-section at the pile tip [:math:`m`].
        b : M
            [:math:`b`] major dimension of the largest cross-section at the pile tip [:math:`m`].

            Where: b ≤ 1.5 * a
        """
        super().__init__()
        self.a = a
        self.b = b

    @staticmethod
    def _evaluate(
        a: M,
        b: M,
    ) -> M:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(b=b)
        raise_if_less_or_equal_to_zero(a=a)
        b_calc = min(b, 1.5 * a)
        return 1.13 * a * np.sqrt(b_calc / a)
