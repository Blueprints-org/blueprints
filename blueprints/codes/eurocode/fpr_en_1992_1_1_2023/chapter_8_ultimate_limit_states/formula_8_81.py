"""Formula 8.81 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_negative


class Form8Dot81DesignTorsionalCapacity(Formula):
    r"""Class representing formula 8.81 for the design torsional capacity of a single cell, thin-walled section
    or a sub-section with constant effective wall thickness.

    The three candidates are the resistances of Formulas (8.82), (8.83) and (8.84), which are yielding of the
    shear reinforcement, yielding of the longitudinal reinforcement, and crushing of the compression field in
    concrete. Whichever gives way first governs, so the standard takes the smallest.

    The standard determines the three on the basis of Annex G, and says the capacity according to this formula
    should be used when combinations of internal forces are verified according to 8.3.6.
    """

    label = "8.81"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        tau_t_rd_sw: MPA,
        tau_t_rd_sl: MPA,
        tau_t_rd_max: MPA,
    ) -> None:
        r"""[$\tau_{t,Rd}$] Design torsional capacity [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.3.4(1) - Formula (8.81)

        Parameters
        ----------
        tau_t_rd_sw : MPA
            [$\tau_{t,Rd,sw}$] Torsional stress resistance governed by yielding of the shear reinforcement,
            refer to Formula (8.82) [$MPa$].
        tau_t_rd_sl : MPA
            [$\tau_{t,Rd,sl}$] Torsional stress resistance governed by yielding of the longitudinal
            reinforcement, refer to Formula (8.83) [$MPa$].
        tau_t_rd_max : MPA
            [$\tau_{t,Rd,max}$] Torsional stress resistance governed by crushing of the compression field in
            concrete, refer to Formula (8.84) [$MPa$].
        """
        super().__init__()
        self.tau_t_rd_sw = tau_t_rd_sw
        self.tau_t_rd_sl = tau_t_rd_sl
        self.tau_t_rd_max = tau_t_rd_max

    @staticmethod
    def _evaluate(
        tau_t_rd_sw: MPA,
        tau_t_rd_sl: MPA,
        tau_t_rd_max: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(tau_t_rd_sw=tau_t_rd_sw, tau_t_rd_sl=tau_t_rd_sl, tau_t_rd_max=tau_t_rd_max)

        return min(tau_t_rd_sw, tau_t_rd_sl, tau_t_rd_max)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.81."""
        # \lbrace and \rbrace rather than \{ and \}: they render identically, but a backslash in front of a
        # brace is eaten by the Markdown parser before the maths is rendered, which breaks the equation on
        # GitHub. Seen on the pull request for this clause.
        _equation: str = r"\min\left\lbrace \tau_{t,Rd,sw}; \tau_{t,Rd,sl}; \tau_{t,Rd,max} \right\rbrace"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{t,Rd,sw}": f"{self.tau_t_rd_sw:.{n}f}",
                r"\tau_{t,Rd,sl}": f"{self.tau_t_rd_sl:.{n}f}",
                r"\tau_{t,Rd,max}": f"{self.tau_t_rd_max:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{t,Rd,sw}": rf"{self.tau_t_rd_sw:.{n}f} \ MPa",
                r"\tau_{t,Rd,sl}": rf"{self.tau_t_rd_sl:.{n}f} \ MPa",
                r"\tau_{t,Rd,max}": rf"{self.tau_t_rd_max:.{n}f} \ MPa",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\tau_{t,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
