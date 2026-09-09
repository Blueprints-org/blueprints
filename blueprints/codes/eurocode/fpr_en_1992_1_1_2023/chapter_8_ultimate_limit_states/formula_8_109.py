"""Formula 8.109 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot109MaximumPunchingShearResistance(Formula):
    r"""Class representing formula 8.109 for the calculation of the maximum punching shear resistance."""

    label = "8.109"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        eta_sys: DIMENSIONLESS,
        tau_rd_c: MPA,
    ) -> None:
        r"""[$\tau_{Rd,max}$] Maximum punching shear resistance [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.4.4(5) - Formula (8.109)

        Parameters
        ----------
        eta_sys : DIMENSIONLESS
            [$\eta_{sys}$] Coefficient accounting for the performance of punching shear reinforcing systems,
            according to Formula (8.110) or (8.111), see
            Form8Dot110To111CoefficientForPunchingShearReinforcingSystem [$-$].
        tau_rd_c : MPA
            [$\tau_{Rd,c}$] Punching shear stress resistance of slabs without shear reinforcement according to
            Formula (8.94) [$MPa$].
        """
        super().__init__()
        self.eta_sys = eta_sys
        self.tau_rd_c = tau_rd_c

    @staticmethod
    def _evaluate(
        eta_sys: DIMENSIONLESS,
        tau_rd_c: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(eta_sys=eta_sys, tau_rd_c=tau_rd_c)

        return eta_sys * tau_rd_c

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.109."""
        _equation: str = r"\eta_{sys} \cdot \tau_{Rd,c}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\eta_{sys}": f"{self.eta_sys:.{n}f}",
                r"\tau_{Rd,c}": f"{self.tau_rd_c:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\eta_{sys}": f"{self.eta_sys:.{n}f}",
                r"\tau_{Rd,c}": rf"{self.tau_rd_c:.{n}f} \ MPa",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rd,max}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
