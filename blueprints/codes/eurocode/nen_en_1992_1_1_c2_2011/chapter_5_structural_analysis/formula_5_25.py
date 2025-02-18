"""Formula 5.25 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_negative


class Form5Dot25AxialForceCorrectionFactor(Formula):
    """Class representing formula 5.25 for the calculation of the axial force correction factor [$k_{2}$]."""

    label = "5.25"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, n: DIMENSIONLESS) -> None:
        r"""[$k_{2}$] Axial force correction factor.

        NEN-EN 1992-1-1+C2:2011 art.5.8.6(3) - Formula (5.25)

        Parameters
        ----------
        n : DIMENSIONLESS
            [$n$] Relative axial force, [$N_{ed} / (A_{c} * f_{cd})$] [-].
        """
        super().__init__()
        self.n = n

    @staticmethod
    def _evaluate(n: DIMENSIONLESS) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(n=n)
        k2 = n * 0.30
        return min(k2, 0.20)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.25."""
        return LatexFormula(
            return_symbol=r"k_{2}",
            result=f"{self:.3f}",
            equation=r"\min(0.20; n \cdot 0.30)",
            numeric_equation=rf"\min(0.20; {self.n:.3f} \cdot 0.30)",
            comparison_operator_label="=",
        )
