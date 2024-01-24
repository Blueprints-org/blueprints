"""Formula 6.5 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate limit state."""
# pylint: disable=arguments-differ
from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.type_alias import KN


class Form6Dot5UnityCheckTensileStrength(Formula):
    """Class representing formula 6.5 for the unity check for tensile strength."""

    label = "6.5"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        n_ed: KN,
        n_t_rd: KN,
    ) -> None:
        """[N_ed/N_t_rd] Unity check for tensile strength of an element in tension.

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.3(1) - Formula (6.5)

        Parameters
        ----------
        n_ed : KN
            [NEd] Design value of the normal tensile force [kN].
        n_t_rd : KN
            [Nt,Rd] Design value of the resistance against tenslie force [kN].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_t_rd = n_t_rd

    @staticmethod
    def _evaluate(
        n_ed: KN,
        n_t_rd: KN,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        if n_t_rd <= 0:
            raise ValueError(f"Negative or zero n_t_rd: {n_t_rd}. n_t_rd cannot zero or be negative")
        if n_ed < 0:
            raise ValueError(f"Negative n_ed: {n_ed}. n_ed cannot be negative (that would be compression).")
        return n_ed / n_t_rd
