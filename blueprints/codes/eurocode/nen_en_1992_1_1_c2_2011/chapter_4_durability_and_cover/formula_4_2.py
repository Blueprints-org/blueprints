"""Formula 4.2 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement."""
# pylint: disable=arguments-differ

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.type_alias import MM


class Form4Dot2MinimumConcreteCover(Formula):
    """Class representing the formula 4.2 for the calculation of the minimum concrete cover [mm]."""

    label = "4.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c_min_b: MM,
        c_min_dur: MM,
        delta_c_dur_gamma: MM,
        delta_c_dur_st: MM,
        delta_c_dur_add: MM,
    ) -> None:
        """[cmin] Calculates the minimum concrete cover [mm].

        NEN-EN 1992-1-1+C2:2011 art.4.4.1.2 (2) - formula (4.2)

        Parameters
        ----------
        c_min_b: MM
            [cminb] The minimum concrete cover based on the adhesion requirements based on art. 4.4.1.2 (3) [mm].
        c_min_dur: MM
            [cmindur] The minimum concrete cover based on environmental conditions based on art. 4.4.1.2 (5) [mm].
        delta_c_dur_gamma: MM
            [Δcdurgamma] An additional safety requirement based on art. 4.4.1.2 (6) [mm].
        delta_c_dur_st: MM
            [Δcdurst] A reduction of minimum concrete cover when using stainless steel based on art. 4.4.1.2 (7) [mm].
        delta_c_dur_add: MM
            [Δcduradd] A reduction of minimum concrete cover when using additional protection based on art. 4.4.1.2 (8) [mm].
        """
        super().__init__()
        self.c_min_b = c_min_b
        self.c_min_dur = c_min_dur
        self.delta_c_dur_gamma = delta_c_dur_gamma
        self.delta_c_dur_st = delta_c_dur_st
        self.delta_c_dur_add = delta_c_dur_add

    @staticmethod
    def _evaluate(
        c_min_b: MM,
        c_min_dur: MM,
        delta_c_dur_gamma: MM,
        delta_c_dur_st: MM,
        delta_c_dur_add: MM,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        if c_min_b < 0:
            raise ValueError(f"Negative c_min_b: {c_min_b}. c_min_b cannot be negative")
        if c_min_dur < 0:
            raise ValueError(f"Negative c_min_dur: {c_min_dur}. c_min_dur cannot be negative")
        if delta_c_dur_gamma < 0:
            raise ValueError(f"Negative delta_c_dur_gamma: {delta_c_dur_gamma}. delta_c_dur_gamma cannot be negative")
        if delta_c_dur_st < 0:
            raise ValueError(f"Negative delta_c_dur_st: {delta_c_dur_st}. delta_c_dur_st cannot be negative")
        if delta_c_dur_add < 0:
            raise ValueError(f"Negative delta_c_dur_add: {delta_c_dur_add}. delta_c_dur_add cannot be negative")
        return max(c_min_b, c_min_dur + delta_c_dur_gamma - delta_c_dur_st - delta_c_dur_add, 10)
