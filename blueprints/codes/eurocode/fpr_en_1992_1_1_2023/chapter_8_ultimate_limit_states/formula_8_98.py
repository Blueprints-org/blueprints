"""Formula 8.98 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot98DistanceToPointOfContraflexure(Formula):
    r"""Class representing formula 8.98 for the calculation of the distance between the centre of the support
    area and the point of contraflexure.

    The standard writes this as an expression bounded from below by [$d_v$], which is implemented as the
    maximum of the two.
    """

    label = "8.98"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        a_p_x: MM,
        a_p_y: MM,
        d_v: MM,
    ) -> None:
        r"""[$a_p$] Distance between the centre of the support area and the point of contraflexure in the
        considered load combination [$mm$].

        FprEN 1992-1-1:2023 (E) art. 8.4.3(2) - Formula (8.98)

        Parameters
        ----------
        a_p_x : MM
            [$a_{p,x}$] Maximum distance from the centroid of the control perimeter (which may be simplified
            according to Figure 8.21a)) to the point on the x-axis where the bending moment [$m_{Ed,x}$] is
            zero. The distance may be calculated according to 8.4.3(3) or using a linear elastic (uncracked)
            model. The local coordinate system [$(x,y)$] has its origin at the centre of the supporting area
            and coincides with the reinforcement directions (principal directions in case of layers which are
            not orthogonal). In large columns, wall ends and wall corners, the origin of the local coordinate
            system may be placed inside the supporting area at a distance [$1,5 d_v$] from the relevant column
            or wall face if it is more favourable [$mm$].
        a_p_y : MM
            [$a_{p,y}$] Maximum distance from the centroid of the control perimeter (which may be simplified
            according to Figure 8.21a)) to the point on the y-axis where the bending moment [$m_{Ed,y}$] is
            zero. The distance may be calculated according to 8.4.3(3) or using a linear elastic (uncracked)
            model. The local coordinate system [$(x,y)$] has its origin at the centre of the supporting area
            and coincides with the reinforcement directions (principal directions in case of layers which are
            not orthogonal). In large columns, wall ends and wall corners, the origin of the local coordinate
            system may be placed inside the supporting area at a distance [$1,5 d_v$] from the relevant column
            or wall face if it is more favourable [$mm$].
        d_v : MM
            [$d_v$] Shear-resisting effective depth of the slab according to Formula (8.91) [$mm$].
        """
        super().__init__()
        self.a_p_x = a_p_x
        self.a_p_y = a_p_y
        self.d_v = d_v

    @staticmethod
    def _evaluate(
        a_p_x: MM,
        a_p_y: MM,
        d_v: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_p_x=a_p_x, a_p_y=a_p_y)
        raise_if_less_or_equal_to_zero(d_v=d_v)

        return max(np.sqrt(a_p_x * a_p_y), d_v)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.98."""
        _equation: str = r"\max\left(\sqrt{a_{p,x} \cdot a_{p,y}}, d_v\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_{p,x}": f"{self.a_p_x:.{n}f}",
                r"a_{p,y}": f"{self.a_p_y:.{n}f}",
                r"d_v": f"{self.d_v:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_{p,x}": rf"{self.a_p_x:.{n}f} \ mm",
                r"a_{p,y}": rf"{self.a_p_y:.{n}f} \ mm",
                r"d_v": rf"{self.d_v:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"a_p",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
