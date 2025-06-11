"""Formula 5.22 from EN 1993-5:2007: Chapter 5 - Ultimate Limit States."""

from blueprints.codes.eurocode.en_1993_5_2007 import EN_1993_5_2007
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import KN, KNM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot22ReducedMomentResistanceClass3(Formula):
    r"""Class representing formula 5.22 for the calculation of [$M_N,Rd$] for Class 3 cross-sections."""

    label = "5.22"
    source_document = EN_1993_5_2007

    def __init__(
        self,
        m_c_rd: KNM,
        n_ed: KN,
        n_pl_rd: KN,
    ) -> None:
        r"""[$M_N,Rd$] Calculation of the reduced design moment resistance allowing for the axial force [$kNm$].

        EN 1993-5:2007 art. 5.2.3 (11) - Formula (5.22)

        Parameters
        ----------
        m_c_rd : KNM
            [$M_c,Rd$] Design moment resistance of the cross-section [$kNm$].
        n_ed : KN
            [$N_Ed$] Design value of the axial force [$kN$].
        n_pl_rd : KN
            [$N_pl,Rd$] Design plastic resistance of the cross-section [$kN$].
        """
        super().__init__()
        self.m_c_rd = m_c_rd
        self.n_ed = n_ed
        self.n_pl_rd = n_pl_rd

    @staticmethod
    def _evaluate(
        m_c_rd: KNM,
        n_ed: KN,
        n_pl_rd: KN,
    ) -> KNM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(m_c_rd=m_c_rd, n_ed=n_ed)
        raise_if_less_or_equal_to_zero(n_pl_rd=n_pl_rd)

        return m_c_rd * (1 - n_ed / n_pl_rd)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.22."""
        _equation: str = r"M_{c,Rd} \cdot \left(1 - \frac{N_{Ed}}{N_{pl,Rd}}\right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"M_{c,Rd}": f"{self.m_c_rd:.3f}",
                r"N_{Ed}": f"{self.n_ed:.3f}",
                r"N_{pl,Rd}": f"{self.n_pl_rd:.3f}",
            },
            False,
        )

        return LatexFormula(
            return_symbol=r"M_{N,Rd}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="kNm",
        )
