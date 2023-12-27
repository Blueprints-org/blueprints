"""Formula 7.3 from NEN-EN 1992-1-1+C2:2011: Chapter 7 - Serviceability limit state (SLS)."""
# pylint: disable=arguments-differ
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import KN, MM2, MPA
from blueprints.unit_conversion import KN_TO_N


class Form7Dot3CoefficientKc(Formula):
    """Class representing the formula 7.3 for the coefficient kc for flanges of tubular cross-sections and T-sections."""

    label = "7.3"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_cr: KN,
        a_ct: MM2,
        f_ct_eff: MPA,
    ) -> None:
        """[kc] Calculates kc for flanges of tubular cross-sections and T-sections [-].

        NEN-EN 1992-1-1:2011 art.7.3.2(2) - Formula (7.3)

        Parameters
        ----------
        f_cr : KN
            [Fcr] Absolute value of the tensile force within the flange immediately before cracking due to the cracking moment calculated with
            fct,eff [kN].
        a_ct : MM2
            [Act] Area of the concrete within the tension zone. The tension zone is that part of the cross-section that, according to the calculation,
            is under tension just before the first crack occurs [mm²].
        f_ct_eff : MPA
            [fc,eff] Average value of the tensile strength of the concrete at the time when the first cracks can be expected [MPa].
        """
        super().__init__()
        self.f_cr = f_cr
        self.a_ct = a_ct
        self.f_ct_eff = f_ct_eff

    @staticmethod
    def _evaluate(
        f_cr: KN,
        a_ct: MM2,
        f_ct_eff: MPA,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if a_ct <= 0:
            raise ValueError("The value of a_ct must be greater than zero.")
        if f_ct_eff <= 0:
            raise ValueError("The value of f_ct_eff must be greater than zero.")
        return max(0.9 * (abs(f_cr) * KN_TO_N / (a_ct * f_ct_eff)), 0.5)
