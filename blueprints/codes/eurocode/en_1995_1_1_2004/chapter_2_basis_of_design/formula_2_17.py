"""Formula 2.1 from EN 1995-1-1:2004: Chapter 2: Basis of design."""

from blueprints.codes.eurocode.en_1995_1_1_2004 import EN_1995_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form2Dot17DesignValueResistance(Formula):
    """Class representing formula 2.17 for the calculation of the design value of the resistance [$R_d$]."""

    label = "2.17"
    source_document = EN_1995_1_1_2004

    def __init__(
        self,
        r_k: N,
        gamma_m: DIMENSIONLESS,
        k_mod: DIMENSIONLESS,
    ) -> None:
        r"""[$R_d$] Design value of the resistance [$N$].

        EN 1995-1-1:2004 art.2.4.3(1) - Formula (2.17)

        Parameters
        ----------
        r_k : N
            [$R_k$] Characteristic value of the resistance [$N$].
        gamma_m : DIMENSIONLESS
            [$\gamma_{M}$] partial factor for the resistance [$-$].
        """
        super().__init__()
        self.r_k = r_k
        self.gamma_m = gamma_m
        self.k_mod = k_mod

    @staticmethod
    def _evaluate(
        r_k: N,
        gamma_m: DIMENSIONLESS,
        k_mod: DIMENSIONLESS,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m=gamma_m)
        raise_if_negative(r_k=r_k)
        return k_mod * r_k / gamma_m

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 2.1."""
        _equation: str = r"k_{mod}* \frac{R_k}{\gamma_M}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"R_k": f"{self.r_k:.{n}f}",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
                r"\k_mod": f"{self.k_mod:.{n}f}",
            },
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"R_k": rf"{self.r_k:.{n}f} \ N",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
                r"\k_mod": f"{self.k_mod:.{n}f}",
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
