"""Formula 5.30 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import KN, KNM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot30TotalDesignMoment(Formula):
    """Class representing formula 5.30 for the calculation of the total design moment, [$M_{Ed}$]."""

    label = "5.30"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        m_0ed: KNM,
        n_ed: KN,
        n_b: KN,
    ) -> None:
        r"""[$M_{Ed}$] Total design moment [$kNm$].

        NEN-EN 1992-1-1+C2:2011 art.5.8.8.2(2) - Formula (5.30)

        Parameters
        ----------
        m_0ed : KNM
            [$M_{0Ed}$] First order moment; see also 5.8.8.2 (2) [$kNm$].
        n_ed : KN
            [$N_{Ed}$] Design value of axial load [$kN$].
        n_b : KN
            [$N_{B}$] Buckling load based on nominal stiffness [$kN$].
        """
        super().__init__()
        self.m_0ed = m_0ed
        self.n_ed = n_ed
        self.n_b = n_b

    @staticmethod
    def _evaluate(
        m_0ed: KNM,
        n_ed: KN,
        n_b: KN,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            m_0ed=m_0ed,
            n_ed=n_ed,
        )
        raise_if_less_or_equal_to_zero(n_b=n_b)

        # When n_ed / n_b is equal to 1, the formula will divide by zero.
        # The spirit of the equation is to raise the second order moment to infinity when n_ed / n_b is equal to 1.
        # This is not possible in numeric calculations, so we will use a large number instead.
        return 1e9 if n_ed == n_b else m_0ed / (1 - (n_ed / n_b))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.30."""
        return LatexFormula(
            return_symbol=r"M_{Ed}",
            result=f"{self:.3f}",
            equation=r"\frac{M_{0Ed}}{1 - \left(\frac{N_{Ed}}{N_{B}}\right)}",
            numeric_equation=rf"\frac{{{self.m_0ed:.3f}}}{{1 - \left(\frac{{{self.n_ed:.3f}}}{{{self.n_b:.3f}}}\right)}}",
            comparison_operator_label="=",
            unit="kNm",
        )
