"""Formula E.3 from EN 1995-1-1:2023."""

from blueprints.codes.eurocode.en_1995_1_1_2023 import EN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class FormEDot3DistanceCentroidAlpha1(Formula):
    r"""Class representing formula E.3 for the distance between the centroid of the composite cross-section
    and the centroid of the 1st layer of the cross-section.
    """

    label = "E.3"
    source_document = EN_1995_1_1_2023

    def __init__(self, h_1: MM, h_2: MM, alpha_2: MM) -> None:
        r"""[$\alpha_1$] Distance between the centroid of the composite cross-section and the centroid of layer 1 of the cross-section.

        EN 1995-1-1:2023 art E.4(1) - Formula (E.3)

        Parameters
        ----------
        h_1 : MM
            [$h_1$] Depth of the 1st part of the cross-section [$mm$].
        h_2 : MM
            [$h_2$] Depth of the 2nd part of the cross-section [$mm$].
        alpha_2 : MM
            [$\alpha_2$] Distance between the centroid of the composite cross-section and the centroid of layer 2 of the cross-section.

        Returns
        -------
        None
        """
        super().__init__()
        self.h_1 = h_1
        self.h_2 = h_2
        self.alpha_2 = alpha_2

    @staticmethod
    def _evaluate(h_1: MM, h_2: MM, alpha_2: MM) -> MM:
        """Evaluates the formula, for more information see the __init__method."""
        # Ensure that the input parameters have valid values
        raise_if_less_or_equal_to_zero(h_1=h_1, h_2=h_2)

        return (h_1 + h_2) / 2 - alpha_2

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula E.3."""
        eq_i = r"\frac{h_1 + h_2}{2} - \alpha_2"

        repl_symb = {r"h_1": rf"{self.h_1:.{n}f}", r"h_2": rf"{self.h_2:.{n}f}", r"\alpha_2": rf"\left({self.alpha_2:.{n}f}\right)"}
        numeric_eq = latex_replace_symbols(eq_i, repl_symb)
        return LatexFormula(
            return_symbol=r"\alpha_1", result=f"{self:.{n}f}", equation=eq_i, numeric_equation=numeric_eq, comparison_operator_label="="
        )
