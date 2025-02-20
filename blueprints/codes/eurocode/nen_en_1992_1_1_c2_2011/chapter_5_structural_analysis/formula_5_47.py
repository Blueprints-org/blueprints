"""Formula 5.47 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.validations import raise_if_negative


class Form5Dot47UpperCharacteristicPrestressingValue(Formula):
    r"""Class representing formula 5.47 for the calculation of the upper characteristic value for the prestressing
    value at SLS and Fatigue, [$P_{k,sup}$].
    """

    label = "5.47"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        r_sup: DIMENSIONLESS,
        p_m_t: KN,
    ) -> None:
        r"""[$P_{k,sup}$] Upper characteristic value for the prestressing value at SLS and Fatigue [$kN$].

        NEN-EN 1992-1-1+C2:2011 art.5.10.9(1) - Formula (5.47)

        Parameters
        ----------
        r_sup : DIMENSIONLESS
            [$r_{sup}$] Factor for the upper characteristic value, recommended value is 1.05 for pre-tensioning or unbounded tendons,
             1.10 for post-tensioning with bonded tendons. When appropriate measures are taken: 1.0 [$-$].
        p_m_t : KN
            [$P_{m,t}(x)$] Mean value of the prestressing force at location x [$kN$].
        """
        super().__init__()
        self.r_sup = r_sup
        self.p_m_t = p_m_t

    @staticmethod
    def _evaluate(
        r_sup: DIMENSIONLESS,
        p_m_t: KN,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            r_sup=r_sup,
            p_m_t=p_m_t,
        )

        return r_sup * p_m_t

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.47."""
        return LatexFormula(
            return_symbol=r"P_{k,sup}",
            result=f"{self:.3f}",
            equation=r"r_{sup} \cdot P_{m,t}(x)",
            numeric_equation=rf"{self.r_sup:.3f} \cdot {self.p_m_t:.3f}",
            comparison_operator_label="=",
            unit="kN",
        )
