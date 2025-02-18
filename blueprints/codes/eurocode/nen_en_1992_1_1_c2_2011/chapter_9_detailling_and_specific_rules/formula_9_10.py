"""Formula 9.10 from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailling and specific rules."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form9Dot10MaximumSpacingBentUpBars(Formula):
    """Class representing the formula 9.10 for the calculation of the maximum longitudinal spacing of bent up bars for slabs."""

    label = "9.10"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, d: MM) -> None:
        r"""[$s_{max}$] Maximum longitudinal spacing of bent up bars for slabs [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.9.3.2(4) - Formula (9.10)

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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 9.10."""
        return LatexFormula(
            return_symbol=r"s_{max}",
            result=f"{self:.2f}",
            equation=r"d",
            numeric_equation=rf"{self.d:.2f}",
            comparison_operator_label="=",
        )
