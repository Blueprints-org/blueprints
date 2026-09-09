"""Formula 8.75 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot75LongitudinalShearStressDueToCompositeAction(Formula):
    r"""Class representing formula 8.75 for the calculation of the longitudinal shear stress between concrete
    interfaces due to composite action.
    """

    label = "8.75"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        beta_new: DIMENSIONLESS,
        v_ed: N,
        z: MM,
        b_i: MM,
    ) -> None:
        r"""[$\tau_{Edi}$] Longitudinal shear stress between concrete interfaces due to composite action [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.2.6(4) - Formula (8.75)

        Parameters
        ----------
        beta_new : DIMENSIONLESS
            [$\beta_{new}$] Ratio of the longitudinal force in the new concrete area and the total longitudinal
            force either in the compression or tension zone, both calculated for the section considered [$-$].
        v_ed : N
            [$V_{Ed}$] Shear force acting perpendicular to the interface. Note that Formula (8.74) uses
            [$V_{Edi}$], the shear force acting parallel to the interface, which is a different quantity [$N$].
        z : MM
            [$z$] Lever arm of composite section [$mm$].
        b_i : MM
            [$b_i$] Width of the interface [$mm$].
        """
        super().__init__()
        self.beta_new = beta_new
        self.v_ed = v_ed
        self.z = z
        self.b_i = b_i

    @staticmethod
    def _evaluate(
        beta_new: DIMENSIONLESS,
        v_ed: N,
        z: MM,
        b_i: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(beta_new=beta_new, v_ed=v_ed)
        raise_if_less_or_equal_to_zero(z=z, b_i=b_i)

        return beta_new * v_ed / (z * b_i)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.75."""
        _equation: str = r"\frac{\beta_{new} \cdot V_{Ed}}{z \cdot b_i}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\beta_{new}": f"{self.beta_new:.{n}f}",
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
                r"z": f"{self.z:.{n}f}",
                r"b_i": f"{self.b_i:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                # The ratio is dimensionless, so it carries no unit here.
                r"\beta_{new}": f"{self.beta_new:.{n}f}",
                r"V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                r"z": rf"{self.z:.{n}f} \ mm",
                r"b_i": rf"{self.b_i:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Edi}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
