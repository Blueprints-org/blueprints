"""Formula 8.9 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons"""
# pylint: disable=arguments-differ
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import KN, MM, MM2, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(Formula):
    """Class representing the formula 8.9 for the calculation of the anchorage capacity of a welded cross bar for nominal bar diameters smaller
    than 12 mm."""

    label = "8.9"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_wd: KN,
        diameter_t: MM,
        diameter_l: MM,
        a_s: MM2,
        f_cd: MPA,
    ) -> None:
        """[Fbtd] Anchorage capacity of a welded cross bar for nominal bar diameters smaller than 12 mm [kN].

        NEN-EN 1992-1-1+C2:2011 art.8.6(5) - formula 8.9

        Parameters
        ----------
        f_wd : KN
            [Fwd] Design shear strength of weld (specified as a factor times As*fyd; say 0.5*As*fyd where As is the cross-section of the anchored bar
            and fyd is its design yield strength)  [kN].
        diameter_t : MM
            [Φt] Diameter of the transverse bar [mm].
            Note: Φt =< 12 mm.
        diameter_l : MM
            [Φl] Diameter of the bar to be anchored [mm].
            Note: Φl =< 12 mm.
        a_s : MM2
            [As] Cross-section of the anchored bar [mm²].
        f_cd : MPA
            [fcd] Design compressive strength of concrete [MPa].
        """
        super().__init__()
        self.f_wd = f_wd
        self.diameter_t = diameter_t
        self.diameter_l = diameter_l
        self.a_s = a_s
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        f_wd: KN,
        diameter_t: MM,
        diameter_l: MM,
        a_s: MM2,
        f_cd: MPA,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method"""
        raise_if_negative(
            f_wd=f_wd,
            diameter_t=diameter_t,
            a_s=a_s,
            f_cd=f_cd,
        )
        raise_if_less_or_equal_to_zero(diameter_l=diameter_l)
        return min(f_wd, N_TO_KN * 16 * a_s * f_cd * (diameter_t / diameter_l))
