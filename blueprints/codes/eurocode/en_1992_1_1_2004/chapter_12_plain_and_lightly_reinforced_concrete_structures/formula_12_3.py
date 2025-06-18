"""Formula 12.3 from EN 1992-1-1:2004: Chapter 12 - Plain and Lightly Reinforced Concrete Structures."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form12Dot3PlainConcreteShearStress(Formula):
    r"""Class representing formula 12.3 for the calculation of the design shear stress of plain concrete,
    :math:`\sigma_{cp}`.

    EN 1992-1-1:2004 art.12.6.3(2) - Formula (12.3)
    """

    label = "12.3"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        n_ed: N,
        a_cc: MM2,
    ) -> None:
        r"""[:math:`\sigma_{cp}`] Design shear stress of plain concrete [:math:`MPa`].

        EN 1992-1-1:2004 art.12.6.3(2) - Formula (12.3)

        Parameters
        ----------
        n_ed : N
            [:math:`N_{Ed}`] Design normal force [:math:`N`].
        a_cc : MM2
            [:math:`A_{cc}`] Compressed area [:math:`mm^2`].
        """
        super().__init__()
        self.n_ed = n_ed
        self.a_cc = a_cc

    @staticmethod
    def _evaluate(
        n_ed: N,
        a_cc: MM2,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(
            a_cc=a_cc,
        )

        raise_if_negative(
            n_ed=n_ed,
        )

        return n_ed / a_cc

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 12.3."""
        return LatexFormula(
            return_symbol=r"\sigma_{cp}",
            result=f"{self:.{n}f}",
            equation=r"\frac{N_{Ed}}{A_{cc}}",
            numeric_equation=rf"\frac{{{self.n_ed:.{n}f}}}{{{self.a_cc:.{n}f}}}",
            comparison_operator_label="=",
        )
