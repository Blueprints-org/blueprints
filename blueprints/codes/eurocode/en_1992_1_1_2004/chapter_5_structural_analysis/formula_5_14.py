"""Formula 5.14 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, M
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot14SlendernessRatio(Formula):
    r"""Class representing formula 5.14 for the calculation of the slenderness ratio, [$\lambda$]."""

    label = "5.14"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        l_0: M,
        i: M,
    ) -> None:
        r"""[$\lambda$] Slenderness ratio [$-$].

        EN 1992-1-1:2004 art.5.8.3.2(1) - Formula (5.14)

        Parameters
        ----------
        l_0 : M
            [$l_{0}$] Effective length [$m$].
            Use your own implementation of this value or use :class: `Form5Dot15EffectiveLengthBraced`
            or :class: `Form5Dot15EffectiveLengthUnbraced`.
        i : M
            [$i$] Radius of gyration of the uncracked concrete section [$m$].
        """
        super().__init__()
        self.l_0 = l_0
        self.i = i

    @staticmethod
    def _evaluate(
        l_0: M,
        i: M,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(
            l_0=l_0,
            i=i,
        )
        return l_0 / i

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.14."""
        return LatexFormula(
            return_symbol=r"λ",
            result=f"{self:.{n}f}",
            equation=r"\frac{l_0}{i}",
            numeric_equation=rf"\frac{{{self.l_0:.{n}f}}}{{{self.i:.{n}f}}}",
            comparison_operator_label="=",
        )
