"""Formula E.2 from EN 1995-1-1:2023."""

import math

from blueprints.codes.eurocode.en_1995_1_1_2023 import EN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA, N_MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class FormEDot2MechanicalConnectEfficiencyFactor(Formula):
    r"""Class representing formula E.2 for the factors for the efficiency of the mechanical \\
        connections of the respective i-numbered parts of the cross-section.
    """

    label = "E.2"
    source_document = EN_1995_1_1_2023

    def __init__(self, i: DIMENSIONLESS, e_i: MPA, a_i: MM2, s_i: MM, k_i: N_MM, length: MM) -> None:
        r"""[$\gamma_i$] Factor for the efficiency of the mechanical connections of the respective i-numbered parts of the cross-section.

        EN 1995-1-1:2023 art E.4(1) - Formula (E.2)

        Parameters
        ----------
        i : DIMENSIONLESS
            [$i$] Number of layer [$-$].
        e_i : MPA
            [$E_i$] Modulus of elasticity of the i-numbered part of the cross-section [$MPA$].
        a_i : MM2
            [$A_i$] Area of the i-numbered part of the cross-section [$mm^2$].
        s_i : MM
            [$s_i$] Spacing between the connections, for i=1 and i=3 [$mm$].
                    For this formula implementation s_2 for i=2 needs to be given too, but it won't be used.
        k_i : N_MM
            [$K_i$] Stiffness of connectors, according to the limit state under consideration [$N/mm$].
        length : MM
            [$l$] Span of the member [$mm$].

        Returns
        -------
        None
        """
        super().__init__()
        self.i = i
        self.e_i = e_i
        self.a_i = a_i
        self.s_i = s_i
        self.k_i = k_i
        self.length = length

    @staticmethod
    def _evaluate(i: int, e_i: MPA, a_i: MM2, s_i: MM, k_i: N_MM, length: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__method."""
        # Ensure that a valid layer number is used
        if i not in {1, 2, 3}:
            raise ValueError("The number of the layer must be either 1, 2 or 3.")

        # Ensure that the input parameters have valid values
        raise_if_less_or_equal_to_zero(length=length, e_i=e_i, a_i=a_i, s_i=s_i, k_i=k_i)

        l_2 = 2

        return 1 if i == l_2 else 1 / (1 + math.pi**2 * e_i * a_i * s_i / (k_i * length**2))

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula E.2."""
        l_2 = 2
        if self.i == l_2:
            eq_i = f"{self:.{n}f}"
            numeric_eq = f"{self:.{n}f}"
        else:
            eq_i = f"\\frac{{1}}{{1+\\frac{{\\pi^2 E_{self.i} A_{self.i} s_{self.i}}}{{K_{self.i} l^2}}}}"

            e_istr = {f"E_{self.i}": rf"{self.e_i:.{n}f} \cdot"}
            a_istr = {f"A_{self.i}": rf"{self.a_i:.{n}f} \cdot"}
            s_istr = {f"s_{self.i}": rf"{self.s_i:.{n}f}"}
            k_istr = {f"K_{self.i}": rf"{self.k_i:.{n}f} \cdot"}
            l_str = {"l": f"{self.length:.{n}f}"}
            repl_symb = e_istr | a_istr | s_istr | k_istr | l_str
            numeric_eq = latex_replace_symbols(eq_i, repl_symb)
        return LatexFormula(
            return_symbol=f"\\gamma_{self.i}",
            result=f"{self:.{n}f}",
            equation=eq_i,
            numeric_equation=numeric_eq,
            comparison_operator_label="=",
        )
