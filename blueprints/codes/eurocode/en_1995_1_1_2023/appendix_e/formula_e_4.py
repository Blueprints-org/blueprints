"""Formula E.4 from EN 1995-1-1:2023."""

from blueprints.codes.eurocode.en_1995_1_1_2023 import EN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MM4, MPA, NMM2
from blueprints.validations import raise_if_less_or_equal_to_zero


class FormEDot4DistanceToCentroidA2(Formula):
    r"""[$\alpha_2$] Distance between the centroid of the composite cross-section and the centroid of layer 2 of the cross-section."""

    label = "E.4"
    source_document = EN_1995_1_1_2023

    def __init__(self, e_i: list[MPA], a_i: list[MM2], gamma_i: list[DIMENSIONLESS], h_i: list[MM]) -> None:
        r"""[$(\alpha)_{2}$] Effective bending stiffness, in [$Nmm^2$].

        EN 1995-1-1:2023 art E.4(1) - Formula (E.1)

        Parameters
        ----------
        e_i : MPA
            [$E_i$] Modulus of elasticity of the i-numbered part of the cross-section [$MPA$].
        a_i : MM2
            [$A_i$] Area of the i-numbered part of the cross-section [$mm^2$].
        gamma_i : DIMENSIONLESS
            [$\gamma_{i}$] Factor for the efficiency of the mechanical connections of the respective i-numbered part of the cross-section [$-$].
        h_i : MM
            [$h_i$] Depth of the i-th part of the cross-section [$mm$].

        Returns
        -------
        None
        """
        super().__init__()
        self.e_i = e_i
        self.gamma_i = gamma_i
        self.a_i = a_i
        self.h_i = h_i

    @staticmethod
    def _evaluate(e_i: list[MPA], a_i: list[MM4], gamma_i: list[DIMENSIONLESS], h_i: list[MM]) -> NMM2:
        """Evaluates the formula, for more information see the __init__ method."""
        prop_lists = [e_i, gamma_i, a_i, h_i]
        n_low = 2
        n_up = 3

        # Ensure all lists have the same length (number of layers) and that is either 2 or 3
        lengths = {len(lst) for lst in prop_lists}
        if len(lengths) != 1:
            raise ValueError("All input lists must have the same length.")

        length = lengths.pop()
        if length not in {n_low, n_up}:
            raise ValueError("The length of the lists/layers must be either 2 or 3.")

        for name, lst in [("e_i", e_i), ("a_i", a_i), ("gamma_i", gamma_i), ("h_i", h_i)]:
            for i, val in enumerate(lst):
                raise_if_less_or_equal_to_zero(**{f"{name}[{i}]": val})
        den = []
        for i in range(len(e_i)):
            term = gamma_i[i] * e_i[i] * a_i[i]
            den.append(term)
        denom = sum(den)
        if len(e_i) == n_low:
            alpha_2 = 1 / (2 * denom) * (gamma_i[0] * e_i[0] * a_i[0] * (h_i[0] + h_i[1]))
        else:
            alpha_2 = 1 / (2 * denom) * (gamma_i[0] * e_i[0] * a_i[0] * (h_i[0] + h_i[1]) - gamma_i[2] * e_i[2] * a_i[2] * (h_i[1] + h_i[2]))
        return alpha_2

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula E.4."""
        n_up = 3
        den_eq_form = " + ".join([rf"\gamma_{i + 1} E_{i + 1} A_{i + 1}" for i in range(len(self.e_i))])
        denom = rf"2 \left({den_eq_form}\right)"

        numerator = r"\gamma_1 E_1 A_1 (h_1 + h_2)"
        if len(self.e_i) == n_up:
            numerator += r" - \gamma_3 E_3 A_3 (h_2 + h_3)"

        eq_form = rf"\frac{{{numerator}}}{{{denom}}}"

        e_istr = {f"E_{i + 1}": rf"{val:.{n}f} \cdot" for i, val in enumerate(self.e_i)}
        a_istr = {f"A_{i + 1}": rf"{val:.{n}f}" for i, val in enumerate(self.a_i)}
        gamma_istr = {rf"\gamma_{i + 1}": rf"{val:.{n}f} \cdot" for i, val in enumerate(self.gamma_i)}
        h_istr = {rf"h_{i + 1}": rf"{val:.{n}f}" for i, val in enumerate(self.h_i)}

        repl_symb = e_istr | a_istr | gamma_istr | h_istr
        return LatexFormula(
            return_symbol=r"\alpha_{2}",
            result=f"{self:.{n}f}",
            equation=eq_form,
            numeric_equation=latex_replace_symbols(eq_form, repl_symb, unique_symbol_check=False),
            comparison_operator_label="=",
        )
