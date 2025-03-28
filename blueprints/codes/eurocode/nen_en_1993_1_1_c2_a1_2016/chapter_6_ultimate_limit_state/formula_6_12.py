"""Formula 6.12 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot12CheckBendingMoment(Formula):
    r"""Class representing formula 6.12 for the test of the bending moment."""

    label = "6.12"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        m_ed: NMM,
        m_c_rd: NMM,
    ) -> None:
        r"""Check the bending moment.

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.4(1) - Formula (6.12)

        Parameters
        ----------
        m_ed : NMM
            [$M_{Ed}$] Design bending moment [$Nmm$].
        m_c_rd : NMM
            [$M_{c,Rd}$] The design resistance for bending about one principal axis of a cross-section [$Nmm$].
        """
        super().__init__()
        self.m_ed = m_ed
        self.m_c_rd = m_c_rd

    @staticmethod
    def _evaluate(
        m_ed: NMM,
        m_c_rd: NMM,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(m_c_rd=m_c_rd)
        raise_if_negative(m_ed=m_ed)

        return m_ed / m_c_rd <= 1

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.12."""
        _equation: str = r"\left( \frac{M_{Ed}}{M_{c,Rd}} \leq 1 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "M_{Ed}": f"{self.m_ed:.3f}",
                "M_{c,Rd}": f"{self.m_c_rd:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
