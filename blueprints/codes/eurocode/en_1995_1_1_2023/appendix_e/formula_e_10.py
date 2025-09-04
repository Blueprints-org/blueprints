"""Formula E.10 from EN 1995-1-1:2023."""

from blueprints.codes.eurocode.en_1995_1_1_2023 import EN_1995_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA, NMM2, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class FormEDot10ShearStressInLayer2(Formula):
    r"""Class representing formula E.10 for maximum shear stress in the cross-section, in the member web."""

    label = "E.10"
    source_document = EN_1995_1_1_2023

    def __init__(self, gamma_3: DIMENSIONLESS, e_2: MPA, e_3: MPA, a_3: MM2, alpha_2: MM, alpha_3: MM, h_2: MM, b_2: MM, v_d: N, ei_ef: NMM2) -> None:
        r"""[$\tau_{2,max}$] maximum shear stress in the cross-section, in the member web (layer 2), in [$MPa$].

        EN 1995-1-1:2023 art E.5(1) - Formula (E.10)

        Parameters
        ----------
        gamma_3 : DIMENSIONLESS
            [$\gamma_3$] Factor for the efficiency of the mechanical connections of 3-numbered part of cross-section [$-$].
        e_2 : MPA
            [$E_1$] Modulus of elasticity of the 2-numbered part of the cross-section [$MPA$].
        e_3 : MPA
            [$E_2$] Modulus of elasticity of the 3-numbered part of the cross-section [$MPA$].
        a_3 : MM2
            [$A_3$] Area of the 3-numbered part of the cross-section [$mm^2$].
        alpha_2 : MM2
            [$\alpha_2$] Distance between centroid of composite cross-section and centroid of 2-numbered part [$mm^2$].
        alpha_3 : MM2
            [$\alpha_3$] Distance between centroid of composite cross-section and centroid of 2-numbered part [$mm^2$].
        h_2 : MM
            [$h_2$] Depth of the 2-numbered part of the cross-section [$mm$].
        b_2 : MM
            [$b_2$] Width of the 2-numbered part of the cross-section [$mm$].
        v_d : N
            [$V_d$] Maximum design shear force in the member, regardless of the sign [$N$].
        ei_ef : NMM2
            [$(EI)_{ef}$] Effective bending stiffness, in [$Nmm^2$].

        Returns
        -------
        None
        """
        super().__init__()
        self.gamma_3 = gamma_3
        self.e_2 = e_2
        self.e_3 = e_3
        self.a_3 = a_3
        self.alpha_2 = alpha_2
        self.alpha_3 = alpha_3
        self.h_2 = h_2
        self.b_2 = b_2
        self.v_d = v_d
        self.ei_ef = ei_ef

    @staticmethod
    def _evaluate(gamma_3: DIMENSIONLESS, e_2: MPA, e_3: MPA, a_3: MM2, alpha_2: MM, alpha_3: MM, h_2: MM, b_2: MM, v_d: N, ei_ef: NMM2) -> MPA:
        """Evaluates the formula, for more information see the __init__method."""
        # Ensure that the input parameters have valid values
        raise_if_less_or_equal_to_zero(gamma_3=gamma_3, e_2=e_2, e_3=e_3, a_3=a_3, alpha_3=alpha_3, b_2=b_2, h_2=h_2, ei_ef=ei_ef)

        return (gamma_3 * e_3 * a_3 * alpha_3 + 0.5 * e_2 * b_2 * ((alpha_2 + h_2) / 2) ** 2) * v_d / (ei_ef * b_2)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula E.10."""
        eq_i = r"\left[\gamma_3 E_3 A_3 \alpha_3 + 0.5 E_2 b_2 \left(\frac{\alpha_2 + h_2}{2}\right)^2\right] \frac{V_d}{b_{2} EI_{ef}}"

        repl_symb = {
            r"\gamma_3": rf"{self.gamma_3:.{n}f}",
            r"E_2": rf"\cdot {self.e_2:.{n}f} \cdot",
            r"E_3": rf"\cdot {self.e_3:.{n}f} \cdot",
            r"A_3": rf"{self.a_3:.{n}f} \cdot",
            r"\alpha_3": rf"{self.alpha_3:.{n}f}",
            r"\alpha_2": rf"{self.alpha_2:.{n}f}",
            r"h_2": rf"{self.h_2:.{n}f}",
            r"b_{2}": rf"{self.b_2:.{n}f}",
            r"b_2": rf"{self.b_2:.{n}f}",
            r"V_d": rf"{self.v_d:.{n}f}",
            r"EI_{ef}": rf"\cdot {self.ei_ef:.{n}f}",
        }
        numeric_eq = latex_replace_symbols(eq_i, repl_symb)
        return LatexFormula(
            return_symbol=r"\tau_{2,max}", result=f"{self:.{n}f}", equation=eq_i, numeric_equation=numeric_eq, comparison_operator_label="="
        )
