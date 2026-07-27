"""Formula 8.38, 8.39 and 8.40 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, N_MM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot38To40ReinforcementRatioPlanarMembers(Formula):
    """Class representing formulas 8.38, 8.39 and 8.40 for the calculation of the reinforcement ratio of planar members
    with different reinforcement ratios in both directions, taken as a function of the ratio of the shear forces.
    """

    label = "8.38/8.39/8.40"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, v_ed_x: N_MM, v_ed_y: N_MM, rho_l_x: DIMENSIONLESS, rho_l_y: DIMENSIONLESS, alpha_v: DEG) -> None:
        r"""[$\rho_l$] Reinforcement ratio of planar members, as a function of the ratio of the shear forces
        [$v_{Ed,y}/v_{Ed,x}$] [$-$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (7) - Formula (8.38), (8.39) and (8.40)

        The boundaries of the ratio are one-sided as printed: a ratio of exactly 0.5 falls under Formula (8.38)
        and a ratio of exactly 2 falls under Formula (8.40). The standard gives no rule for [$v_{Ed,x} = 0$],
        for which the ratio is undefined, so that input is rejected. Both shear forces are taken as magnitudes,
        since a negative ratio would fall under Formula (8.38) without the standard intending it.

        Parameters
        ----------
        v_ed_x : N_MM
            [$v_{Ed,x}$] Out-of-plane design shear force per unit width acting on the cross-section perpendicular
            to the x direction [$N/mm$].
        v_ed_y : N_MM
            [$v_{Ed,y}$] Out-of-plane design shear force per unit width acting on the cross-section perpendicular
            to the y direction [$N/mm$].
        rho_l_x : DIMENSIONLESS
            [$\rho_{l,x}$] Reinforcement ratio in the x direction [$-$].
        rho_l_y : DIMENSIONLESS
            [$\rho_{l,y}$] Reinforcement ratio in the y direction [$-$].
        alpha_v : DEG
            [$\alpha_v$] Angle between the principal shear force and the x-axis as defined in 8.2.1(5), which may be
            taken according to Formula (8.26), see Form8Dot26AngleBetweenPrincipalShearForceAndXAxis. It is only used
            by Formula (8.39), and it is the caller's responsibility to keep it consistent with the shear forces
            passed here [$degrees$].
        """
        super().__init__()
        self.v_ed_x = v_ed_x
        self.v_ed_y = v_ed_y
        self.rho_l_x = rho_l_x
        self.rho_l_y = rho_l_y
        self.alpha_v = alpha_v

    @staticmethod
    def _evaluate(v_ed_x: N_MM, v_ed_y: N_MM, rho_l_x: DIMENSIONLESS, rho_l_y: DIMENSIONLESS, alpha_v: DEG) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(v_ed_y=v_ed_y, rho_l_x=rho_l_x, rho_l_y=rho_l_y, alpha_v=alpha_v)
        raise_if_less_or_equal_to_zero(v_ed_x=v_ed_x)

        ratio = v_ed_y / v_ed_x
        if ratio <= 0.5:
            return rho_l_x
        if ratio < 2:
            alpha_v_rad = np.deg2rad(alpha_v)
            return rho_l_x * np.cos(alpha_v_rad) ** 4 + rho_l_y * np.sin(alpha_v_rad) ** 4
        return rho_l_y

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 8.38, 8.39 and 8.40."""
        _equation: str = (
            r"\begin{cases} \rho_{l,x} & \text{if } \frac{v_{Ed,y}}{v_{Ed,x}} \leq 0.5 \\ "
            r"\rho_{l,x} \cdot \cos^4(\alpha_v) + \rho_{l,y} \cdot \sin^4(\alpha_v) "
            r"& \text{if } 0.5 < \frac{v_{Ed,y}}{v_{Ed,x}} < 2 \\ "
            r"\rho_{l,y} & \text{if } \frac{v_{Ed,y}}{v_{Ed,x}} \geq 2 \end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"v_{Ed,x}": f"{self.v_ed_x:.{n}f}",
                r"v_{Ed,y}": f"{self.v_ed_y:.{n}f}",
                r"\rho_{l,x}": f"{self.rho_l_x:.{n}f}",
                r"\rho_{l,y}": f"{self.rho_l_y:.{n}f}",
                r"\alpha_v": f"{self.alpha_v:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"v_{Ed,x}": rf"{self.v_ed_x:.{n}f} \ N/mm",
                r"v_{Ed,y}": rf"{self.v_ed_y:.{n}f} \ N/mm",
                r"\rho_{l,x}": f"{self.rho_l_x:.{n}f}",
                r"\rho_{l,y}": f"{self.rho_l_y:.{n}f}",
                r"\alpha_v": rf"{self.alpha_v:.{n}f} \ degrees",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\rho_l",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
