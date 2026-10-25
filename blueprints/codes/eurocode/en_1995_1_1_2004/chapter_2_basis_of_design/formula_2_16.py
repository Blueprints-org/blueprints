"""Formula 2.16 from EN 1995-1-1:2004: Chapter 2: Basis of design."""

from blueprints.codes.eurocode.en_1995_1_1_2004 import EN_1995_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form2Dot16DesignShearModulus(Formula):
    """Class representing formula 2.16 for the calculation of the design value of the shear modulus [$G_d$]."""

    label = "2.16"
    source_document = EN_1995_1_1_2004

    def __init__(
        self,
        g_mean: MPA,
        gamma_m: DIMENSIONLESS,
    ) -> None:
        r"""[$G_d$] Design value of the shear modulus [$MPA$].

        EN 1995-1-1:2004 art.2.4.1(2) - Formula (2.16)

        Parameters
        ----------
        g_mean : MPA
            [$G_{mean}$] Mean value of the shear modulus [$MPA$].
        gamma_m : DIMENSIONLESS
            [$\gamma_M$] Partial factor for a material property [$-$].
        """
        super().__init__()
        self.g_mean = g_mean
        self.gamma_m = gamma_m

    @staticmethod
    def _evaluate(
        g_mean: MPA,
        gamma_m: DIMENSIONLESS,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(g_mean=g_mean)
        raise_if_less_or_equal_to_zero(gamma_m=gamma_m)
        return g_mean / gamma_m

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 2.16."""
        _equation: str = r"\frac{G_{mean}}{\gamma_M}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"G_{mean}": f"{self.g_mean:.{n}f}",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
            },
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"G_{mean}": rf"{self.g_mean:.{n}f} \ MPA",
                r"\gamma_M": f"{self.gamma_m:.{n}f}",
            },
        )
        return LatexFormula(
            return_symbol=r"G_d",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPA",
        )
