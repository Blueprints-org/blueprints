"""Formula 5.38a from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot38aCheckRelativeSlendernessRatio(Formula):
    r"""Class representing formula 5.38a for check of relative slenderness ratio."""

    label = "5.38a"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        lambda_y: DIMENSIONLESS,
        lambda_z: DIMENSIONLESS,
    ) -> None:
        r"""Check the ratio of the slenderness in y-direction and z-direction.

        NEN-EN 1992-1-1+C2:2011 art.5.8.9(3) - Formula (5.38a)

        Parameters
        ----------
        lambda_y : DIMENSIONLESS
            [$\lambda_{y}$] Slenderness ratio in y-direction [-].
        lambda_z : DIMENSIONLESS
            [$\lambda_{z}$] Slenderness ratio in z-direction [-].
        """
        super().__init__()
        self.lambda_y = lambda_y
        self.lambda_z = lambda_z

    @staticmethod
    def _evaluate(
        lambda_y: float,
        lambda_z: float,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(lambda_y=lambda_y, lambda_z=lambda_z)

        return (lambda_y / lambda_z <= 2) and (lambda_z / lambda_y <= 2)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.38a."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\left( \frac{\lambda_{y}}{\lambda_{z}} \leq 2 \text{ and } \frac{\lambda_{z}}{\lambda_{y}} \leq 2 \right)",
            numeric_equation=rf"\left( \frac{{{self.lambda_y:.3f}}}{{{self.lambda_z:.3f}}} \leq 2 \text{{ and }} "
            rf"\frac{{{self.lambda_z:.3f}}}{{{self.lambda_y:.3f}}} \leq 2 \right)",
            comparison_operator_label="\\to",
            unit="",
        )
