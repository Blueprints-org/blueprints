"""Formula 5.7 from EN 1993-1-1:C2_A1_2016: Chapter 5 - Structural Analysis."""

from blueprints.codes.formula import Formula
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.type_alias import MM, N
from blueprints.validations import raise_if_negative


class Form5Dot7NeglectFrameTilt(Formula):
    r"""Class representing formula 5.7 to check if the tilt of a frame in a building can be neglected or not."""

    label = "5.7"
    source_document = EN_1993_1_1_2005

    def __init__(
            self,
            h_ed: MM,
            v_ed: N
    ) -> None:
        r"""Check if tilt can be neglected with 'latex formula'

        EN 1993-1-1:C2_A1_2016 - Formula (5.7)

        Parameters
        ----------
        h_ed: MM
            [latex] Description

        v_ed: N
            [latex] Description

        """

        super().__init__()
        self.h_ed = h_ed
        self.v_ed = v_ed

    @staticmethod
    def _evaluate(
            h_ed: MM,
            v_ed: N
    ) -> bool:
        """Evaluates the formula"""
        raise_if_negative(h_ed=h_ed, v_ed=v_ed)

        return h_ed >= 0.15 * v_ed
