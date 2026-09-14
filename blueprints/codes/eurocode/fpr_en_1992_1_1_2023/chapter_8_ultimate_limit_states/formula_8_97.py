"""Formula 8.97 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot97ReplacementEffectiveDepth(Formula):
    r"""Class representing formula 8.97 for the calculation of the replacement value of the shear-resisting
    effective depth [$d_v$] to be used in Formula (8.94), for a distance to the point of contraflexure
    smaller than [$8 d_v$].
    """

    label = "8.97"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        a_p: MM,
        d_v: MM,
    ) -> None:
        r"""[$a_{pd}$] Replacement value for [$d_v$] in Formula (8.94) [$mm$].

        FprEN 1992-1-1:2023 (E) art. 8.4.3(2) - Formula (8.97)

        For distances between the centre of the support area and the point of contraflexure in the
        considered load combination [$a_p$] smaller than [$8 d_v$], the value of [$d_v$] in Formula (8.94)
        may be replaced by [$a_{pd}$].

        Parameters
        ----------
        a_p : MM
            [$a_p$] Distance between the centre of the support area and the point of contraflexure in the
            considered load combination according to Formula (8.98), see
            Form8Dot98DistanceToPointOfContraflexure [$mm$].
        d_v : MM
            [$d_v$] Shear-resisting effective depth of the slab according to Formula (8.91) [$mm$].
        """
        super().__init__()
        self.a_p = a_p
        self.d_v = d_v

    @staticmethod
    def _evaluate(
        a_p: MM,
        d_v: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_p=a_p)
        raise_if_less_or_equal_to_zero(d_v=d_v)

        return np.sqrt((a_p / 8) * d_v)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.97."""
        _equation: str = r"\sqrt{\frac{a_p}{8} \cdot d_v}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_p": f"{self.a_p:.{n}f}",
                r"d_v": f"{self.d_v:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_p": rf"{self.a_p:.{n}f} \ mm",
                r"d_v": rf"{self.d_v:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"a_{pd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
