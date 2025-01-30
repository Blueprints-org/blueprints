"""Formula 5.15 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

import math

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_negative


class Form5Dot15EffectiveLengthBraced(Formula):
    """Class representing formula 5.15 for the calculation of the effective length of braced members, [$$l_0$$]."""

    label = "5.15"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, k_1: DIMENSIONLESS, k_2: DIMENSIONLESS, height: M) -> None:
        r"""[$$l_{0}$$] Effective length for braced members [$$m$$].

        NEN-EN 1992-1-1+C2:2011 art.5.8.3.2(3) - Formula (5.15)

        Parameters
        ----------
        k_1 : DIMENSIONLESS
            [$$k_{1}$$] Relative flexibility of rotational constraint at end 1 [$$-$$].
        k_2 : DIMENSIONLESS
            [$$k_{2}$$] Relative flexibility of rotational constraint at end 2 [$$-$$].
        height : M
            [$$l$$] Clear height of compression member between end restraints [$$m$$].
        """
        raise_if_negative(k_1=k_1)
        raise_if_negative(k_2=k_2)
        raise_if_negative(height=height)

        self.k_1 = k_1
        self.k_2 = k_2
        self.height = height

    def calculate(self) -> M:
        """Calculate the effective length for braced members [$$l_0$$].

        Returns
        -------
        l_0 : M
            Effective length for braced members [$$m$$].
        """
        return self.height * math.sqrt(self.k_1 * self.k_2)
