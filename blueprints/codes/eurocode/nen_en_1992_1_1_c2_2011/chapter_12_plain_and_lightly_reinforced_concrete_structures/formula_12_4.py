"""Formula 12.4 from NEN-EN 1992-1-1+C2:2011: Chapter 12 - Plain and Lightly Reinforced Concrete Structures."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form12Dot4PlainConcreteShearStress(Formula):
    r"""Class representing formula 12.4 for the calculation of the design shear stress of plain concrete, :math:`\tau_{cp}`.

    NEN-EN 1992-1-1+C2:2011 art.12.6.3 - Formula (12.4)
    """

    label = "12.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        k: float,
        v_ed: N,
        a_cc: MM2,
    ) -> None:
        r"""[:math:`\tau_{cp}`] Design shear stress of plain concrete [:math:`MPa`].

        NEN-EN 1992-1-1+C2:2011 art.12.6.3 - Formula (12.4)

        Parameters
        ----------
        k : float
            [:math:`k`] Nationally determined parameter [-].
        v_ed : N
            [:math:`V_{Ed}`] Design shear force [:math:`N`].
        a_cc : MM2
            [:math:`A_{cc}`] Compressed area [:math:`mm^2`].
        """
        super().__init__()
        self.k = k
        self.v_ed = v_ed
        self.a_cc = a_cc

    @staticmethod
    def _evaluate(
        k: float,
        v_ed: N,
        a_cc: MM2,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            v_ed=v_ed,
            a_cc=a_cc,
        )
        raise_if_less_or_equal_to_zero(
            v_ed=v_ed,
            a_cc=a_cc,
        )
        return k * v_ed / a_cc

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 12.4."""
        return LatexFormula(
            return_symbol=r"\tau_{cp}",
            result=f"{self:.3f}",
            equation=r"k \cdot \frac{V_{Ed}}{A_{cc}}",
            numeric_equation=rf"{self.k:.3f} \cdot \frac{{{self.v_ed:.3f}}}{{{self.a_cc:.3f}}}",
            comparison_operator_label="=",
        )
