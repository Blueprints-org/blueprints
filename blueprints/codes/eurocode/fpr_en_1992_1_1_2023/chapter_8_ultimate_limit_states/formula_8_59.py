"""Formula 8.59 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot59ShearStressResistanceInclinedShearReinforcement(Formula):
    """Class representing formula 8.59 for the calculation of the shear stress resistance in case of yielding of
    inclined shear reinforcement.

    This replaces Formula (8.42) for members with inclined shear reinforcement.
    """

    label = "8.59"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, rho_w: DIMENSIONLESS, f_ywd: MPA, cot_theta: DIMENSIONLESS, alpha_w: DEG) -> None:
        r"""[$\tau_{Rd,sy}$] Shear stress resistance perpendicular to the longitudinal member axis in case of
        yielding of the inclined shear reinforcement [$MPa$].

        FprEN 1992-1-1:2023 (E) art 8.2.3 (13) - Formula (8.59)

        Parameters
        ----------
        rho_w : DIMENSIONLESS
            [$\rho_w$] Shear reinforcement ratio according to Formula (8.43) [$-$].
        f_ywd : MPA
            [$f_{ywd}$] Design value of the yield strength of the shear reinforcement [$MPa$].
        cot_theta : DIMENSIONLESS
            [$\cot\theta$] Cotangent of the inclination of the compression field in the web, selected within the
            range of Formula (8.58), see Form8Dot58CheckCotangentInclinedShearReinforcement [$-$].
        alpha_w : DEG
            [$\alpha_w$] Inclination of the shear reinforcement, measured positive as shown in Figure 8.11 b).
            The standard gives this clause for [$45 \leq \alpha_w < 90$] degrees. Its cotangent and its sine both
            appear in the formula, so it is taken as the angle itself rather than as a pair of values that could
            contradict each other. For spiral reinforcement it may be assumed as the average angle of both legs,
            provided that the difference of each leg inclination and the 90 degrees is not greater than 12
            degrees [$degrees$].
        """
        super().__init__()
        self.rho_w = rho_w
        self.f_ywd = f_ywd
        self.cot_theta = cot_theta
        self.alpha_w = alpha_w

    @staticmethod
    def _evaluate(rho_w: DIMENSIONLESS, f_ywd: MPA, cot_theta: DIMENSIONLESS, alpha_w: DEG) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(rho_w=rho_w, f_ywd=f_ywd, cot_theta=cot_theta)
        raise_if_less_or_equal_to_zero(alpha_w=alpha_w)

        alpha_w_rad = np.deg2rad(alpha_w)
        return rho_w * f_ywd * (cot_theta + 1 / np.tan(alpha_w_rad)) * np.sin(alpha_w_rad)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.59."""
        _equation: str = r"\rho_w \cdot f_{ywd} \cdot \left(\cot(\theta) + \cot(\alpha_w)\right) \cdot \sin(\alpha_w)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
                r"\cot(\theta)": f"{self.cot_theta:.{n}f}",
                r"\alpha_w": f"{self.alpha_w:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\rho_w": f"{self.rho_w:.{n}f}",
                r"f_{ywd}": rf"{self.f_ywd:.{n}f} \ MPa",
                r"\cot(\theta)": f"{self.cot_theta:.{n}f}",
                r"\alpha_w": rf"{self.alpha_w:.{n}f} \ degrees",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Rd,sy}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
