"""This package represents the Eurocode NEN-EN 1992-1-1+C2:2011 code - Chapter 9 - formula (9.15)."""
# pylint: disable=arguments-differ

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import KN, KN_M, M
from blueprints.validations import raise_if_negative


class Form9Dot15MinimumResistancePeripheralTie(Formula):
    """Class representing the formula 9.15 for calculating the minimum force a peripheral tie should be able to resist."""

    label = "9.15"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        l_i: M,
        q_1: KN_M,
        q_2: KN,
    ) -> None:
        """[Ftie,per] Minimum force a peripheral tie should be able to resist [kN].

        NEN-EN 1992-1-1+C2:2011 art.9.10.2.2(2) - Formula (9.15)

        Parameters
        ----------
        l_i: MM
            [li] Length of the end-span [mm].
        q_1: KN_M
            [q1] Minimum downward load may be found in national annex, recommended value is 10 [kN/m].
        q_2: KN
            [Q2] May be found in national annex, recommended value is 70 [kN].
        """
        super().__init__()
        self.l_i = l_i
        self.q_1 = q_1
        self.q_2 = q_2

    @staticmethod
    def _evaluate(
        l_i: M,
        q_1: KN_M,
        q_2: KN,
    ) -> KN:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(l_i=l_i, q_1=q_1, q_2=q_2)
        return max(l_i * q_1, q_2)
