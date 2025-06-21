"""Formula 7.10 from EN 1992-1-1:2004: Chapter 7 - Serviceability Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7Dot10RhoPEff(Formula):
    r"""Class representing formula 7.10 for the calculation of [$\rho_{p,eff}$]."""

    label = "7.10"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        a_s: MM2,
        xi_1: DIMENSIONLESS,
        a_p_prime: MM2,
        a_c_eff: MM2,
    ) -> None:
        r"""[$\rho_{p,eff}$] Calculation of the effective reinforcement ratio [$mm^2$].

        EN 1992-1-1:2004 art.7.3.2(3) - Formula (7.10)

        Parameters
        ----------
        a_s : MM2
            [$A_s$] Area of tensile reinforcement [$mm^2$].
        xi_1 : DIMENSIONLESS
            [$\xi_1$] Coefficient related to the reinforcement.
        a_p_prime : MM2
            [$A'_p$] Area of pre- or post-tensioned steel [$mm^2$].
        a_c_eff : MM2
            [$A_{c,eff}$] Effective area of concrete [$mm^2$].
        """
        super().__init__()
        self.a_s = a_s
        self.xi_1 = xi_1
        self.a_p_prime = a_p_prime
        self.a_c_eff = a_c_eff

    @staticmethod
    def _evaluate(
        a_s: MM2,
        xi_1: DIMENSIONLESS,
        a_p_prime: MM2,
        a_c_eff: MM2,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_s=a_s, xi_1=xi_1, a_p_prime=a_p_prime)
        raise_if_less_or_equal_to_zero(a_c_eff=a_c_eff)

        return (a_s + xi_1 * a_p_prime) / a_c_eff

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.10."""
        _equation: str = r"\frac{A_s + \xi_1 \cdot A'_p}{A_{c,eff}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_s": f"{self.a_s:.{n}f}",
                r"\xi_1": f"{self.xi_1:.{n}f}",
                r"A'_p": f"{self.a_p_prime:.{n}f}",
                r"A_{c,eff}": f"{self.a_c_eff:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\rho_{p,eff}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
