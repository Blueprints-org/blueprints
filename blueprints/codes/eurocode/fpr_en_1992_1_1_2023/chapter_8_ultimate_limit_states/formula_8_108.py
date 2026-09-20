"""Formula 8.108 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot108ShearResistingEffectiveDepthOuterShearReinforcement(Formula):
    r"""Class representing formula 8.108 for the calculation of the shear-resisting effective depth of the
    outer shear reinforcement.
    """

    label = "8.108"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        d_x: MM,
        d_y: MM,
        c_v: MM,
    ) -> None:
        r"""[$d_{v,out}$] Shear-resisting effective depth of the outer shear reinforcement, see 8.4.4(4) [$mm$].

        FprEN 1992-1-1:2023 (E) art. 8.4.4(4), NOTE - Formula (8.108)

        Parameters
        ----------
        d_x : MM
            [$d_x$] Effective depth in the x direction [$mm$].
        d_y : MM
            [$d_y$] Effective depth in the y direction [$mm$].
        c_v : MM
            [$c_v$] Distance defined in Figure 8.23, unless the National Annex gives a different value [$mm$].
        """
        super().__init__()
        self.d_x = d_x
        self.d_y = d_y
        self.c_v = c_v

    @staticmethod
    def _evaluate(
        d_x: MM,
        d_y: MM,
        c_v: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(d_x=d_x, d_y=d_y)
        raise_if_negative(c_v=c_v)

        return (d_x + d_y) / 2 - c_v

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.108."""
        _equation: str = r"\frac{d_x + d_y}{2} - c_v"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_x": f"{self.d_x:.{n}f}",
                r"d_y": f"{self.d_y:.{n}f}",
                r"c_v": f"{self.c_v:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_x": rf"{self.d_x:.{n}f} \ mm",
                r"d_y": rf"{self.d_y:.{n}f} \ mm",
                r"c_v": rf"{self.c_v:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"d_{v,out}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
