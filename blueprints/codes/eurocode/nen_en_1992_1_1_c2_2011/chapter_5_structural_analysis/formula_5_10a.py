"""Formula 5.10a from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot10aRedistributionOfMomentsLowerFck:
    r"""Class representing formula 5.10a for the redistribution of moments in continuous beams or slabs when [$f_{ck} \leq 50 MPa$]."""

    label = "5.10a"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, delta: DIMENSIONLESS, k1: DIMENSIONLESS, k2: DIMENSIONLESS, xu: M, d: M) -> None:
        r"""[$\delta$] Redistribution of moments in continuous beams or slabs when [$f_{ck} \leq 50 MPa$].

        NEN-EN 1992-1-1+C2:2011 art.5.5(4) - Formula (5.10a)

        Parameters
        ----------
        delta : DIMENSIONLESS
            [$\delta$] is the ratio of the redistributed moment to the elastic moment.
        k1 : DIMENSIONLESS
            [$k_1$] is a coefficient for redistribution.
        k2 : DIMENSIONLESS
            [$k_2$] is a coefficient for redistribution.
        xu : M
            [$x_u$] is the depth of the compression zone in the ultimate limit state after redistribution.
        d : M
            [$d$] is the effective depth of the section.
        """
        super().__init__()
        self.delta = delta
        self.k1 = k1
        self.k2 = k2
        self.xu = xu
        self.d = d
        raise_if_less_or_equal_to_zero(delta=delta, k1=k1, k2=k2, xu=xu, d=d)

    @property
    def left_hand_side(self) -> DIMENSIONLESS:
        """Calculate the left hand side of the comparison.

        Returns
        -------
        DIMENSIONLESS
            Left hand side of the comparison.
        """
        return self.delta

    @property
    def right_hand_side(self) -> DIMENSIONLESS:
        """Calculate the right hand side of the comparison.

        Returns
        -------
        DIMENSIONLESS
            Right hand side of the comparison.
        """
        raise_if_less_or_equal_to_zero(d=self.d)
        raise_if_less_or_equal_to_zero(xu=self.xu)
        return self.k1 + self.k2 * (self.xu / self.d)

    @property
    def ratio(self) -> DIMENSIONLESS:
        """Ratio between left hand side and right hand side of the comparison, commonly referred to as unity check."""
        return self.left_hand_side / self.right_hand_side

    def __bool__(self) -> bool:
        """Evaluates the comparison, for more information see the __init__ method."""
        return self.left_hand_side >= self.right_hand_side

    def __str__(self) -> str:
        """Return the result of the comparison."""
        return self.latex().complete

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.10a."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\delta \geq k_1 + k_2 \frac{x_u}{d}",
            numeric_equation=rf"{self.left_hand_side:.3f} \geq {self.k1} + {self.k2} \frac{{{self.xu}}}{{{self.d}}}",
            comparison_operator_label=r"\rightarrow",
        )
