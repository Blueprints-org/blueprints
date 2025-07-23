"""Formula 6.31 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM
from blueprints.validations import raise_if_negative


class Form6Dot31CheckBendingAndAxialForce(Formula):
    r"""Class representing formula 6.31 for bending and axial force."""

    label = "6.31"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        m_ed: NMM,
        m_n_rd: NMM,
    ) -> None:
        r"""Check the bending and axial force criterion.

        EN 1993-1-1:2005 art.6.2.9.1 - Formula (6.31)

        Parameters
        ----------
        m_ed : NMM
            [$M_{Ed}$] Design value of the applied bending moment [$Nmm$].
        m_n_rd : NMM
            [$M_{N,Rd}$] Design plastic moment resistance reduced due to the axial force $N_{Ed}$ [$Nmm$].
        """
        super().__init__()
        self.m_ed = m_ed
        self.m_n_rd = m_n_rd

    @staticmethod
    def _evaluate(
        m_ed: NMM,
        m_n_rd: NMM,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(m_ed=m_ed, m_n_rd=m_n_rd)

        return m_ed <= m_n_rd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.31."""
        _equation: str = r"M_{Ed} \leq M_{N,Rd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                "M_{Ed}": f"{self.m_ed:.{n}f}",
                "M_{N,Rd}": f"{self.m_n_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                "M_{Ed}": rf"{self.m_ed:.{n}f} \ Nmm",
                "M_{N,Rd}": rf"{self.m_n_rd:.{n}f} \ Nmm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="\\to",
            unit="",
        )
