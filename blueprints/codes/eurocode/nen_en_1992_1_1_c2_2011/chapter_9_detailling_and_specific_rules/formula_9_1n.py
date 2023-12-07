"""This package represents the Eurocode NEN-EN 1992-1-1+C2:2011 code - Chapter 9 - formula (9.1N)."""
# pylint: disable=arguments-differ

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MM, MM2, MPA
from blueprints.validations import raise_if_negative


class Form9Dot1NMinimumTensileReinforcementBeam(Formula):
    """Class representing the formula 9.1N for the calculation of minimum tensile reinforcement area in longitudinal direction for beams"""

    label = "9.1N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ctm: MPA,
        f_yk: MPA,
        b_t: MM,
        d: MM,
    ) -> None:
        """[As,min] Calculates the minimum required tensile reinforcement area in longitudinal direction for beams [mm²].

        NEN-EN 1992-1-1+C2:2011 art.9.2.1.1(1) - Formula (9.1N)

        Parameters
        ----------
        f_ctm: MPA
            [fctm] Average axial tensile stress concrete [MPa].
        f_yk: MPA
            [fyk] Characteristic yield strength reinforcement steel [MPa].
        b_t: MM
            [bt] Average width concrete tension zone, for T-beams with a flange under compression only the width of the web is considered for
            calculating bt [mm].
        d: MM
            [d] Effective height of the cross-section [mm].
        """
        super().__init__()
        self.f_ctm = f_ctm
        self.f_yk = f_yk
        self.b_t = b_t
        self.d = d

    @staticmethod
    def _evaluate(
        f_ctm: MPA,
        f_yk: MPA,
        b_t: MM,
        d: MM,
    ) -> MM2:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(f_ctm=f_ctm, f_yk=f_yk, b_t=b_t, d=d)
        return max(0.26 * f_ctm * b_t * d / f_yk, 0.0013 * b_t * d)
