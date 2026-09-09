"""Formula 8.107 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot107ShearReinforcementRatio(Formula):
    r"""Class representing formula 8.107 for the calculation of the shear reinforcement ratio at the
    investigated control perimeter.
    """

    label = "8.107"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        a_sw: MM2,
        s_r: MM,
        s_t: MM,
    ) -> None:
        r"""[$\rho_w$] Shear reinforcement ratio at the investigated control perimeter [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.4(1) - Formula (8.107)

        Parameters
        ----------
        a_sw : MM2
            [$A_{sw}$] Area of one leg of shear reinforcement [$mm^2$].
        s_r : MM
            [$s_r$] Radial spacing of shear reinforcement, [$s_r = \max(s_0 + s_1/2; s_1)$] where [$s_0$] and
            [$s_1$] are defined in Figure 8.23 a) and should comply with 12.5.1 [$mm$].
        s_t : MM
            [$s_t$] Average tangential spacing of perimeters of shear reinforcement measured at the
            investigated control perimeter, the length of the investigated control perimeter divided by the
            number of shear reinforcement bars arranged on it or near to it [$mm$].
        """
        super().__init__()
        self.a_sw = a_sw
        self.s_r = s_r
        self.s_t = s_t

    @staticmethod
    def _evaluate(
        a_sw: MM2,
        s_r: MM,
        s_t: MM,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_sw=a_sw)
        raise_if_less_or_equal_to_zero(s_r=s_r, s_t=s_t)

        return a_sw / (s_r * s_t)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.107."""
        _equation: str = r"\frac{A_{sw}}{s_r \cdot s_t}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_{sw}": f"{self.a_sw:.{n}f}",
                r"s_r": f"{self.s_r:.{n}f}",
                r"s_t": f"{self.s_t:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"A_{sw}": rf"{self.a_sw:.{n}f} \ mm^2",
                r"s_r": rf"{self.s_r:.{n}f} \ mm",
                r"s_t": rf"{self.s_t:.{n}f} \ mm",
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
            unit="-",
        )
