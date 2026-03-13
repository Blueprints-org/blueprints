"""Formula E.9 from EN 1995-1-1:2023."""

from blueprints.codes.eurocode.en_1995_1_1_2023 import EN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA, NMM, NMM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class FormEDot9BendingStressInILayer(Formula):
    r"""Class representing formula E.9 for bending stress in the i-numbered part of the cross-section."""

    label = "E.9"
    source_document = EN_1995_1_1_2023

    def __init__(self, i: int, e_i: MPA, h_i: MM, m_yd: NMM, ei_ef: NMM2) -> None:
        r"""[$\sigma_{m,i}$] axial stress in the i-numbered part of the cross-section, in [$MPa$].

        EN 1995-1-1:2023 art E.5(1) - Formula (E.9)

        Parameters
        ----------
        i : DIMENSIONLESS
            [$i$] Number of layer i of cross-section.
        e_i : MPA
            [$E_i$] Modulus of elasticity of the i-numbered part of the cross-section [$MPA$].
        h_i : MM
            [$h_i$] Depth of the i-numbered part of the cross-section [$mm$].
        m_yd : NMM
            [$M_{y,d}$] Design bending moment about y-axis [$Nmm$].
        ei_ef : NMM2
            [$(EI)_{ef}$] Effective bending stiffness, in [$Nmm^2$].

        Returns
        -------
        None
        """
        super().__init__()
        self.e_i = e_i
        self.h_i = h_i
        self.m_yd = m_yd
        self.ei_ef = ei_ef
        self.i = i

    @staticmethod
    def _evaluate(i: int, e_i: MPA, h_i: MM, m_yd: NMM, ei_ef: NMM2) -> MPA:
        """Evaluates the formula, for more information see the __init__method."""
        # Ensure that a valid layer number is used
        if i not in {1, 2, 3}:
            raise ValueError("The number of the layer must be either 1, 2 or 3.")

        # Ensure that the input parameters have valid values
        raise_if_less_or_equal_to_zero(e_i=e_i, ei_ef=ei_ef)
        if i != 3:
            raise_if_less_or_equal_to_zero(h_i=h_i)
        else:
            raise_if_negative(h_i=h_i)

        return 0.5 * e_i * h_i * m_yd / ei_ef

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula E.9."""
        eq_i = f"\\frac{{0.5 E_{self.i} h_{self.i} M_{{yd}}}}{{EI_{{ef}}}}"

        repl_symb = {
            f"E_{self.i}": rf"\cdot {self.e_i:.{n}f} \cdot",
            f"h_{self.i}": rf"{self.h_i:.{n}f} \cdot",
            r"M_{yd}": rf"{self.m_yd:.{n}f}",
            r"EI_{ef}": rf"{self.ei_ef:.{n}f}",
        }
        numeric_eq = latex_replace_symbols(eq_i, repl_symb)
        return LatexFormula(
            return_symbol=rf"\sigma_{{{self.i}}}", result=f"{self:.{n}f}", equation=eq_i, numeric_equation=numeric_eq, comparison_operator_label="="
        )
