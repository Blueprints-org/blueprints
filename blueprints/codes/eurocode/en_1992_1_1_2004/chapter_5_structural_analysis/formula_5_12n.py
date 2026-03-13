"""Formula 5.12N from EN 1992-1-1:2004: Chapter 5 Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_fraction
from blueprints.type_alias import DIMENSIONLESS, KN, KNM, M
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot12nRatioDistancePointZeroAndMaxMoment(Formula):
    """Class representing formula 5.12N for the calculation of the lambda ratio.

    Note:
    Ratio of the distance between point of zero and maximum moment after redistribution and
    effective depth, d. [$λ$]
    """

    label = "5.12N"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        m_sd: KNM,
        v_sd: KN,
        d: M,
    ) -> None:
        r"""[$λ$] ratio of the distance between point of zero and maximum moment after redistribution and
        effective depth, d [$-$].

        EN 1992-1-1:2004 art.5.6.3(4) - Formula (5.12N)

        Parameters
        ----------
        m_sd : KNM
            [$M_{sd}$] Design moment at the section [$kNm$].
        v_sd : KN
            [$V_{sd}$] Design shear force at the section [$kN$].
        d : M
            [$d$] Effective depth [$m$].
        """
        super().__init__()
        self.m_sd = m_sd
        self.v_sd = v_sd
        self.d = d

    @staticmethod
    def _evaluate(
        m_sd: KNM,
        v_sd: KN,
        d: M,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(
            m_sd=m_sd,
            v_sd=v_sd,
            d=d,
        )
        return m_sd / (v_sd * d)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.12N."""
        numerator = f"{self.m_sd:.{n}f}"
        denominator = f"{self.v_sd:.{n}f} \\cdot {self.d:.{n}f}"
        return LatexFormula(
            return_symbol="λ",
            result=f"{self:.{n}f}",
            equation=r"\frac{M_{sd}}{V_{sd} \cdot d}",
            numeric_equation=f"{latex_fraction(numerator=numerator, denominator=denominator)}",
            comparison_operator_label="=",
        )
