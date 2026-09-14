"""Formula 8.91 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot91ShearResistingEffectiveDepth(Formula):
    r"""Class representing formula 8.91 for the calculation of the shear-resisting effective depth of a slab."""

    label = "8.91"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        d_vx: MM,
        d_vy: MM,
    ) -> None:
        r"""[$d_v$] Shear-resisting effective depth of the slab [$mm$].

        FprEN 1992-1-1:2023 (E) art. 8.4.2(1) - Formula (8.91)

        The shear-resisting effective depth is the distance from the supporting area to the average level of the
        reinforcement layers, see Figure 8.17. Where the column penetrates into the slab by more than [$d/20$],
        8.4.2(1) refers to Figure 8.17 c) for its determination, which this class cannot express.

        Parameters
        ----------
        d_vx : MM
            [$d_{vx}$] Nominal value of the shear-resisting effective depth in the x-direction. NOTE 1 of
            8.4.2(1) states that the nominal values apply unless the National Annex permits alternative use of
            [$d_{dx}$] and [$d_{dy}$] [$mm$].
        d_vy : MM
            [$d_{vy}$] Nominal value of the shear-resisting effective depth in the y-direction [$mm$].
        """
        super().__init__()
        self.d_vx = d_vx
        self.d_vy = d_vy

    @staticmethod
    def _evaluate(
        d_vx: MM,
        d_vy: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(d_vx=d_vx, d_vy=d_vy)

        return (d_vx + d_vy) / 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.91."""
        _equation: str = r"\frac{d_{vx} + d_{vy}}{2}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_{vx}": f"{self.d_vx:.{n}f}",
                r"d_{vy}": f"{self.d_vy:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_{vx}": rf"{self.d_vx:.{n}f} \ mm",
                r"d_{vy}": rf"{self.d_vy:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"d_v",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
