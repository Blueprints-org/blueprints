"""Formula 5.20 from EN 1992-1-1:2004: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot20DesignModulusElasticity(Formula):
    """Class representing formula 5.20 for the calculation of the design modulus of elasticity, [$E_{cd}$]."""

    label = "5.20"
    source_document = EN_1992_1_1_2004

    def __init__(self, e_cm: MPA, gamma_ce: DIMENSIONLESS = 1.2) -> None:
        r"""[$E_{cd}$] Design modulus of elasticity.

        EN 1992-1-1:2004 art.5.8.6(3) - Formula (5.20)

        Parameters
        ----------
        e_cm : MPA
            [$E_{cm}$] is the characteristic modulus of elasticity of concrete.
        gamma_ce : DIMENSIONLESS, optional
            [$\gamma_{cE}$] is the factor for the design value of the modulus of elasticity. Default is 1.2 which is the recommended value.
        """
        super().__init__()
        self.e_cm = e_cm
        self.gamma_ce = gamma_ce

    @staticmethod
    def _evaluate(e_cm: MPA, gamma_ce: DIMENSIONLESS) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_ce=gamma_ce)
        return e_cm / gamma_ce

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 5.20."""
        return LatexFormula(
            return_symbol=r"E_{cd}",
            result=f"{self:.{n}f}",
            equation=r"\frac{E_{cm}}{\gamma_{CE}}",
            numeric_equation=rf"\frac{{{self.e_cm}}}{{{self.gamma_ce}}}",
            comparison_operator_label="=",
        )
