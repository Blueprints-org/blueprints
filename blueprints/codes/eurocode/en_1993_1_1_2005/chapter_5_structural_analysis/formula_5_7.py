"""Formula 5.7 from EN 1993-1-1:C2_A1_2016: Chapter 5 - Structural Analysis."""

from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM, N
from blueprints.validations import raise_if_negative


class Form5Dot7NeglectFrameTilt(ComparisonFormula):
    r"""Class representing formula 5.7 to check if the tilt of a frame in a building can be neglected or not."""

    label = "5.7"
    source_document = EN_1993_1_1_2005

    def __init__(
            self,
            h_ed: MM,
            v_ed: N
    ) -> None:
        r"""Check if the tilt in a frame in building can be neglected.

        EN 1993-1-1:C2_A1_2016 - Formula (5.7)

        Parameters
        ----------
        h_ed: MM
            [$H_{Ed}$] Design value of the total horizontal load, transferred from the storey. Including equivalent forces according to chapter 5.3.2 (7).

        v_ed: N
            [$V_{Ed}$] Design value of the total vertical load on the frame, transferred from the storey.
        """

        super().__init__()
        self.h_ed = h_ed
        self.v_ed = v_ed

    @staticmethod
    def _evaluate(h_ed: MM, v_ed: N) -> bool:
        """Evaluates the formula"""
        raise_if_negative(h_ed=h_ed, v_ed=v_ed)

        return h_ed >= 0.15 * v_ed

    def latex(self, n: int = 3) -> LatexFormula:
        pass

    @staticmethod
    def _evaluate_lhs(self) -> float:
        return self.v_ed

    @staticmethod
    def _evaluate_rhs(*args, **kwargs) -> float:
        pass

    @property
    def unity_check(self) -> float:
        pass
