"""Formula 8.3 from EN 1993-1-1:2025: Chapter 8 - Ultimate limit state."""

# pylint: disable=arguments-differ
from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, KNM, RATIO
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot3UtilizationRatio(Formula):
    """Class representing form 8.3 for the calculation of the utilization ratio [$UC$]."""

    label = "8.3"
    source_document = EN_1993_1_1_2025

    def __init__(self, n_ed: KN, n_rd: KN, m_y_ed: KNM, m_y_rd: KNM, m_z_ed: KNM, m_z_rd: KNM) -> None:
        r"""
        [$UC$] The calculation of the utilization ratio [$-$].

        EN 1993-1-1:2025 art.8.2.1(7) - Formula (8.3)

        Parameters
        ----------
        n_ed : kN
            [$N_{Ed}$] Contains the design axial force [$kN$].
        n_rd : kN
            [$N_{Rd}$] Contains the design axial resistance [$kN$].
        m_y_ed : kNm
            [$M_{y,Ed}$] Contains the design moment about the y-axis [$kNm$].
        m_y_rd : kNm
            [$M_{y,Rd}$] Contains the design moment resistance about the y-axis [$kNm$].
        m_z_ed : kNm
            [$M_{z,Ed}$] Contains the design moment about the z-axis [$kNm$].
        m_z_rd : kNm
            [$M_{z,Rd}$] Contains the design moment resistance about the z-axis [$kNm$].

        Returns
        -------
        None
        """
        super().__init__()
        self.n_ed = n_ed
        self.n_rd = n_rd
        self.m_y_ed = m_y_ed
        self.m_y_rd = m_y_rd
        self.m_z_ed = m_z_ed
        self.m_z_rd = m_z_rd

    @staticmethod
    def _evaluate(
        n_ed: KN,
        n_rd: KN,
        m_y_ed: KNM,
        m_y_rd: KNM,
        m_z_ed: KNM,
        m_z_rd: KNM,
    ) -> RATIO:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(n_rd=n_rd, m_y_rd=m_y_rd, m_z_rd=m_z_rd)
        raise_if_negative(n_ed=n_ed, m_y_ed=m_y_ed, m_z_ed=m_z_ed)

        return (n_ed / n_rd) + (m_y_ed / m_y_rd) + (m_z_ed / m_z_rd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for form 8.3."""
        numeric_equation = (
            rf"\frac{{{self.n_ed:.{n}f}}}{{{self.n_rd:.{n}f}}} + "
            rf"\frac{{{self.m_y_ed:.{n}f}}}{{{self.m_y_rd:.{n}f}}} + "
            rf"\frac{{{self.m_z_ed:.{n}f}}}{{{self.m_z_rd:.{n}f}}}"
        )
        return LatexFormula(
            return_symbol=r"UC",
            result=f"{self:.{n}f}",
            equation=r"\frac{N_{Ed}}{N_{Rd}} + \frac{M_{y,Ed}}{M_{y,Rd}} + \frac{M_{z,Ed}}{M_{z,Rd}}",
            numeric_equation=numeric_equation,
            comparison_operator_label="=",
        )
