"""Formula E.7 from EN 1995-1-1:2023."""

from blueprints.codes.eurocode.en_1995_1_1_2023 import EN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM4
from blueprints.validations import raise_if_less_or_equal_to_zero


class FormEDot7SecondMomentInertia(Formula):
    r"""Class representing formula E.7 for second moment of inertia of the i-numbered part of the cross-section."""

    label = "E.7"
    source_document = EN_1995_1_1_2023

    def __init__(self, b_i: MM, h_i: MM, i: int) -> None:
        r"""[$I_i$] Second moment of inertia of the i-numbered part of the cross-section, in [$mm^4$].

        EN 1995-1-1:2023 art E.4(1) - Formula (E.7)

        Parameters
        ----------
        b_i : MM
            [$b_i$] Width of the i-numbered part of the cross-section [$mm$].
        h_i : MM
            [$h_2$] Depth of the i-numbered part of the cross-section [$mm$].
        i : DIMENSIONLESS
            [$i$] Number of layer i of cross-section.

        Returns
        -------
        None
        """
        super().__init__()
        self.b_i = b_i
        self.h_i = h_i
        self.i = i

    @staticmethod
    def _evaluate(b_i: MM, h_i: MM, i: int) -> MM4:
        """Evaluates the formula, for more information see the __init__method."""
        # Ensure that a valid layer number is used
        if i not in {1, 2, 3}:
            raise ValueError("The number of the layer must be either 1, 2 or 3.")

        # Ensure that the input parameters have valid values
        raise_if_less_or_equal_to_zero(b_i=b_i, h_i=h_i)

        return (b_i * h_i**3) / 12

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula E.7."""
        eq_i = f"\\frac{{b_{self.i} h_{self.i}^3}}{{12}}"

        repl_symb = {
            f"b_{self.i}": rf"{self.b_i:.{n}f} \cdot",
            f"h_{self.i}": rf"{self.h_i:.{n}f}",
        }
        numeric_eq = latex_replace_symbols(eq_i, repl_symb)
        return LatexFormula(
            return_symbol=f"I_{self.i}", result=f"{self:.{n}f}", equation=eq_i, numeric_equation=numeric_eq, comparison_operator_label="="
        )
