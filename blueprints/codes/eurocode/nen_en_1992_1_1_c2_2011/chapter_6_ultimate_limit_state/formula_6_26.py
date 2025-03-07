"""Formula 6.26 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM2, N_MM, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot26ShearStressInWall(Formula):
    r"""Class representing formula 6.26 for the calculation of the shear stress in a wall of a section
    subject to a pure torsional moment multiplied with the effective thickness [$\tau_{t,i}t_{ef,i}$].
    """

    label = "6.26"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        t_ed: NMM,
        a_k: MM2,
    ) -> None:
        r"""[$\tau_{t,i}t_{ef,i}$] Shear stress in a wall of a section subject to a pure torsional moment multiplied with the
        effective thickness [$N/m$].

        NEN-EN 1992-1-1+C2:2011 art.6.3.2(1) - Formula (6.26)

        Parameters
        ----------
        t_ed : NMM
            [$T_{Ed}$] Applied design torsion [$Nmm$].
        a_k : MM2
            [$A_k$] Area enclosed by the centre-lines of the connecting walls, including inner hollow areas [$mm^2$].
        """
        super().__init__()
        self.t_ed = t_ed
        self.a_k = a_k

    @staticmethod
    def _evaluate(
        t_ed: NMM,
        a_k: MM2,
    ) -> N_MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(a_k=a_k)
        raise_if_negative(t_ed=t_ed)

        return t_ed / (2 * a_k)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.26."""
        return LatexFormula(
            return_symbol=r"\tau_{t,i}t_{ef,i}",
            result=f"{self:.3f}",
            equation=r"\frac{T_{Ed}}{2 \cdot A_{k}}",
            numeric_equation=rf"\frac{{{self.t_ed:.3f}}}{{2 \cdot {self.a_k:.3f}}}",
            comparison_operator_label="=",
            unit="N/mm",
        )
