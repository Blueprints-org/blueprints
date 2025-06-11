"""Formula 6.18 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot18DesignPlasticShearResistance(Formula):
    r"""Class representing formula 6.18 for the calculation of [$V_{pl,Rd}$]."""

    label = "6.18"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a_v: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""[$V_{pl,Rd}$] Calculation of the design plastic shear resistance [$N$].

        EN 1993-1-1:2005 art.6.2.6(2) - Formula (6.18)

        Parameters
        ----------
        a_v : MM2
            [$A_v$] Shear area, to be taken from a subformula from 6.18 [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for resistance of cross-sections.
        """
        super().__init__()
        self.a_v = a_v
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @staticmethod
    def _evaluate(
        a_v: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_v=a_v, f_y=f_y)
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0)

        return (a_v * (f_y / np.sqrt(3))) / gamma_m0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.18."""
        _equation: str = r"\frac{A_v \cdot (f_y / \sqrt{3})}{\gamma_{M0}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_v": f"{self.a_v:.3f}",
                r"f_y": f"{self.f_y:.3f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"V_{pl,Rd}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
