"""Formula 8.101 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot101FactorKN(Formula):
    r"""Class representing formula 8.101 for the calculation of the factor [$k_N$], used to account for axial
    forces and prestressing in the punching shear gradient enhancement coefficient of Formulas (8.99) and
    (8.100).
    """

    label = "8.101"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        b_0: MM,
        b_0_5: MM,
        sigma_d: MPA,
        f_ck: MPA,
    ) -> None:
        r"""[$k_N$] Factor accounting for axial forces and prestressing [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.4.3(4) - Formula (8.101)

        Parameters
        ----------
        b_0 : MM
            [$b_0$] Length of the perimeter at the face of the supporting area, see Formula (8.96) [$mm$].
        b_0_5 : MM
            [$b_{0,5}$] Length of the control perimeter, taken at a distance [$0,5 d_v$] from the face of the
            supporting area according to 8.4.2(2) to (5) [$mm$].
        sigma_d : MPA
            [$\sigma_d$] Average normal stress over the width [$b_s$] defined in Figure 8.22 [$MPa$].
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.b_0 = b_0
        self.b_0_5 = b_0_5
        self.sigma_d = sigma_d
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        b_0: MM,
        b_0_5: MM,
        sigma_d: MPA,
        f_ck: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(b_0=b_0)
        raise_if_less_or_equal_to_zero(b_0_5=b_0_5, f_ck=f_ck)
        control_perimeter_ratio_complement = 1 - b_0 / b_0_5
        raise_if_less_or_equal_to_zero(control_perimeter_ratio_complement=control_perimeter_ratio_complement)

        return np.sqrt(1 + (0.47 / control_perimeter_ratio_complement) * (abs(sigma_d) / np.sqrt(f_ck)))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.101."""
        _equation: str = r"\sqrt{1 + \frac{0.47}{1 - b_0/b_{0,5}} \cdot \frac{\left|\sigma_d\right|}{\sqrt{f_{ck}}}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_0/b_{0,5}": rf"{self.b_0:.{n}f}/{self.b_0_5:.{n}f}",
                r"\sigma_d": f"{self.sigma_d:.{n}f}",
                r"f_{ck}": f"{self.f_ck:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"b_0/b_{0,5}": rf"{self.b_0:.{n}f} \ mm/{self.b_0_5:.{n}f} \ mm",
                r"\sigma_d": rf"{self.sigma_d:.{n}f} \ MPa",
                r"f_{ck}": rf"{self.f_ck:.{n}f} \ MPa",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"k_N",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
