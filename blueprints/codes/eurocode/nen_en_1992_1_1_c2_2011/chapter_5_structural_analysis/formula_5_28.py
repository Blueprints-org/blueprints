"""Formula 5.28 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN, KNM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot28TotalDesignMoment(Formula):
    """Class representing formula 5.28 for the calculation of the total design moment, [$M_{Ed}$]."""

    label = "5.28"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        m_0ed: KNM,
        beta: DIMENSIONLESS,
        n_ed: KN,
        n_b: KN,
    ) -> None:
        r"""[$M_{Ed}$] Total design moment [$kNm$].

        NEN-EN 1992-1-1+C2:2011 art.5.8.8.2(2) - Formula (5.28)

        Parameters
        ----------
        m_0ed : KNM
            [$M_{0Ed}$] First order moment; see also 5.8.8.2 (2) [$kNm$].
        beta : float
            [$\beta$] Factor which depends on distribution of 1st and 2nd order moments, see 5.8.7.3 (2)-(3) [-].
        n_ed : KN
            [$N_{Ed}$] Design value of axial load [$kN$].
        n_b : KN
            [$N_{B}$] Buckling load based on nominal stiffness [$kN$].
        """
        super().__init__()
        self.m_0ed = m_0ed
        self.beta = beta
        self.n_ed = n_ed
        self.n_b = n_b

    @staticmethod
    def _evaluate(
        m_0ed: KNM,
        beta: DIMENSIONLESS,
        n_ed: KN,
        n_b: KN,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            m_0ed=m_0ed,
            beta=beta,
            n_b=n_b,
        )
        raise_if_less_or_equal_to_zero(n_ed=n_ed)

        # When n_b / n_ed is equal to 1, the formula will divide by zero.
        # The spirit of the equation is to raise the second order moment to infinity when n_b / n_ed is equal to 1.
        # This is not possible in numeric calculations, so we will use a large number instead.
        return 1e9 if n_b == n_ed else m_0ed * (1 + beta / (n_b / n_ed - 1))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.28."""
        return LatexFormula(
            return_symbol=r"M_{Ed}",
            result=f"{self:.3f}",
            equation=r"M_{0Ed} \cdot \left(1 + \frac{\beta}{\frac{N_{B}}{N_{Ed}} - 1}\right)",
            numeric_equation=rf"{self.m_0ed:.3f} \cdot \left(1 + \frac{{{self.beta:.3f}}}{{\frac{{{self.n_b:.3f}}}{{{self.n_ed:.3f}}} - 1}}\right)",
            comparison_operator_label="=",
            unit="kNm",
        )
