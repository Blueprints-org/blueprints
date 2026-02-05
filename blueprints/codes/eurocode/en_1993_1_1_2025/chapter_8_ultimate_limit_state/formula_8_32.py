"""Formula 8.32 from EN 1993-1-1:2025: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2025 import EN_1993_1_1_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot32VplTRdChannelSection(Formula):
    r"""Class representing formula 8.32 for the calculation of [$V_{pl,T,Rd}$]."""

    label = "8.32"
    source_document = EN_1993_1_1_2025

    def __init__(
        self,
        tau_t_ed: MPA,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        tau_w_ed: MPA,
        v_pl_rd: N,
    ) -> None:
        r"""[$V_{pl,T,Rd}$] Calculation of the shear resistance for channel sections [$N$].

        EN 1993-1-1:2025 art.8.2.7(9) - Formula (8.32)

        Parameters
        ----------
        tau_t_ed : MPA
            [$\tau_{Ed}$] Design shear stress due to St. Venant torsion [$MPa$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for resistance of cross-sections.
        tau_w_ed : MPA
            [$\tau_{w,Ed}$] Design shear stress due to warping [$MPa$].
        v_pl_rd : N
            [$V_{pl,Rd}$] Plastic shear resistance [$N$].
        """
        super().__init__()
        self.tau_t_ed = tau_t_ed
        self.f_y = f_y
        self.gamma_m0 = gamma_m0
        self.tau_w_ed = tau_w_ed
        self.v_pl_rd = v_pl_rd

    @staticmethod
    def _evaluate(
        tau_t_ed: MPA,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        tau_w_ed: MPA,
        v_pl_rd: N,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0, f_y=f_y)
        under_root = 1 - (tau_t_ed / (1.25 * (f_y / np.sqrt(3)) / gamma_m0))
        raise_if_negative(tau_t_ed=tau_t_ed, v_pl_rd=v_pl_rd, tau_w_ed=tau_w_ed, under_root=under_root)

        return (np.sqrt(1 - (tau_t_ed / (1.25 * (f_y / np.sqrt(3)) / gamma_m0))) - (tau_w_ed / ((f_y / np.sqrt(3)) / gamma_m0))) * v_pl_rd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.32."""
        _equation: str = (
            r"\left( \sqrt{1 - \frac{\tau_{t,Ed}}{1.25 \cdot \left( f_y / \sqrt{3} \right) / \gamma_{M0}}} - "
            r"\frac{\tau_{w,Ed}}{\left( f_y / \sqrt{3} \right) / \gamma_{M0}} \right) \cdot V_{pl,Rd}"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\tau_{t,Ed}": f"{self.tau_t_ed:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
                r"\tau_{w,Ed}": f"{self.tau_w_ed:.{n}f}",
                r"V_{pl,Rd}": f"{self.v_pl_rd:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"V_{pl,T,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
