"""Formula 2.1 from EN 1993-1-1:2005: Chapter 2: Basis of design."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form2Dot1DesignValueResistance(Formula):
    """Class representing formula 2.1 for the calculation of the design resistance [$R_d$]."""

    label = "2.1"
    source_document = EN_1993_1_1_2005

    def __init__(self, r_k: KN, gamma_m: DIMENSIONLESS) -> None:
        r"""[$R_d$] Design value of the resistance [$kN$].

        EN 1993-1-1:2005 art.2.4.3(1) - Formula (2.1)

        Parameters
        ----------
        r_k : kN
            [$R_k$] Characteristic value of the resistance based on EN 1990 [$kN$].
        gamma_m : DIMENSIONLESS
            [$\gamma_{M}$] Global partial factor for the resistance [$-$].
        """
        super().__init__()
        self.r_k = r_k
        self.gamma_m = gamma_m

    @staticmethod
    def _evaluate(r_k: KN, gamma_m: DIMENSIONLESS) -> KN:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m=gamma_m)
        raise_if_negative(r_k=r_k)
        return r_k / gamma_m

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 2.1."""
        return LatexFormula(
            return_symbol=r"R_{d}",
            result=f"{self:.{n}f}",
            equation=r"\frac{R_k}{\gamma_M}",
            numeric_equation=rf"\frac{{{self.r_k:.{n}f}}}{{{self.gamma_m:.{n}f}}}",
            comparison_operator_label="=",
        )
