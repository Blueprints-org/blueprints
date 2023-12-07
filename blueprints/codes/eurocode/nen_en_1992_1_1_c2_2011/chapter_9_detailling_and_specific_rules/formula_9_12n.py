"""This package represents the Eurocode NEN-EN 1992-1-1+C2:2011 code - Chapter 9 - formula (9.12N)."""
# pylint: disable=arguments-differ

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import KN, MM2, MPA
from blueprints.unit_conversion import KN_TO_N


class Form9Dot12NMinimumLongitudinalReinforcementColumns(Formula):
    """Class representing the formula 9.12N for the calculation of the minimum longitudinal reinforcement for columns."""

    label = "9.12N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        n_ed: KN,
        f_yd: MPA,
        a_c: MM2,
    ) -> None:
        """[As,min] Minimum longitudinal reinforcement for columns [mm²].

        NEN-EN 1992-1-1+C2:2011 art.9.5.2(5) - Formula (9.12N)

        Parameters
        ----------
        n_ed: KN
            [Ned] Design value of axial force [kN].
        f_yd: MPA
            [fyd] Design yield strength reinforcement steel [MPa].
        a_c: MM2
            [Ac] Concrete cross-sectional area [mm²].
        """
        super().__init__()
        self.n_ed = n_ed
        self.f_yd = f_yd
        self.a_c = a_c

    @staticmethod
    def _evaluate(
        n_ed: KN,
        f_yd: MPA,
        a_c: MM2,
    ) -> MM2:
        """For more detailed documentation see the class docstring."""
        if n_ed < 0:
            raise ValueError(f"Negative n_ed: {n_ed}. n_ed cannot be negative")
        if f_yd < 0:
            raise ValueError(f"Negative f_yd: {f_yd}. f_yd cannot be negative")
        if a_c < 0:
            raise ValueError(f"Negative a_c: {a_c}. a_c cannot be negative")
        return max(0.1 * n_ed * KN_TO_N / f_yd, 0.002 * a_c)
