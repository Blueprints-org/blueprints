"""Formula 6.44 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot44BetaRectangular(Formula):
    r"""Class representing formula 6.44 for the calculation of [$\beta$] for rectangular columns where there are
    eccentricities in both orthogonal directions.
    """

    label = "6.44"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        u1: MM,
        u1_star: MM,
        k: DIMENSIONLESS,
        w_1: NMM,
        e_par: MM,
    ) -> None:
        r"""[$\beta$] Calculation of [$\beta$] where there are eccentricities in both orthogonal directions.

        NEN-EN 1992-1-1+C2:2011 art.6.4.3(3) - Formula (6.44)

        Parameters
        ----------
        u1 : MM
            [$u_1$] Basic control perimeter [$mm$].
        u1_star : MM
            [$u_{1^*}$] Reduced basic control perimeter [$mm$].
        k : DIMENSIONLESS
            [$k$] Factor determined from Table 6.1 with the ratio c1/2c2 [$-$].
        w_1 : NMM
            [$W_1$] Calculated for the basic control perimeter [$Nmm$].
        e_par : MM
            [$e_{par}$] Eccentricity parallel to the slab edge [$mm$].
        """
        super().__init__()
        self.u1 = u1
        self.u1_star = u1_star
        self.k = k
        self.w_1 = w_1
        self.e_par = e_par

    @staticmethod
    def _evaluate(
        u1: MM,
        u1_star: MM,
        k: DIMENSIONLESS,
        w_1: NMM,
        e_par: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(u1=u1, k=k, e_par=e_par)
        raise_if_less_or_equal_to_zero(u1_star=u1_star, w_1=w_1)

        return (u1 / u1_star) + k * (u1 / w_1) * e_par

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.44."""
        _equation: str = r"\frac{u_1}{u_{1^*}} + k \cdot \frac{u_1}{W_1} \cdot e_{par}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"u_1": f"{self.u1:.3f}",
                r"u_{1^*}": f"{self.u1_star:.3f}",
                r"k": f"{self.k:.3f}",
                r"W_1": f"{self.w_1:.3f}",
                r"e_{par}": f"{self.e_par:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\beta",
            result=f"{self._evaluate(self.u1, self.u1_star, self.k, self.w_1, self.e_par):.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
