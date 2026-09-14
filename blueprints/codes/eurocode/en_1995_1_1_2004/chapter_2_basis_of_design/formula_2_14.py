"""Formula 2.14 from EN 1995-1-1:2004: Chapter 2: Basis of design."""

from blueprints.codes.eurocode.en_1995_1_1_2004 import EN_1995_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form2Dot14DesignValueStrength(Formula):
    """Class representing formula 2.14 for the calculation of the design value of the strength [$X_d$]."""

    label = "2.14"
    source_document = EN_1995_1_1_2004

    def __init__(
        self,
        x_k: MPA,
        gamma_m: DIMENSIONLESS,
        k_mod: DIMENSIONLESS,
    ) -> None:
        r"""[$X_d$] Design value of the strength [$MPA$].

        EN 1995-1-1:2004 art.2.4.1(1) - Formula (2.14)

        Parameters
        ----------
        x_k : MPA
            [$X_k$] Characteristic value of the strength [$MPA$].
        gamma_m : DIMENSIONLESS
            [$\gamma_{M}$] partial factor for the strength [$-$].
        k_mod : DIMENSIONLESS
            [$\k_{mod}$] modification factor for load and moisture content [$-$].
        """
        super().__init__()
        self.x_k = x_k
        self.gamma_m = gamma_m
        self.k_mod = k_mod

    @staticmethod
    def _evaluate(
        x_k: MPA,
        gamma_m: DIMENSIONLESS,
        k_mod: DIMENSIONLESS,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(x_k=x_k)
        raise_if_less_or_equal_to_zero(gamma_m=gamma_m)
        raise_if_less_or_equal_to_zero(k_mod=k_mod)
        return k_mod * x_k / gamma_m

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 2.14."""
        _equation: str = r"k_{mod} \cdot \frac{X_k}{\gamma_M}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"X_k": f"{self.x_k:.{n}f}",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
                r"k_{mod}": f"{self.k_mod:.{n}f}",
            },
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"X_k": rf"{self.x_k:.{n}f} \ MPA",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
                r"k_{mod}": f"{self.k_mod:.{n}f}",
            },
        )
        return LatexFormula(
            return_symbol=r"X_d",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPA",
        )
