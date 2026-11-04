"""Formula 2.15 from EN 1995-1-1:2004: Chapter 2: Basis of design."""

from blueprints.codes.eurocode.en_1995_1_1_2004 import EN_1995_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form2Dot15DesignModulusElasticity(Formula):
    """Class representing formula 2.15 for the calculation of the design value of the modulus of elasticity [$E_d$]."""

    label = "2.15"
    source_document = EN_1995_1_1_2004

    def __init__(
        self,
        e_mean: MPA,
        gamma_m: DIMENSIONLESS,
    ) -> None:
        r"""[$E_d$] Design value of the modulus of elasticity [$MPA$].

        EN 1995-1-1:2004 art.2.4.1(2) - Formula (2.15)

        Parameters
        ----------
        e_mean : MPA
            [$E_{mean}$] Mean value of the modulus of elasticity [$MPA$].
        gamma_m : DIMENSIONLESS
            [$\gamma_M$] Partial factor for a material property [$-$].
        """
        super().__init__()
        self.e_mean = e_mean
        self.gamma_m = gamma_m

    @staticmethod
    def _evaluate(
        e_mean: MPA,
        gamma_m: DIMENSIONLESS,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(e_mean=e_mean)
        raise_if_less_or_equal_to_zero(gamma_m=gamma_m)
        return e_mean / gamma_m

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 2.15."""
        _equation: str = r"\frac{E_{mean}}{\gamma_M}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"E_{mean}": f"{self.e_mean:.{n}f}",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
            },
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"E_{mean}": rf"{self.e_mean:.{n}f} \ MPA",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
            },
        )
        return LatexFormula(
            return_symbol=r"E_d",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPA",
        )
