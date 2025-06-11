"""Formula 5.39 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KNM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot39SimplifiedCriterionBiaxialBending(Formula):
    r"""Class representing formula 5.39 for simplified criterion for biaxial bending."""

    label = "5.39"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        m_edz: KNM,
        m_rdz: KNM,
        m_edy: KNM,
        m_rdy: KNM,
        a: DIMENSIONLESS,
    ) -> None:
        r"""Simplified criterion for biaxial bending.

        NEN-EN 1992-1-1+C2:2011 art.5.8.9(4) - Formula (5.39)

        Parameters
        ----------
        m_edz : KNM
            [$M_{Edz}$] Design moment including second order moment in z-direction [$kNm$].
        m_rdz : KNM
            [$M_{Rdz}$] Design moment resistance in z-direction [$kNm$].
        m_edy : KNM
            [$M_{Edy}$] Design moment including second order moment in y-direction [$kNm$].
        m_rdy : KNM
            [$M_{Rdy}$] Design moment resistance in y-direction [$kNm$].
        a : DIMENSIONLESS
            [$a$] Exponent for the interaction formula, for circular and elliptical cross sections: a = 2, for rectangular see table [-].
        """
        super().__init__()
        self.m_edz = m_edz
        self.m_rdz = m_rdz
        self.m_edy = m_edy
        self.m_rdy = m_rdy
        self.a = a

    @staticmethod
    def _evaluate(
        m_edz: KNM,
        m_rdz: KNM,
        m_edy: KNM,
        m_rdy: KNM,
        a: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(m_edz=m_edz, m_edy=m_edy)
        raise_if_less_or_equal_to_zero(m_rdz=m_rdz, m_rdy=m_rdy, a=a)

        return (m_edz / m_rdz) ** a + (m_edy / m_rdy) ** a <= 1

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.39."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\left( \frac{M_{Edz}}{M_{Rdz}} \right)^{a} + \left( \frac{M_{Edy}}{M_{Rdy}} \right)^{a} \leq 1",
            numeric_equation=rf"\left( \frac{{{self.m_edz:.3f}}}{{{self.m_rdz:.3f}}} \right)^{{{self.a:.3f}}} + "
            rf"\left( \frac{{{self.m_edy:.3f}}}{{{self.m_rdy:.3f}}} \right)^{{{self.a:.3f}}} \leq 1",
            comparison_operator_label="\\to",
            unit="",
        )
