"""Formula 5.48 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.validations import raise_if_negative


class Form5Dot48LowerCharacteristicPrestressingValue(Formula):
    r"""Class representing formula 5.48 for the calculation of the lower characteristic value for the prestressing
    value at SLS and Fatigue, [$P_{k,inf}$].
    """

    label = "5.48"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        r_inf: DIMENSIONLESS,
        p_m_t: KN,
    ) -> None:
        r"""[$P_{k,inf}$] Lower characteristic value for the prestressing value at SLS and Fatigue [$kN$].

        EN 1992-1-1:2004 art.5.10.9(1) - Formula (5.48)

        Parameters
        ----------
        r_inf : DIMENSIONLESS
            [$r_{inf}$] Factor for the lower characteristic value, recommended value is 0.95 for pre-tensioning or unbounded tendons,
             0.90 for post-tensioning with bonded tendons. When appropriate measures are taken: 1.0 [$-$].
        p_m_t : KN
            [$P_{m,t}(x)$] Mean value of the prestressing force at location x [$kN$].
        """
        super().__init__()
        self.r_inf = r_inf
        self.p_m_t = p_m_t

    @staticmethod
    def _evaluate(
        r_inf: DIMENSIONLESS,
        p_m_t: KN,
    ) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            r_inf=r_inf,
            p_m_t=p_m_t,
        )

        return r_inf * p_m_t

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.48."""
        return LatexFormula(
            return_symbol=r"P_{k,inf}",
            result=f"{self:.{n}f}",
            equation=r"r_{inf} \cdot P_{m,t}(x)",
            numeric_equation=rf"{self.r_inf:.{n}f} \cdot {self.p_m_t:.{n}f}",
            comparison_operator_label="=",
            unit="kN",
        )
