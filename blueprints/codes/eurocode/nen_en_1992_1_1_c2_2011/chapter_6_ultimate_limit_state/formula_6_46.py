"""Formula 6.46 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot46BetaCorner(Formula):
    r"""Class representing formula 6.46 for the calculation of [$\beta$] for corner column connections."""

    label = "6.46"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        u1: MM,
        u1_star: MM,
    ) -> None:
        r"""[$\beta$] Calculation of [$\beta$].

        NEN-EN 1992-1-1+C2:2011 art.6.4.3(3) - Formula (6.46)

        Parameters
        ----------
        u1 : MM
            [$u_1$] Basic control perimeter [$mm$].
        u1_star : MM
            [$u_{1^*}$] Reduced basic control perimeter [$mm$].
        """
        super().__init__()
        self.u1 = u1
        self.u1_star = u1_star

    @staticmethod
    def _evaluate(
        u1: MM,
        u1_star: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(u1=u1)
        raise_if_less_or_equal_to_zero(u1_star=u1_star)

        return u1 / u1_star

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.46."""
        _equation: str = r"\frac{u_1}{u_{1^*}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"u_1": f"{self.u1:.3f}",
                r"u_{1^*}": f"{self.u1_star:.3f}",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"\beta",
            result=f"{self._evaluate(self.u1, self.u1_star):.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
