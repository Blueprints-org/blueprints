"""Formula E.5 from EN 1995-1-1:2023."""

from blueprints.codes.eurocode.en_1995_1_1_2023 import EN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class FormEDot5DistanceCentroidAlpha3(Formula):
    r"""Class representing formula E.5 for the distances between the centroid of the composite cross-section
    and the centroids of i-numbered parts of the cross-section.
    """

    label = "E.5"
    source_document = EN_1995_1_1_2023

    def __init__(self, h_2: MM, h_3: MM, alpha_2: MM) -> None:
        r"""[$\alpha_3$] Distance between the centroid of the composite cross-section and the centroid of layer 1 of the cross-section.

        EN 1995-1-1:2023 art E.4(1) - Formula (E.5)

        Parameters
        ----------
        h_2 : MM
            [$h_2$] Depth of the 2nd part of the cross-section [$mm$].
        h_3 : MM
            [$h_3$] Depth of the 3rd part of the cross-section [$mm$].
        alpha_2 : MM
            [$\alpha_2$] Distance between the centroid of the composite cross-section and the centroid of layer 2 of the cross-section.

        Returns
        -------
        None
        """
        super().__init__()
        self.h_2 = h_2
        self.h_3 = h_3
        self.alpha_2 = alpha_2

    @staticmethod
    def _evaluate(h_2: MM, h_3: MM, alpha_2: MM) -> MM:
        """Evaluates the formula, for more information see the __init__method."""
        # Ensure that the input parameters have valid values
        raise_if_less_or_equal_to_zero(h_2=h_2, h_3=h_3)

        return (h_2 + h_3) / 2 - alpha_2

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula E.5."""
        eq_i = r"\frac{h_2 + h_3}{2} - \alpha_2"

        repl_symb = {r"h_2": rf"{self.h_2:.{n}f}", r"h_3": rf"{self.h_3:.{n}f}", r"\alpha_2": rf"\left({self.alpha_2:.{n}f}\right)"}
        numeric_eq = latex_replace_symbols(eq_i, repl_symb)
        return LatexFormula(
            return_symbol=r"\alpha_3", result=f"{self:.{n}f}", equation=eq_i, numeric_equation=numeric_eq, comparison_operator_label="="
        )
