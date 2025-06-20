"""Formula 5.32 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KNM


class Form5Dot32EquivalentFirstOrderEndMoment(Formula):
    """Class representing formula 5.32 for the calculation of the equivalent first order end moment, [$M_{0e}$]."""

    label = "5.32"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        m_01: KNM,
        m_02: KNM,
    ) -> None:
        r"""[$M_{0e}$] Equivalent first order end moment [$kNm$].

        EN 1992-1-1:2004 art.5.8.8.2(2) - Formula (5.32)

        Parameters
        ----------
        m_01 : KNM
            [$M_{01}$] The smaller first order end moment [$kNm$].
        m_02 : KNM
            [$M_{02}$] The larger first order end moment [$kNm$].
        """
        super().__init__()
        self.m_01 = m_01
        self.m_02 = m_02

    @staticmethod
    def _evaluate(
        m_01: KNM,
        m_02: KNM,
    ) -> KNM:
        """Evaluates the formula, for more information see the __init__ method."""
        if abs(m_02) < abs(m_01):
            raise ValueError("The absolute value of M_02 must be equal to or larger than the absolute value of M_01.")

        return max(0.6 * m_02 + 0.4 * m_01, 0.4 * m_02)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.32."""
        return LatexFormula(
            return_symbol=r"M_{0e}",
            result=f"{self:.{n}f}",
            equation=r"\max\left(0.6 \cdot M_{02} + 0.4 \cdot M_{01}; 0.4 \cdot M_{02}\right)",
            numeric_equation=rf"\max\left(0.6 \cdot {self.m_02:.{n}f} + 0.4 \cdot {self.m_01:.{n}f}; 0.4 \cdot {self.m_02:.{n}f}\right)",
            comparison_operator_label="=",
            unit="kNm",
        )
