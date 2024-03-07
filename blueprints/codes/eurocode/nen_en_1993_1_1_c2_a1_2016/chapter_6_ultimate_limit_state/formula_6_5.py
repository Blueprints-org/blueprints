"""Formula 6.5 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate limit state."""

# pylint: disable=arguments-differ
from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.type_alias import KN, RATIO
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


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
    ) -> RATIO:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_t_rd=n_t_rd)
        raise_if_negative(n_ed=n_ed)
        return n_ed / n_t_rd
