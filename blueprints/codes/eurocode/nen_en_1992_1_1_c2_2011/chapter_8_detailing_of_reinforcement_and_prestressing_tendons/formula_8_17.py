"""Formula 8.17 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form8Dot17DesignValueTransmissionLength1(Formula):
    """Class representing formula 8.17 for the calculation of design value 1 of the transmission length :math:`l_{pt1}`. The less favourable of
    :math:`l_{pt1}` or :math:`l_{pt2}` has to be chosen depending on the design situation.
    """

    label = "8.17"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, l_pt: MM) -> None:
        """[:math:`l_{pt1}`] design value 1 of the transmission length [:math:`mm`].

        NEN-EN 1992-1-1+C2:2011 art.8.10.2.2(3) - Formula (8.17)

        Parameters
        ----------
        l_pt : MM
            [:math:`l_{pt}`] Basic value of the transmission length [:math:`mm`].
            Use your own implementation for this value or use :class:`Form8Dot16BasicTransmissionLength` class.
        """
        super().__init__()
        self.l_pt = l_pt

    @staticmethod
    def _evaluate(
        l_pt: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(l_pt=l_pt)
        return 0.8 * l_pt
