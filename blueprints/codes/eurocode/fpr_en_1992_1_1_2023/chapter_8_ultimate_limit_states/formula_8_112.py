"""Formula 8.112 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot112OuterControlPerimeterWithoutShearReinforcement(Formula):
    r"""Class representing formula 8.112 for the calculation of the outer control perimeter at which shear
    reinforcement is not required.
    """

    label = "8.112"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        b_0_5: MM,
        d_v: MM,
        d_v_out: MM,
        eta_c: DIMENSIONLESS,
    ) -> None:
        r"""[$b_{0,5,out}$] Outer control perimeter at which shear reinforcement is not required, see
        Figure 8.24 [$mm$].

        FprEN 1992-1-1:2023 (E) art. 8.4.4(7) - Formula (8.112)

        Parameters
        ----------
        b_0_5 : MM
            [$b_{0,5}$] Control perimeter located at a distance [$d_v/2$] from the face of the supporting area
            according to 8.4.2(2) [$mm$].
        d_v : MM
            [$d_v$] Shear-resisting effective depth of the slab according to Formula (8.91) [$mm$].
        d_v_out : MM
            [$d_{v,out}$] Shear-resisting effective depth of the outer shear reinforcement according to
            Formula (8.108), see Form8Dot108ShearResistingEffectiveDepthOuterShearReinforcement [$mm$].
        eta_c : DIMENSIONLESS
            [$\eta_c$] As defined in Formula (8.105), see
            Form8Dot105StrengthReductionCoefficientForShearResistance [$-$].
        """
        super().__init__()
        self.b_0_5 = b_0_5
        self.d_v = d_v
        self.d_v_out = d_v_out
        self.eta_c = eta_c

    @staticmethod
    def _evaluate(
        b_0_5: MM,
        d_v: MM,
        d_v_out: MM,
        eta_c: DIMENSIONLESS,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(b_0_5=b_0_5, d_v=d_v, d_v_out=d_v_out, eta_c=eta_c)

        return b_0_5 * ((d_v / d_v_out) * (1 / eta_c)) ** 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.112."""
        _equation: str = r"b_{0,5} \cdot \left(\frac{d_v}{d_{v,out}} \cdot \frac{1}{\eta_c}\right)^2"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_{0,5}": f"{self.b_0_5:.{n}f}",
                r"d_v": f"{self.d_v:.{n}f}",
                r"d_{v,out}": f"{self.d_v_out:.{n}f}",
                r"\eta_c": f"{self.eta_c:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_{0,5}": rf"{self.b_0_5:.{n}f} \ mm",
                r"d_v": rf"{self.d_v:.{n}f} \ mm",
                r"d_{v,out}": rf"{self.d_v_out:.{n}f} \ mm",
                r"\eta_c": f"{self.eta_c:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"b_{0,5,out}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
