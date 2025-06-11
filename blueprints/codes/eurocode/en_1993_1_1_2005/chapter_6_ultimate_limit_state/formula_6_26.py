"""Formula 6.26 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot26VplTRdIOrHSection(Formula):
    r"""Class representing formula 6.26 for the calculation of [$V_{pl,T,Rd}$]."""

    label = "6.26"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        tau_t_ed: MPA,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        v_pl_rd: N,
    ) -> None:
        r"""[$V_{pl,T,Rd}$] Calculation of the design plastic shear resistance for I or H sections [$N$].

        EN 1993-1-1:2005 art.6.2.7(9) - Formula (6.26)

        Parameters
        ----------
        tau_t_ed : MPA
            [$\tau_{Ed}$] Design shear stress due to St. Venant torsion [$MPa$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPA$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for resistance of cross-sections.
        v_pl_rd : N
            [$V_{pl,Rd}$] Plastic shear resistance given in 6.2.6 [$N$].
        """
        super().__init__()
        self.tau_t_ed = tau_t_ed
        self.f_y = f_y
        self.gamma_m0 = gamma_m0
        self.v_pl_rd = v_pl_rd

    @staticmethod
    def _evaluate(
        tau_t_ed: MPA,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
        v_pl_rd: N,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0, f_y=f_y)
        under_root = 1 - (tau_t_ed / (1.25 * (f_y / np.sqrt(3)) / gamma_m0))
        raise_if_negative(tau_t_ed=tau_t_ed, v_pl_rd=v_pl_rd, under_root=under_root)

        return np.sqrt(1 - (tau_t_ed / (1.25 * (f_y / np.sqrt(3)) / gamma_m0))) * v_pl_rd

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.26."""
        _equation: str = r"\sqrt{1 - \frac{\tau_{t,Ed}}{1.25 \cdot \left( f_y / \sqrt{3} \right) / \gamma_{M0}}} \cdot V_{pl,Rd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\tau_{t,Ed}": f"{self.tau_t_ed:.3f}",
                r"f_y": f"{self.f_y:.3f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.3f}",
                r"V_{pl,Rd}": f"{self.v_pl_rd:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"V_{pl,T,Rd}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
