"""Formula 6.63 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot63ConcentratedResistanceForce(Formula):
    r"""Class representing formula 6.63 for the calculation of [$F_{Rdu}$]."""

    label = "6.63"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        a_c0: MM2,
        a_c1: MM2,
        f_cd: MPA,
    ) -> None:
        r"""[$F_{Rdu}$] Calculation of [$F_{Rdu}$].

        EN 1992-1-1:2004 art.6.7(2) - Formula (6.63)

        Parameters
        ----------
        a_c0 : MM2
            [$A_{c0}$] Loaded area [$mm^2$].
        a_c1 : MM2
            [$A_{c1}$] Maximum design distribution area with a similar shape to [$A_{c0}$] [$mm^2$].
        f_cd : MPA
            [$f_{cd}$] Design compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.a_c0 = a_c0
        self.a_c1 = a_c1
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        a_c0: MM2,
        a_c1: MM2,
        f_cd: MPA,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_c1=a_c1, f_cd=f_cd)
        raise_if_less_or_equal_to_zero(a_c0=a_c0)

        return min(a_c0 * f_cd * np.sqrt(a_c1 / a_c0), 3 * f_cd * a_c0)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.63."""
        _equation: str = r"\min \left( A_{c0} \cdot f_{cd} \cdot \sqrt{\frac{A_{c1}}{A_{c0}}}, 3 \cdot f_{cd} \cdot A_{c0} \right)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_{c0}": f"{self.a_c0:.{n}f}",
                r"A_{c1}": f"{self.a_c1:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"F_{Rdu}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
