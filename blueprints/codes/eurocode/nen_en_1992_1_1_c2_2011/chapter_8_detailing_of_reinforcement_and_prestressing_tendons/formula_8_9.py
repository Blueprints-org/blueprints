"""Formula 8.9 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import KN, MM, MM2, MPA
from blueprints.unit_conversion import N_TO_KN
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot9AnchorageCapacityWeldedTransverseBarSmallDiameter(Formula):
    """Class representing the formula 8.9 for the calculation of the anchorage capacity of a welded cross bar for nominal bar diameters smaller
    than 12 mm.
    """

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
        """[:math:`F_{btd}`] Anchorage capacity of a welded cross bar for nominal bar diameters smaller than 12 mm [:math:`kN`].

        NEN-EN 1992-1-1+C2:2011 art.8.6(5) - formula 8.9

        Parameters
        ----------
        f_wd : KN
            [:math:`F_{wd}`] Design shear strength of weld (specified as a factor times :math:`A_{s} ⋅ f_{yd}`; say :math:`0.5 ⋅ A_{s} ⋅ f_{yd}`
            where :math:`A_{s}` is the cross-section of the anchored bar and :math:`f_{yd}` is its design yield strength)  [:math:`kN`].
        diameter_t : MM
            [:math:`ø_{t}`] Diameter of the transverse bar [:math:`mm`].

            Note: :math:`ø_{t} =< 12 mm`.
        diameter_l : MM
            [:math:`ø_{l}`] Diameter of the bar to be anchored [:math:`mm`].

            Note: :math:`ø_{l} =< 12 mm`.
        a_s : MM2
            [:math:`A_{s}`] Cross-section of the anchored bar [:math:`mm^{2}`].
        f_cd : MPA
            [:math:`f_{cd}`] Design compressive strength of concrete [:math:`MPa`].
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
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            f_wd=f_wd,
            diameter_t=diameter_t,
            a_s=a_s,
            f_cd=f_cd,
        )
        raise_if_less_or_equal_to_zero(diameter_l=diameter_l)
        return min(f_wd, N_TO_KN * 16 * a_s * f_cd * (diameter_t / diameter_l))
