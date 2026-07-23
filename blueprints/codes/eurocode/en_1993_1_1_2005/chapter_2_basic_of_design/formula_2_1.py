"""Formula 2.1 from EN 1993-1-1:2005: Chapter 2: Basis of design."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form2Dot1DesignValueResistance(Formula):
    """Class representing formula 2.1 for the calculation of the design value of the resistance [$R_d$]."""

    label = "2.1"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        r_k: N,
        gamma_m: DIMENSIONLESS,
    ) -> None:
        r"""[$R_d$] Design value of the resistance [$N$].

        EN 1993-1-1:2005 art.2.4.3(1) - Formula (2.1)

        Parameters
        ----------
        r_k : N
            [$R_k$] Characteristic value of the resistance based on EN 1990 [$N$].
        gamma_m : DIMENSIONLESS
            [$\gamma_{M}$] Global partial factor for the resistance [$-$].
        """
        super().__init__()
        self.r_k = r_k
        self.gamma_m = gamma_m

    @staticmethod
    def _evaluate(
        r_k: N,
        gamma_m: DIMENSIONLESS,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m=gamma_m)
        raise_if_negative(r_k=r_k)
        return r_k / gamma_m

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 2.1."""
        _equation: str = r"\frac{R_k}{\gamma_M}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"R_k": f"{self.r_k:.{n}f}",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
            },
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"R_k": rf"{self.r_k:.{n}f} \ N",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
            },
        )
        return LatexFormula(
            return_symbol=r"R_{d}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )
