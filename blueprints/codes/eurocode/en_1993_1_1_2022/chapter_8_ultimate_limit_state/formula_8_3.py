"""Formula 8.3 from EN 1993-1-1:2022: Chapter 8 - Ultimate limit state."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.en_1993_1_1_2022 import EN_1993_1_1_2022
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import KN, KNM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot3UtilizationRatio(ComparisonFormula):
    r"""Class representing formula 8.3 for the calculation of the utilization ratio [$UC$]."""

    label = "8.3"
    source_document = EN_1993_1_1_2022

    def __init__(
        self,
        n_ed: KN,
        n_rd: KN,
        m_y_ed: KNM,
        m_y_rd: KNM,
        m_z_ed: KNM,
        m_z_rd: KNM,
    ) -> None:
        r"""
        [$UC$] The calculation of the utilization ratio [$-$].

        EN 1993-1-1:2022 art.8.2.1(7) - Formula (8.3)

        Parameters
        ----------
        n_ed : KN
            [$N_{Ed}$] Contains the design axial force [$kN$].
        n_rd : KN
            [$N_{Rd}$] Contains the design axial resistance [$kN$].
        m_y_ed : KNM
            [$M_{y,Ed}$] Contains the design moment about the y-axis [$kNm$].
        m_y_rd : KNM
            [$M_{y,Rd}$] Contains the design moment resistance about the y-axis [$kNm$].
        m_z_ed : KNM
            [$M_{z,Ed}$] Contains the design moment about the z-axis [$kNm$].
        m_z_rd : KNM
            [$M_{z,Rd}$] Contains the design moment resistance about the z-axis [$kNm$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_rd = n_rd
        self.m_y_ed = m_y_ed
        self.m_y_rd = m_y_rd
        self.m_z_ed = m_z_ed
        self.m_z_rd = m_z_rd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(
        n_ed: KN,
        n_rd: KN,
        m_y_ed: KNM,
        m_y_rd: KNM,
        m_z_ed: KNM,
        m_z_rd: KNM,
    ) -> float:
        """Evaluates the left-hand side of the comparison. see __init__ for details."""
        raise_if_less_or_equal_to_zero(n_rd=n_rd, m_y_rd=m_y_rd, m_z_rd=m_z_rd)
        raise_if_negative(n_ed=n_ed, m_y_ed=m_y_ed, m_z_ed=m_z_ed)
        return (n_ed / n_rd) + (m_y_ed / m_y_rd) + (m_z_ed / m_z_rd)

    @staticmethod
    def _evaluate_rhs(*_, **_kwargs) -> float:
        """Evaluates the right-hand side of the comparison. see __init__ for details."""
        return 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for form 8.3."""
        _equation: str = r"\frac{N_{Ed}}{N_{Rd}} + \frac{M_{y,Ed}}{M_{y,Rd}} + \frac{M_{z,Ed}}{M_{z,Rd}} \leq 1.0"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"N_{Rd}": f"{self.n_rd:.{n}f}",
                r"M_{y,Ed}": f"{self.m_y_ed:.{n}f}",
                r"M_{y,Rd}": f"{self.m_y_rd:.{n}f}",
                r"M_{z,Ed}": f"{self.m_z_ed:.{n}f}",
                r"M_{z,Rd}": f"{self.m_z_rd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ kN",
                r"N_{Rd}": rf"{self.n_rd:.{n}f} \ kN",
                r"M_{y,Ed}": rf"{self.m_y_ed:.{n}f} \ kNm",
                r"M_{y,Rd}": rf"{self.m_y_rd:.{n}f} \ kNm",
                r"M_{z,Ed}": rf"{self.m_z_ed:.{n}f} \ kNm",
                r"M_{z,Rd}": rf"{self.m_z_rd:.{n}f} \ kNm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result=rf"{self.lhs:.{n}f} \to OK" if bool(self) else rf"{self.lhs:.{n}f} \to \text{{Not OK}}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
        )
