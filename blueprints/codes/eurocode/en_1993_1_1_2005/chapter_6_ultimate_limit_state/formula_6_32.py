"""Formula 6.32 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot32MNrdRectangular(Formula):
    r"""Class representing formula 6.32 for the calculation of [$M_{N,Rd}$]."""

    label = "6.32"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        m_pl_rd: NMM,
        n_ed: N,
        n_pl_rd: N,
    ) -> None:
        r"""[$M_{N,Rd}$] Calculation of the reduced plastic moment for rectangular solid section without fastener holes [$Nmm$].

        EN 1993-1-1:2005 art.6.2.9(3) - Formula (6.32)

        Parameters
        ----------
        m_pl_rd : NMM
            [$M_{pl,Rd}$] Plastic moment resistance of the section [$Nmm$].
        n_ed : N
            [$N_{Ed}$] Design axial force [$N$].
        n_pl_rd : N
            [$N_{pl,Rd}$] Plastic axial resistance of the section [$N$].
        """
        super().__init__()
        self.m_pl_rd = m_pl_rd
        self.n_ed = n_ed
        self.n_pl_rd = n_pl_rd

    @staticmethod
    def _evaluate(
        m_pl_rd: NMM,
        n_ed: N,
        n_pl_rd: N,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_pl_rd=n_pl_rd)
        raise_if_negative(n_ed=n_ed, m_pl_rd=m_pl_rd)

        return m_pl_rd * (1 - (n_ed / n_pl_rd) ** 2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.32."""
        _equation: str = r"M_{pl,Rd} \cdot \left[ 1 - \left( \frac{N_{Ed}}{N_{pl,Rd}} \right)^2 \right]"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"M_{pl,Rd}": f"{self.m_pl_rd:.{n}f}",
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"N_{pl,Rd}": f"{self.n_pl_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"M_{pl,Rd}": rf"{self.m_pl_rd:.{n}f} \ Nmm",
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"N_{pl,Rd}": rf"{self.n_pl_rd:.{n}f} \ N",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"M_{N,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )
