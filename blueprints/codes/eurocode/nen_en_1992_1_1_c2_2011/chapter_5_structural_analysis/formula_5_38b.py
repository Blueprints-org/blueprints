r"""Formula 5.38b from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form5Dot38bCheckRelativeEccentricityRatio(Formula):
    r"""Class representing formula 5.38b for check of relative eccentricity ratio."""

    label = "5.38b"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        e_y: MM,
        e_z: MM,
        b_eq: MM,
        h_eq: MM,
    ) -> None:
        r"""Check the excentricity of the loads in x and y direction.

        NEN-EN 1992-1-1+C2:2011 art.5.8.9(3) - Formula (5.38b)

        Parameters
        ----------
        e_y : MM
            [$e_{y}$] Eccentricity along y-axis [$mm$].
        e_z : MM
            [$e_{z}$] Eccentricity along z-axis [$mm$].
        b_eq : MM
            [$b_{eq}$] Equivalent width [$mm$].
        h_eq : MM
            [$h_{eq}$] Equivalent depth [$mm$].
        """
        super().__init__()
        self.e_y = e_y
        self.e_z = e_z
        self.b_eq = b_eq
        self.h_eq = h_eq

    @staticmethod
    def _evaluate(
        e_y: MM,
        e_z: MM,
        b_eq: MM,
        h_eq: MM,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(e_y=e_y, e_z=e_z)
        raise_if_less_or_equal_to_zero(b_eq=b_eq, h_eq=h_eq)

        # The formula is simplified to avoid division by zero.
        if e_y == 0 or e_z == 0:
            return True

        return (e_y / h_eq) / (e_z / b_eq) <= 0.2 or (e_z / b_eq) / (e_y / h_eq) <= 0.2

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.38b."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\left(\frac{e_{y}/h_{eq}}{e_{z}/b_{eq}} \leq 0.2 \text{ or } \frac{e_{z}/b_{eq}}{e_{y}/h_{eq}} \leq 0.2 \right)",
            numeric_equation=rf"\left(\frac{{{self.e_y:.3f}/{self.h_eq:.3f}}}{{{self.e_z:.3f}/{self.b_eq:.3f}}} "
            rf"\leq 0.2 \text{{ or }} \frac{{{self.e_z:.3f}/{self.b_eq:.3f}}}{{{self.e_y:.3f}/{self.h_eq:.3f}}} \leq 0.2 \right)",
            comparison_operator_label="\\to",
            unit="",
        )
