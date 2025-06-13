"""Formula 5.16 from EN 1993-5:2007 Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1993_5_2007 import EN_1993_5_2007
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot16PlasticDesignResistance(Formula):
    """Class representing formula 5.16 for the calculation of the plastic design resistance of the cross-section, [$N_{pl,Rd}$]."""

    label = "5.16"
    source_document = EN_1993_5_2007

    def __init__(
        self,
        a: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""[$N_{pl,Rd}$] Plastic design resistance of the cross-section [$N$].

        EN 1993-5:2007 art.5.2.3 (9) - Formula (5.16)

        Parameters
        ----------
        a : MM2
            [$A$] Area of the cross-section [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial factor according to 5.1.1 (4) [$-$].
        """
        super().__init__()
        self.a = a
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @staticmethod
    def _evaluate(
        a: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0)
        raise_if_negative(f_y=f_y, a=a)

        return (a * f_y) / gamma_m0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.16."""
        return LatexFormula(
            return_symbol=r"N_{pl,Rd}",
            result=f"{self:.{n}f}",
            equation=r"\frac{A \cdot f_y}{\gamma_{M0}}",
            numeric_equation=rf"\frac{{{self.a:.{n}f} \cdot {self.f_y:.{n}f}}}{{{self.gamma_m0:.{n}f}}}",
            comparison_operator_label="=",
            unit="N",
        )
