"""Formula 8.3 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""
# pylint: disable=arguments-differ
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot3RequiredAnchorageLength(Formula):
    """Class representing formula 8.3 for the calculation of the basic required anchorage length, assuming constant bond stress fbd."""

    label = "8.3"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        diameter: MM,
        sigma_sd: MPA,
        f_bd: MPA,
    ) -> None:
        """[lb,rqd] Basic required anchorage length, for anchoring the force As*σsd in a straight bar assuming constant bond stress fbd. [mm].

        NEN-EN 1992-1-1+C2:2011 art.8.4.3(2) - Formula (8.3)

        Parameters
        ----------
        diameter: MM
            [Ø] Diameter of the bar [mm].
        sigma_sd: MPA
            [σsd] design stress of the bar at the position from where the anchorage is measured from [MPa].
        f_bd: MPA
            [fbd] Design value ultimate bond stress [MPa].
            Use your own implementation for this value or use the Form8Dot2UltimateBondStress class.
        """
        super().__init__()
        self.diameter = diameter
        self.sigma_sd = sigma_sd
        self.f_bd = f_bd

    @staticmethod
    def _evaluate(
        diameter: MM,
        sigma_sd: MPA,
        f_bd: MPA,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(diameter=diameter, sigma_sd=sigma_sd)
        raise_if_less_or_equal_to_zero(f_bd=f_bd)
        return (diameter / 4) * (sigma_sd / f_bd)
