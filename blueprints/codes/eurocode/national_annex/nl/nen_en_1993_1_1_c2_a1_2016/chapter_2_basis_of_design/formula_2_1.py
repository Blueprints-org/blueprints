"""Formula 2.1 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 2 - Basis of Design."""

from blueprints.codes.eurocode.national_annex.nl.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form2Dot1DesignResistance(Formula):
    r"""Class representing formula 2.1 for the calculation of [$R_d$]."""

    label = "2.1"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        r_k: DIMENSIONLESS,
        gamma_m: DIMENSIONLESS,
    ) -> None:
        r"""[$R_d$] Calculation of the design resistance.

        NEN-EN 1993-1-1+C2+A1:2016 art.2 - Formula (2.1)

        Parameters
        ----------
        r_k : DIMENSIONLESS
            [$R_k$] Characteristic value of the resistance.
        gamma_m : DIMENSIONLESS
            [$\gamma_M$] Partial safety factor for resistance.
        """
        super().__init__()
        self.r_k = r_k
        self.gamma_m = gamma_m

    @staticmethod
    def _evaluate(
        r_k: DIMENSIONLESS,
        gamma_m: DIMENSIONLESS,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m=gamma_m)

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
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"R_k": rf"{self.r_k:.{n}f}",
                r"\gamma_M": rf"{self.gamma_m:.{n}f}",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"R_d",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
        )
