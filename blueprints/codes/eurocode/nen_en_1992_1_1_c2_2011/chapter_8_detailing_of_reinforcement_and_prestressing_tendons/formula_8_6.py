"""Formula 8.6 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons"""
# pylint: disable=arguments-differ
# pylint: disable=duplicate-code

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form8Dot6MinimumTensionAnchorage(Formula):
    """Class representing formula 8.6 for the calculation of the minimum anchorage length if no other limitation is applied for anchorage in
    tension."""

    label = "8.6"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        l_b_rqd: MM,
        diameter: MM,
    ) -> None:
        """[lb,min] Minimum anchorage length if no other limitation is applied for anchorage in tension. [mm].

        NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.6)

        Parameters
        ----------
        l_b_rqd: MM
            [lb,rqd] Basic required anchorage length, for anchoring the force As*σsd in a straight bar assuming constant
            bond stress (formula 8.3) [mm].
            Use your own implementation for this value or use the Form8Dot3RequiredAnchorageLength class.
        diameter: MM
            [Ø] Diameter of the bar [mm].
        """
        super().__init__()
        self.l_b_rqd = l_b_rqd
        self.diameter = diameter

    @staticmethod
    def _evaluate(l_b_rqd: MM, diameter: MM) -> MM:
        """Evaluates the formula, for more information see the __init__ method"""
        raise_if_negative(diameter=diameter, l_b_rqd=l_b_rqd)
        return max(0.3 * l_b_rqd, 10 * diameter, 100)
