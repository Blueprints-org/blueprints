"""Formula 5.23 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form5Dot23FactorConcreteStrengthClass(Formula):
    """Class representing formula 5.23 for the calculation of the factor for concrete strength class, [$k_{1}$]."""

    label = "5.23"
    source_document = EN_1992_1_1_2004

    def __init__(self, f_ck: MPA) -> None:
        r"""[$k_{1}$] Factor for concrete strength class.

        EN 1992-1-1:2004 art.5.8.6(3) - Formula (5.23)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] is the characteristic compressive strength of concrete.
        """
        super().__init__()
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(f_ck: MPA) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ck=f_ck)
        return (f_ck / 20) ** 0.5

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.23."""
        return LatexFormula(
            return_symbol=r"k_{1}",
            result=f"{self:.{n}f}",
            equation=r"\sqrt{\frac{f_{ck}}{20}}",
            numeric_equation=rf"\sqrt{{\frac{{{self.f_ck:.{n}f}}}{{20}}}}",
            comparison_operator_label="=",
        )
