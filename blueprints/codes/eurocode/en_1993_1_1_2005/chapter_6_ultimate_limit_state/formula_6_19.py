"""Formula 6.19 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot19CheckDesignElasticShearResistance(Formula):
    r"""Class representing formula 6.19 for checking the design elastic shear resistance."""

    label = "6.19"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        tau_ed: MPA,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""Check the design elastic shear resistance.

        EN 1993-1-1:2005 art.6.2.6(4) - Formula (6.19)

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Design shear stress [MPa].
        f_y : MPA
            [$f_{y}$] Yield strength of the material [MPa].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor [-].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @staticmethod
    def _evaluate(
        tau_ed: MPA,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0, f_y=f_y)
        raise_if_negative(tau_ed=tau_ed)

        return tau_ed / (f_y / (3**0.5 * gamma_m0)) <= 1.0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.19."""
        _equation: str = r"\left( \frac{\tau_{Ed}}{f_{y} / (\sqrt{3} \cdot \gamma_{M0})} \leq 1.0 \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"f_{y}": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
