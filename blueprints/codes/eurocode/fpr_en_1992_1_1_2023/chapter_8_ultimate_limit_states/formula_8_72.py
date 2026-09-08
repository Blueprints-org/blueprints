"""Formula 8.72 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot72LongitudinalStrainInTensileFlange(Formula):
    r"""Class representing formula 8.72 for the estimation of the longitudinal strain in the tensile flange.

    The strain feeds the strength reduction factor of Formula (8.45), which 8.2.5(5) requires when lower angles
    of the inclined compression field in the tensile flange than those of 8.2.5(3) are adopted.

    The expression is the one of Formula (8.47) with a lower bound of zero added by the standard. That bound is
    the reason this class accepts a negative force in the tension chord where Formula (8.47) refuses one: a
    guard against a negative force would make the printed bound unreachable.
    """

    label = "8.72"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        f_td: N,
        a_st: MM2,
        e_s: MPA,
    ) -> None:
        r"""[$\epsilon_x$] Longitudinal strain in the tensile flange [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.2.5(5) - Formula (8.72)

        Parameters
        ----------
        f_td : N
            [$F_{td}$] Force in the tension chord, refer to 8.2.3(7) and (8) [$N$].
        a_st : MM2
            [$A_{st}$] Area of the longitudinal reinforcement in the tension chord, refer to 8.2.3(7) and (8)
            [$mm^2$].
        e_s : MPA
            [$E_s$] Modulus of elasticity of reinforcement steel [$MPa$].
        """
        super().__init__()
        self.f_td = f_td
        self.a_st = a_st
        self.e_s = e_s

    @staticmethod
    def _evaluate(
        f_td: N,
        a_st: MM2,
        e_s: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(a_st=a_st, e_s=e_s)

        return max(f_td / (a_st * e_s), 0)

    def latex(self, n: int = 4) -> LatexFormula:
        """Returns LatexFormula object for formula 8.72."""
        _equation: str = r"\max\left(\frac{F_{td}}{A_{st} \cdot E_s}, 0\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_{td}": f"{self.f_td:.{n}f}",
                r"A_{st}": f"{self.a_st:.{n}f}",
                r"E_s": f"{self.e_s:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"F_{td}": rf"{self.f_td:.{n}f} \ N",
                r"A_{st}": rf"{self.a_st:.{n}f} \ mm^2",
                r"E_s": rf"{self.e_s:.{n}f} \ MPa",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\epsilon_x",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
