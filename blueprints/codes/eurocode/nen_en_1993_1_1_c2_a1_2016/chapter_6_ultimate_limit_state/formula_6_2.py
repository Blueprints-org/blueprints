"""Formula 6.2 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate limit state."""

# pylint: disable=arguments-differ
from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, KNM, RATIO
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot2UtilizationRatio(Formula):
    """Class representing form 6.2 for the calculation of the utilization ratio [$UC$]."""

    label = "6.2"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(self, n_ed: KN, n_rd: KN, m_y_ed: KNM, m_y_rd: KNM, m_z_ed: KNM, m_z_rd: KNM) -> None:
        r"""
        [$UC$] The calculation of the utilization ratio [$-$].

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.1(7) - Formula (6.2)

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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for form 6.2."""
        numeric_equation = (
            rf"\frac{{{self.n_ed:.3f}}}{{{self.n_rd:.3f}}} + "
            rf"\frac{{{self.m_y_ed:.3f}}}{{{self.m_y_rd:.3f}}} + "
            rf"\frac{{{self.m_z_ed:.3f}}}{{{self.m_z_rd:.3f}}}"
        )
        return LatexFormula(
            return_symbol=r"UC",
            result=f"{self:.3f}",
            equation=r"\frac{N_{Ed}}{N_{Rd}} + \frac{M_{y,Ed}}{M_{y,Rd}} + \frac{M_{z,Ed}}{M_{z,Rd}}",
            numeric_equation=numeric_equation,
            comparison_operator_label="=",
        )
