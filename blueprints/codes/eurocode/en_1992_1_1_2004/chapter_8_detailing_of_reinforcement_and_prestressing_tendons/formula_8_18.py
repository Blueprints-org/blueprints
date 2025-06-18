"""Formula 8.18 from EN 1992-1-1:2004: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form8Dot18DesignValueTransmissionLength2(Formula):
    r"""Class representing formula 8.18 for the calculation of design value 2 of the transmission length [$l_{pt2}$]. The less favourable of
    [$l_{pt1}$] or [$l_{pt2}$] has to be chosen depending on the design situation.
    """

    label = "8.18"
    source_document = EN_1992_1_1_2004

    def __init__(self, l_pt: MM) -> None:
        r"""[$l_{pt2}$] design value 2 of the transmission length [$mm$].

        EN 1992-1-1:2004 art.8.10.2.2(3) - Formula (8.18)

        Parameters
        ----------
        l_pt : MM
            [$l_{pt}$] Basic value of the transmission length [$mm$].
            Use your own implementation for this value or use :class:`Form8Dot16BasicTransmissionLength` class.
        """
        super().__init__()
        self.l_pt = l_pt

    @staticmethod
    def _evaluate(
        l_pt: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(l_pt=l_pt)
        return 1.2 * l_pt

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.18."""
        return LatexFormula(
            return_symbol=r"l_{pt2}",
            result=f"{self:.{n}f}",
            equation=r"1.2 \cdot l_{pt}",
            numeric_equation=rf"1.2 \cdot {self.l_pt:.{n}f}",
            comparison_operator_label="=",
        )
