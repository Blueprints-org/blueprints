"""Formula 5.7a and 5.7b from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import M
from blueprints.validations import raise_if_negative


class Form5Dot7abFlangeEffectiveFlangeWidth(Formula):
    """Class representing formula 5.7a and formula 5.7b for the calculation of effective flange width of the i-th flange [$b_{eff,i}$].
    See Figure 5.3.
    """

    label = "5.7a, 5.7b"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        b_i: M,
        l_0: M,
    ) -> None:
        r"""[$b_{eff,i}$] Effective flange width of the i-th flange of a beam [$m$].

        NEN-EN 1992-1-1+C2:2011 art.5.3.2.1(3) - Formula (5.7a) and (5.7b)

        Parameters
        ----------
        b_i : M
            [$b_{i}$] Effective flange width of the i-th flange [$m$].
        l_0 : M
            [$l_{0}$] distance between points of zero moment, which may be obtained from Figure 5.2 [$m$].

        Notes
        -----
        This formula is the combination of formula 5.7a and 5.7b. Formula 5.7a and 5.7b cannot be used independently.
        """
        super().__init__()
        self.b_i = b_i
        self.l_0 = l_0

    @staticmethod
    def _evaluate(
        b_i: M,
        l_0: M,
    ) -> M:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            b_i=b_i,
            l_0=l_0,
        )
        return min(0.2 * b_i + 0.1 * l_0, 0.2 * l_0, b_i)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.7ab."""
        return LatexFormula(
            return_symbol=r"b_{eff,i}",
            result=f"{self:.3f}",
            equation=r"0.2b_{i}+0.1l_{0} \le 0.2l_{0}\text{ and }b_{eff,i}\le b_{i}",
            numeric_equation=rf"0.2\cdot{self.b_i}+0.1\cdot{self.l_0} \le 0.2\cdot{self.l_0}\text{{ and }}b_{{eff,i}}\le {self.b_i}",
            comparison_operator_label="=",
        )
