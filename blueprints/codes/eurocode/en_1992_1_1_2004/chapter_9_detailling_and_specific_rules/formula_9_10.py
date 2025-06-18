"""Formula 9.10 from EN 1992-1-1:2004: Chapter 9 - Detailling and specific rules."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form9Dot10MaximumSpacingBentUpBars(Formula):
    """Class representing the formula 9.10 for the calculation of the maximum longitudinal spacing of bent up bars for slabs."""

    label = "9.10"
    source_document = EN_1992_1_1_2004

    def __init__(self, d: MM) -> None:
        r"""[$s_{max}$] Maximum longitudinal spacing of bent up bars for slabs [$mm$].

        EN 1992-1-1:2004 art.9.3.2(4) - Formula (9.10)

        Parameters
        ----------
        d: MM
            [$d$] Effective height of the cross-section [$mm$].
        """
        super().__init__()
        self.d = d

    @staticmethod
    def _evaluate(d: MM) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(d=d)
        return d

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 9.10."""
        return LatexFormula(
            return_symbol=r"s_{max}",
            result=f"{self:.{n}f}",
            equation=r"d",
            numeric_equation=rf"{self.d:.{n}f}",
            comparison_operator_label="=",
        )
