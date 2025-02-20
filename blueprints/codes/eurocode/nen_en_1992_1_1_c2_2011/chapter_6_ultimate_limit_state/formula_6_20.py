"""Formula 6.20 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot20LongitudinalShearStress(Formula):
    r"""Class representing formula 6.20 for the calculation of the longitudinal shear stress, [$v_{Ed}$]."""

    label = "6.20"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        delta_f_d: N,
        h_f: MM,
        delta_x: MM,
    ) -> None:
        r"""[$v_{Ed}$] Longitudinal shear stress [$MPa$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.4(3) - Formula (6.20)

        Parameters
        ----------
        delta_f_d : N
            [$\Delta F_{d}$] Change of the normal force in the flange over the length [$\Delta x$] [$N$].
        h_f : MM
            [$h_{f}$] Thickness of flange at the junctions [$mm$].
        delta_x : MM
            [$\Delta x$] Length under consideration, see Figure 6.7 [$mm$].
        """
        super().__init__()
        self.delta_f_d = delta_f_d
        self.h_f = h_f
        self.delta_x = delta_x

    @staticmethod
    def _evaluate(
        delta_f_d: N,
        h_f: MM,
        delta_x: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_f_d=delta_f_d)
        raise_if_less_or_equal_to_zero(h_f=h_f, delta_x=delta_x)

        return delta_f_d / (h_f * delta_x)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.20."""
        return LatexFormula(
            return_symbol=r"v_{Ed}",
            result=f"{self:.3f}",
            equation=r"\frac{\Delta F_{d}}{h_{f} \cdot \Delta x}",
            numeric_equation=rf"\frac{{{self.delta_f_d:.3f}}}{{{self.h_f:.3f} \cdot {self.delta_x:.3f}}}",
            comparison_operator_label="=",
            unit="MPa",
        )
