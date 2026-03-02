"""Formula 8.19 from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot19CheckBendingMoment(Formula):
    r"""Class representing formula 8.19 for the test of the bending moment."""

    label = "8.19"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        m_ed: NMM,
        m_c_rd: NMM,
    ) -> None:
        r"""Check the bending moment.

        EN 1993-1-1:2025 art.8.2.5(1) - Formula (8.19)

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

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.19."""
        _equation: str = r"\left( \frac{M_{Ed}}{M_{c,Rd}} \leq 1 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "M_{Ed}": f"{self.m_ed:.{n}f}",
                "M_{c,Rd}": f"{self.m_c_rd:.{n}f}",
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
