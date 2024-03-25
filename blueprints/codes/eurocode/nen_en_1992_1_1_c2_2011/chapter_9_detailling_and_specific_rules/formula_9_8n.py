"""Formula 9.8N from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailing of members and particular rules."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form9Dot8nMaximumTransverseDistanceLegsSeriesShearLinks(Formula):
    """Class representing the formula 9.8N for the calculation of the maximum distance in transverse direction between legs in a series of shear
    links.
    """

    label = "9.8N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, d: MM) -> None:
        """[st,max] Maximum distance in transverse direction between legs in a series of shear links [mm].

        NEN-EN 1992-1-1+C2:2011 art.9.2.2(8) - Formula (9.8N)

        Parameters
        ----------
        d: MM
            [d] Effective height of the cross-section [mm].
        """
        super().__init__()
        self.d = d

    @staticmethod
    def _evaluate(d: MM) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(d=d)
        return min(0.75 * d, 600)
