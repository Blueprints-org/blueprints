"""Formula E.1 from EN 1995-1-1:2023."""

from blueprints.codes.eurocode.en_1995_1_1_2023 import EN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MM4, MPA, NMM2
from blueprints.validations import raise_if_less_or_equal_to_zero


class FormEDot1EffBendingStiffness(Formula):
    r"""Class representing formula E.1 for the effective bending stiffness of mechanically jointed members [$(EI)_{ef}$]."""

    label = "E.1"
    source_document = EN_1995_1_1_2023

    def __init__(self, e_i: list[MPA], i_i: list[MM4], gamma_i: list[DIMENSIONLESS], a_i: list[MM2], alpha_i: list[MM]) -> None:
        r"""[$(EI)_{ef}$] Effective bending stiffness, in [$Nmm^2$].

        EN 1995-1-1:2023 art E.4(1) - Formula (E.1)

        Parameters
        ----------
        e_i : MPA
            [$E_i$] Modulus of elasticity of the i-numbered part of the cross-section [$MPA$].
        i_i : MM4
            [$I_i$] Second moment of inertia of the i-numbered part of the cross-section [$mm^4$].
        gamma_i : DIMENSIONLESS
            [$\gamma_{i}$] Factor for the efficiency of the mechanical connections of the respective i-numbered part of the cross-section [$-$].
        a_i : MM2
            [$A_i$] Area of the i-numbered part of the cross-section [$mm^2$].
        alpha_i : MM
            [$\alpha_i$] Distance between the centroid of the composite cross-section and the centroid of i-numbered part of the cross-section [$mm$].

        Returns
        -------
        None
        """
        super().__init__()
        self.e_i = e_i
        self.i_i = i_i
        self.gamma_i = gamma_i
        self.a_i = a_i
        self.alpha_i = alpha_i
        self.ei_i: list[NMM2] = []

    @staticmethod
    def _evaluate(e_i: list[MPA], i_i: list[MM4], gamma_i: list[DIMENSIONLESS], a_i: list[MM2], alpha_i: list[MM]) -> NMM2:
        """Evaluates the formula, for more information see the __init__ method."""
        prop_lists = [e_i, i_i, gamma_i, a_i, alpha_i]

        # Ensure all lists have the same length (number of layers) and that is either 2 or 3
        lengths = {len(lst) for lst in prop_lists}
        if len(lengths) != 1:
            raise ValueError("All input lists must have the same length.")

        length = lengths.pop()
        if length not in {2, 3}:
            raise ValueError("The length of the lists/layers must be either 2 or 3.")

        for name, lst in [("e_i", e_i), ("i_i", i_i), ("gamma_i", gamma_i), ("a_i", a_i)]:
            for i, val in enumerate(lst):
                raise_if_less_or_equal_to_zero(**{f"{name}[{i}]": val})
        ei_i = []
        for i in range(len(e_i)):
            term = e_i[i] * i_i[i] + gamma_i[i] * e_i[i] * a_i[i] * alpha_i[i] ** 2
            ei_i.append(term)
        return sum(ei_i)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula E.1."""
        part_eq_form = [rf"(E_{i + 1} I_{i + 1} + \gamma_{i + 1} E_{i + 1} A_{i + 1} \alpha_{i + 1}^2)" for i in range(len(self.e_i))]
        eq_form = " + ".join(part_eq_form)

        e_istr = {f"E_{i + 1}": rf"{val:.{n}f} \cdot" for i, val in enumerate(self.e_i)}
        i_istr = {f"I_{i + 1}": rf"{val:.{n}f}" for i, val in enumerate(self.i_i)}
        gamma_istr = {rf"\gamma_{i + 1}": rf"{val:.{n}f} \cdot" for i, val in enumerate(self.gamma_i)}
        a_istr = {rf"A_{i + 1}": rf"{val:.{n}f}" for i, val in enumerate(self.a_i)}
        alpha_istr = {rf"\alpha_{i + 1}": rf"\cdot {val:.{n}f}" for i, val in enumerate(self.alpha_i)}

        repl_symb = e_istr | i_istr | gamma_istr | a_istr | alpha_istr
        return LatexFormula(
            return_symbol=r"(EI)_{ef}",
            result=f"{self:.{n}f}",
            equation=eq_form,
            numeric_equation=latex_replace_symbols(eq_form, repl_symb, unique_symbol_check=False),
            comparison_operator_label="=",
        )
