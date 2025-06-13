"""Formula 6.6n from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form6Dot6nStrengthReductionFactor(Formula):
    r"""Class representing formula 6.6n for the calculation of the strength reduction factor, [$\nu$]."""

    label = "6.6n"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        r"""[$\nu$] Strength reduction factor for concrete cracked in shear [$-$].

        EN 1992-1-1:2004 art.6.2.2 (6) - Formula (6.6n)

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

        return 0.6 * (1 - f_ck / 250)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.6n."""
        return LatexFormula(
            return_symbol=r"\nu",
            result=f"{self:.{n}f}",
            equation=r"0.6 \cdot \left(1 - \frac{f_{ck}}{250}\right)",
            numeric_equation=rf"0.6 \cdot \left(1 - \frac{{{self.f_ck:.{n}f}}}{{250}}\right)",
            comparison_operator_label="=",
            unit="-",
        )
