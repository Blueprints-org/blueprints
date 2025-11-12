"""Formula 12.5 and 12.6 from EN 1992-1-1:2004: Chapter 12 - Plain and Lightly Reinforced Concrete Structures."""

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_12_plain_and_lightly_reinforced_concrete_structures.formula_12_3 import (
    Form12Dot3PlainConcreteShearStress,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_12_plain_and_lightly_reinforced_concrete_structures.formula_12_4 import (
    Form12Dot4PlainConcreteShearStressComparison,
)
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form12Dot5And6PlainConcreteBendingResistance(Formula):
    r"""Class representing formula 12.5 and 12.6 for the calculation of the design bending resistance of plain concrete,
    :math:`f_{cvd}`.

    EN 1992-1-1:2004 art.12.6.1 - Formula (12.5)
    """

    label = "12.5/12.6"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_ctd_pl: MPA,
        sigma_cp: MPA | Form12Dot3PlainConcreteShearStress,
        sigma_c_lim: MPA,
    ) -> None:
        r"""[:math:`f_{cvd}`] Design bending resistance of plain concrete [:math=`MPa`].

        EN 1992-1-1:2004 art.12.6.1 - Formula (12.5)

        Parameters
        ----------
        f_ctd_pl : MPA
            [:math=`f_{ctd,pl}`] Design tensile strength of plain concrete [:math=`MPa`].
        sigma_cp : MPA | Form12Dot3PlainConcreteShearStress
            [:math=`\sigma_{cp}`] Compressive stress [:math=`MPa`] or an instance of Form12Dot3PlainConcreteShearStress.
        sigma_c_lim : MPA
            [:math=`\sigma_{c,lim}`] Limiting compressive stress [:math=`MPa`].
        """
        super().__init__()
        self.f_ctd_pl = f_ctd_pl
        self.sigma_cp = sigma_cp
        self.sigma_c_lim = sigma_c_lim

    @staticmethod
    def _evaluate(f_ctd_pl: MPA, sigma_cp: MPA, sigma_c_lim: MPA) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(f_ctd_pl=f_ctd_pl, sigma_cp=sigma_cp)
        comparison = Form12Dot4PlainConcreteShearStressComparison(sigma_cp, sigma_c_lim)
        if comparison:
            return np.sqrt(f_ctd_pl**2 + sigma_cp * f_ctd_pl)
        return np.sqrt(f_ctd_pl**2 + sigma_cp * f_ctd_pl - ((sigma_cp - sigma_c_lim / 2) ** 2))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 12.5. / 12.6."""
        result = self._evaluate(self.f_ctd_pl, self.sigma_cp, self.sigma_c_lim)
        comparison = Form12Dot4PlainConcreteShearStressComparison(self.sigma_cp, self.sigma_c_lim)
        if comparison:
            equation = r"\sqrt{f_{ctd, pl} ^ 2 + \sigma_{cp} \cdot f_{ctd, pl}}"
            numeric_equation = rf"\sqrt{{{self.f_ctd_pl:.{n}f} ^ 2 + {self.sigma_cp:.{n}f} \cdot {self.f_ctd_pl:.{n}f}}}"
        else:
            equation = r"\sqrt{f_{ctd, pl} ^ 2 + \sigma_{cp} \cdot f_{ctd, pl} - \left(\frac{\sigma_{cp} - \sigma_{c, lim}}{2}\right) ^ 2}"
            part1 = f"{self.f_ctd_pl:.{n}f} ^ 2"
            part2 = rf"{self.sigma_cp:.{n}f} \cdot {self.f_ctd_pl:.{n}f}"
            part3 = f"\\left(\\frac{{{self.sigma_cp:.{n}f} - {self.sigma_c_lim:.{n}f}}}{2}\\right) ^ 2"
            numeric_equation = rf"\sqrt{{{part1} + {part2} - {part3}}}"
        return LatexFormula(
            return_symbol=r"f_{cvd}",
            result=f"{result:.{n}f}",
            equation=equation,
            numeric_equation=numeric_equation,
            comparison_operator_label="=",
        )
