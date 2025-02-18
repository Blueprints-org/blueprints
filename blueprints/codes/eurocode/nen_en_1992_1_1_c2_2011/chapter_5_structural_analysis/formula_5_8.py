"""Formula 5.8 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import M
from blueprints.validations import raise_if_negative


class Form5Dot8EffectiveSpan(Formula):
    """Class representing formula 5.8 for calculating the effective span of beams and slabs, [$l_{eff}$].

    See Figure 5.4
    """

    label = "5.8"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        l_n: M,
        a_1: M,
        a_2: M,
    ) -> None:
        r"""[$l_{eff}$] the effective span of a member [$m$].

        NEN-EN 1992-1-1+C2:2011 art.5.3.2.2(1) - Formula (5.8)

        Parameters
        ----------
        l_n : M
            [$l_{n}$] clear distance between the faces of the supports [$m$].
        a_1 : M
            [$a_{1}$] values for [$a_{1}$] and [$a_{2}$] at each end of the span, may be determined from the appropriate [$a_{i}$]
                            values in Figure 5.4 where t is the width of the supporting element as shown. [$m$].
        a_2 : M
            [$a_{2}$] values for [$a_{1}$] and [$a_{2}$] at each end of the span, may be determined from the appropriate [$a_{i}$]
                            values in Figure 5.4 where t is the width of the supporting element as shown. [$m$].
        """
        super().__init__()
        self.l_n = l_n
        self.a_1 = a_1
        self.a_2 = a_2

    @staticmethod
    def _evaluate(
        l_n: M,
        a_1: M,
        a_2: M,
    ) -> M:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            l_n=l_n,
            a_1=a_1,
            a_2=a_2,
        )
        return l_n + a_1 + a_2

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.8."""
        return LatexFormula(
            return_symbol=r"l_{eff}",
            result=f"{self:.3f}",
            equation=r"l_{n} + a_{1} + a_{2}",
            numeric_equation=f"{self.l_n:.3f} + {self.a_1:.3f} + {self.a_2:.3f}",
            comparison_operator_label="=",
        )
