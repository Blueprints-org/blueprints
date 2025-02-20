"""Formula 6.39 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot39BetaCoefficient(Formula):
    r"""Class representing formula 6.39 for the calculation of the beta coefficient, [$\beta$]."""

    label = "6.39"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        k: DIMENSIONLESS,
        m_ed: NMM,
        v_ed: N,
        u_1: MM,
        w_1: MM2,
    ) -> None:
        r"""[$\beta$] Beta coefficient [$-$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.3(3) - Formula (6.39)

        Parameters
        ----------
        k : DIMENSIONLESS
            [$k$] Coefficient dependent on the ratio between the column dimensions c1 and c2 [$-$].
        m_ed : NMM
            [$M_{Ed}$] Design value of the applied moment [$Nmm$].
        v_ed : N
            [$V_{Ed}$] Design value of the applied shear force [$N$].
        u_1 : MM
            [$u_1$] Length of the basic control perimeter [$mm$].
        w_1 : MM2
            [$W_1$] Distribution of shear as illustrated in Figure 6.19 [$mm^2$].
        """
        super().__init__()
        self.k = k
        self.m_ed = m_ed
        self.v_ed = v_ed
        self.u_1 = u_1
        self.w_1 = w_1

    @staticmethod
    def _evaluate(
        k: DIMENSIONLESS,
        m_ed: NMM,
        v_ed: N,
        u_1: MM,
        w_1: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            k=k,
            m_ed=m_ed,
            u_1=u_1,
        )
        raise_if_less_or_equal_to_zero(v_ed=v_ed, w_1=w_1)

        return 1 + k * m_ed / v_ed * u_1 / w_1

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.39."""
        return LatexFormula(
            return_symbol=r"\beta",
            result=f"{self:.3f}",
            equation=r"1 + k \cdot \frac{M_{Ed}}{V_{Ed}} \cdot \frac{u_1}{W_1}",
            numeric_equation=rf"1 + {self.k:.3f} \cdot \frac{{{self.m_ed:.3f}}}{{{self.v_ed:.3f}}} \cdot \frac{{{self.u_1:.3f}}}{{{self.w_1:.3f}}}",
            comparison_operator_label="=",
            unit="-",
        )
