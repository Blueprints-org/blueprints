"""Formula 8.93 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA, N_MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot93DesignPunchingShearStressFromDetailedAnalysis(Formula):
    r"""Class representing formula 8.93 for the calculation of the design punching shear stress at the control
    perimeter directly from a detailed analysis of the shear stress distribution.

    This is the alternative of 8.4.2(7) to Formula (8.92): the concentration of the shear forces is already
    contained in the shear force per unit width that the analysis returns, so no coefficient [$\beta_e$] of
    Table 8.3 appears here. According to 8.4.2(8) this route is required, rather than optional, where significant
    concentrated loads of at least [$0,2 V_{Ed}$] act closer to the control perimeter than [$3 d_v$].
    """

    label = "8.93"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        v_ed: N_MM,
        d_v: MM,
    ) -> None:
        r"""[$\tau_{Ed}$] Design punching shear stress at the control perimeter [$b_{0,5}$] [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.4.2(7) - Formula (8.93)

        Parameters
        ----------
        v_ed : N_MM
            [$v_{Ed}$] Shear force per unit width along the control perimeter, from a method accounting for
            equilibrium and compatibility conditions of the slab, for instance a linear elastic analysis. It may
            be averaged according to 8.2.1(6), where [$2d$] should be replaced by [$2 d_v$]. Note that Formula
            (8.92) uses [$V_{Ed}$], a shear force in N, which is a different quantity [$N/mm$].
        d_v : MM
            [$d_v$] Shear-resisting effective depth of the slab according to Formula (8.91) [$mm$].
        """
        super().__init__()
        self.v_ed = v_ed
        self.d_v = d_v

    @staticmethod
    def _evaluate(
        v_ed: N_MM,
        d_v: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed=v_ed)
        raise_if_less_or_equal_to_zero(d_v=d_v)

        return v_ed / d_v

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.93."""
        _equation: str = r"\frac{v_{Ed}}{d_v}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"v_{Ed}": f"{self.v_ed:.{n}f}",
                r"d_v": f"{self.d_v:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"v_{Ed}": rf"{self.v_ed:.{n}f} \ N/mm",
                r"d_v": rf"{self.d_v:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
