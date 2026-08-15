"""Formula 8.29 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot29MechanicalShearSpan(Formula):
    """Class representing formula 8.29 for the calculation of the mechanical shear span, which may replace
    the effective depth in Formula (8.27).
    """

    label = "8.29"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, a_cs: MM, d: MM) -> None:
        r"""[$a_v$] Mechanical shear span [$mm$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (3) - Formula (8.29)

        The value of [$d$] in Formula (8.27) may be replaced by [$a_v$], for members with an effective shear
        span [$a_{cs}$] shorter than [$4 \cdot d$]. That condition is a matter of applicability rather than a
        branch of the formula, so it is left to the caller and not enforced here.

        Parameters
        ----------
        a_cs : MM
            [$a_{cs}$] Effective shear span with respect to the control section according to Formula (8.30),
            see Form8Dot30EffectiveShearSpan [$mm$].
        d : MM
            [$d$] Effective depth [$mm$].
        """
        super().__init__()
        self.a_cs = a_cs
        self.d = d

    @staticmethod
    def _evaluate(a_cs: MM, d: MM) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        # An effective depth or shear span of zero is not a cross-section. The standard prints no such
        # condition, so this is an addition made here, consistent with (8.22) to (8.24) and with (8.31),
        # where a_cs sits in a denominator and is guarded the same way.
        raise_if_less_or_equal_to_zero(a_cs=a_cs, d=d)

        return np.sqrt(a_cs / 4 * d)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.29."""
        _equation: str = r"\sqrt{\frac{a_{cs}}{4} \cdot d}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_{cs}": f"{self.a_cs:.{n}f}",
                r"\cdot d": rf"\cdot {self.d:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"a_{cs}": rf"{self.a_cs:.{n}f} \ mm",
                r"\cdot d": rf"\cdot {self.d:.{n}f} \ mm",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"a_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
