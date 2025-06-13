"""Formula 6.24 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot24DesignShearStress(Formula):
    r"""Class representing formula 6.24 for the calculation of the design shear stress in the interface, [$v_{Edi}$]."""

    label = "6.24"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        beta: DIMENSIONLESS,
        v_ed: N,
        z: MM,
        b_i: MM,
    ) -> None:
        r"""[$v_{Edi}$] Design shear stress in the interface [$MPa$].

        EN 1992-1-1:2004 art.6.2.5(1) - Formula (6.24)

        Parameters
        ----------
        beta : DIMENSIONLESS
            [$\beta$] Ratio of the longitudinal force in the new concrete area and the total longitudinal force either in
            the compression or tension zone, both calculated for the section considered [$-$].
        v_ed : N
            [$V_{Ed}$] Transverse shear force [$N$].
        z : MM
            [$z$] Lever arm of composite section [$mm$].
        b_i : MM
            [$b_{i}$] Width of the interface (see Figure 6.8) [$mm$].
        """
        super().__init__()
        self.beta = beta
        self.v_ed = v_ed
        self.z = z
        self.b_i = b_i

    @staticmethod
    def _evaluate(
        beta: DIMENSIONLESS,
        v_ed: N,
        z: MM,
        b_i: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            beta=beta,
            v_ed=v_ed,
        )
        raise_if_less_or_equal_to_zero(z=z, b_i=b_i)

        return beta * v_ed / (z * b_i)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.24."""
        return LatexFormula(
            return_symbol=r"v_{Edi}",
            result=f"{self:.{n}f}",
            equation=r"\beta \cdot \frac{V_{Ed}}{z \cdot b_{i}}",
            numeric_equation=rf"{self.beta:.{n}f} \cdot \frac{{{self.v_ed:.{n}f}}}{{{self.z:.{n}f} \cdot {self.b_i:.{n}f}}}",
            comparison_operator_label="=",
            unit="MPa",
        )
