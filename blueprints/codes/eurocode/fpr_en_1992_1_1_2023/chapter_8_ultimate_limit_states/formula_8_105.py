"""Formula 8.105 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot105StrengthReductionCoefficientForShearResistance(Formula):
    r"""Class representing formula 8.105 for the calculation of the strength reduction coefficient for the
    shear resistance [$\tau_{Rd,c}$].
    """

    label = "8.105"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        tau_rd_c: MPA,
        tau_ed: MPA,
    ) -> None:
        r"""[$\eta_c$] Strength reduction coefficient for shear resistance [$\tau_{Rd,c}$] [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.4(1) - Formula (8.105)

        Parameters
        ----------
        tau_rd_c : MPA
            [$\tau_{Rd,c}$] Punching shear stress resistance of slabs without shear reinforcement according to
            Formula (8.94) [$MPa$].
        tau_ed : MPA
            [$\tau_{Ed}$] Design punching shear stress at the control perimeter, according to Formula (8.92)
            or (8.93) [$MPa$].
        """
        super().__init__()
        self.tau_rd_c = tau_rd_c
        self.tau_ed = tau_ed

    @staticmethod
    def _evaluate(
        tau_rd_c: MPA,
        tau_ed: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(tau_rd_c=tau_rd_c)
        raise_if_less_or_equal_to_zero(tau_ed=tau_ed)

        return tau_rd_c / tau_ed

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.105."""
        _equation: str = r"\frac{\tau_{Rd,c}}{\tau_{Ed}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Rd,c}": f"{self.tau_rd_c:.{n}f}",
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Rd,c}": rf"{self.tau_rd_c:.{n}f} \ MPa",
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\eta_c",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
