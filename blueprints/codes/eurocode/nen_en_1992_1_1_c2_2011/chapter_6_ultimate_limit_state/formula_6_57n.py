"""Formula 6.57N from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form6Dot57NNuPrime(Formula):
    r"""Class representing formula 6.57N for the calculation of [$\nu'$]."""

    label = "6.57N"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        r"""[$\nu'$] Calculation of [$\nu'$].

        NEN-EN 1992-1-1+C2:2011 art.6.5.2(2) - Formula (6.57N)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        f_ck: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ck=f_ck)

        return 1 - f_ck / 250

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.57N."""
        _equation: str = r"1 - \frac{f_{ck}}{250}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"f_{ck}": f"{self.f_ck:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\nu'",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
