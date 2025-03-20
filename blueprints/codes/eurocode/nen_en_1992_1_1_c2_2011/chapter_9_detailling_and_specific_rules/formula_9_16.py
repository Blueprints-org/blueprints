"""Formula 9.16 from NEN-EN 1992-1-1+C2:2011: Chapter 9 - Detailling and specific rules."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, KN_M, M
from blueprints.validations import raise_if_negative


class Form9Dot16MinimumForceOnInternalBeamLine(Formula):
    """Class representing the formula 9.16 for calculating the minimum force on an internal beam line for floors without screeds."""

    label = "9.16"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        q_3: KN_M,
        l_1: M,
        l_2: M,
        q_4: KN,
    ) -> None:
        r"""[$F_{tie}$] Minimum force on an internal beam line [$kN$].

        NEN-EN 1992-1-1+C2:2011 art.9.10.2.3(4) - Formula (9.16)

        Parameters
        ----------
        q_3: KN_M
            [$q_3$] May be found in national annex, recommended value is 20 [$kN/m$].
        l_1: M
            [$l_1$] span length of floor slabs on either side of the beam, see figure 9.15 [$m$].
        l_2: M
            [$l_2$] span length of floor slabs on either side of the beam, see figure 9.15 [$m$].
        q_4: KN
            [$Q_4$] May be found in national annex, recommended value is 70 [$kN$].
        """
        super().__init__()
        self.q_3 = q_3
        self.l_1 = l_1
        self.l_2 = l_2
        self.q_4 = q_4

    @staticmethod
    def _evaluate(
        q_3: KN_M,
        l_1: M,
        l_2: M,
        q_4: KN,
    ) -> KN:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(q_3=q_3, l_1=l_1, l_2=l_2, q_4=q_4)
        return max(q_3 * (l_1 + l_2) / 2, q_4)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 9.16."""
        return LatexFormula(
            return_symbol=r"F_{tie}",
            result=f"{self:.2f}",
            equation=r"min(q_3 \cdot (l_1 + l_2) / 2, Q_4)",
            numeric_equation=rf"min({self.q_3:.2f} \cdot ({self.l_1:.2f} + {self.l_2:.2f}) / 2, {self.q_4:.2f})",
            comparison_operator_label="=",
        )
