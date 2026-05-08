"""Formula 8.43 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot43ShearReinforcementRatio(Formula):
    r"""Class representing formula 8.43 for the shear reinforcement ratio.

    prEN 1992-1-1:2023 art. 8.2.3 - Formula (8.43)

    Formula
    -------
    $\rho_w = \frac{A_{sw}}{b_w \cdot s}$

    Parameters
    ----------
    a_sw : MM2
        [$A_{sw}$] Shear reinforcement area ($mm^2$).
    b_w : MM
        [$b_w$] Width of the web or width of the shear plane ($mm$).
    s : MM
        [$s$] Spacing of the shear reinforcement ($mm$).
    """

    label = "8.43"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        a_sw: MM2,
        b_w: MM,
        s: MM,
    ) -> None:
        super().__init__()
        self.a_sw = a_sw
        self.b_w = b_w
        self.s = s

    @staticmethod
    def _evaluate(a_sw: MM2, b_w: MM, s: MM) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_sw=a_sw)
        raise_if_less_or_equal_to_zero(b_w=b_w, s=s)
        return a_sw / (b_w * s)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.43."""
        _equation: str = r"\frac{A_{sw}}{b_w \cdot s}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_{sw}": f"{self.a_sw:.{n}f}",
                r"b_w": f"{self.b_w:.{n}f}",
                r"s": f"{self.s:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_{sw}": rf"{self.a_sw:.{n}f} \ mm^2",
                r"b_w": rf"{self.b_w:.{n}f} \ mm",
                r"s": rf"{self.s:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )

        return LatexFormula(
            return_symbol=r"\rho_w",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="",
        )
