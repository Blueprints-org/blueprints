"""Formula 5.31 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KNM


class Form5Dot31DesignMoment(Formula):
    """Class representing formula 5.31 for the calculation of the design moment, [$M_{Ed}$]."""

    label = "5.31"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        m_0ed: KNM,
        m_2: KNM,
    ) -> None:
        r"""[$M_{Ed}$] Design moment [$kNm$].

        NEN-EN 1992-1-1+C2:2011 art.5.8.8.2(2) - Formula (5.31)

        Parameters
        ----------
        m_0ed : KNM
            [$M_{0Ed}$] First order moment, including the effect of imperfections; see also 5.8.8.2 (2) [$kNm$].
        m_2 : KNM
            [$M_{2}$] Nominal 2nd order moment; see 5.8.8.2 (3) [$kNm$].
        """
        super().__init__()
        self.m_0ed = m_0ed
        self.m_2 = m_2

    @staticmethod
    def _evaluate(
        m_0ed: KNM,
        m_2: KNM,
    ) -> KNM:
        """Evaluates the formula, for more information see the __init__ method."""
        return m_0ed + m_2

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.31."""
        return LatexFormula(
            return_symbol=r"M_{Ed}",
            result=f"{self:.3f}",
            equation=r"M_{0Ed} + M_{2}",
            numeric_equation=rf"{self.m_0ed:.3f} + {self.m_2:.3f}",
            comparison_operator_label="=",
            unit="kNm",
        )
