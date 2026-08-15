"""Formula 8.38, 8.39 and 8.40 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, N_MM
from blueprints.validations import raise_if_greater_than_90, raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot38To40ReinforcementRatioPlanarMembers(Formula):
    """Class representing formulas 8.38, 8.39 and 8.40 for the calculation of the reinforcement ratio of planar members
    with different reinforcement ratios in both directions, taken as a function of the ratio of the shear forces.
    """

    label = "8.38/8.39/8.40"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        v_ed_x: N_MM,
        v_ed_y: N_MM,
        rho_l_x: DIMENSIONLESS,
        rho_l_y: DIMENSIONLESS,
        alpha_v: DEG | None = None,
    ) -> None:
        r"""[$\rho_l$] Reinforcement ratio of planar members, as a function of the ratio of the shear forces
        [$v_{Ed,y}/v_{Ed,x}$] [$-$].

        FprEN 1992-1-1:2023 (E) art 8.2.2 (7) - Formula (8.38), (8.39) and (8.40)

        The boundaries of the ratio are one-sided as printed: a ratio of exactly 0.5 falls under Formula (8.38)
        and a ratio of exactly 2 falls under Formula (8.40). The standard gives no rule for [$v_{Ed,x} = 0$],
        for which the ratio is undefined, so that input is rejected.

        Both shear forces are taken as magnitudes. They are components of a shear force vector and the standard
        places no restriction on their sign, but the printed boundaries only order a ratio of magnitudes: a
        signed ratio turns negative as soon as one component does, and every negative value would fall under
        Formula (8.38) regardless of which direction carries the shear. This matches Formulas (8.22) to (8.24),
        which the standard writes with the same ratio and the same two boundaries.

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
        alpha_v : DEG, optional
            [$\alpha_v$] Angle between the principal shear force and the x-axis, which the standard defines in
            8.2.1(5). When it is left out it is computed from the two shear forces with Formula (8.26),
            [$\arctan\left(\left|v_{Ed,y}\right| / \left|v_{Ed,x}\right|\right)$], the value that clause allows
            it to be taken as and the only one consistent with the forces passed here. That clause prints
            Formula (8.26) as what the angle "may be taken as", so a directly determined direction of the
            principal shear force is admissible as well and can be passed here instead; it is then the caller's
            responsibility to keep it consistent with the two forces. The angle only reaches Formula (8.39). It
            lies between 0 and 90 degrees, as Formula (8.26) can produce nothing else [$degrees$].
        """
        super().__init__()
        self.v_ed_x = v_ed_x
        self.v_ed_y = v_ed_y
        self.rho_l_x = rho_l_x
        self.rho_l_y = rho_l_y
        self.alpha_v = self._angle(v_ed_x, v_ed_y) if alpha_v is None else alpha_v

    @staticmethod
    def _angle(v_ed_x: N_MM, v_ed_y: N_MM) -> DEG:
        """The angle of Formula (8.26), taken on the magnitudes of the two shear forces."""
        raise_if_less_or_equal_to_zero(abs_v_ed_x=abs(v_ed_x))

        return float(np.rad2deg(np.arctan(abs(v_ed_y) / abs(v_ed_x))))

    @classmethod
    def _evaluate(
        cls,
        v_ed_x: N_MM,
        v_ed_y: N_MM,
        rho_l_x: DIMENSIONLESS,
        rho_l_y: DIMENSIONLESS,
        alpha_v: DEG | None = None,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(rho_l_x=rho_l_x, rho_l_y=rho_l_y)
        raise_if_less_or_equal_to_zero(abs_v_ed_x=abs(v_ed_x))

        angle = cls._angle(v_ed_x, v_ed_y) if alpha_v is None else alpha_v
        raise_if_negative(alpha_v=angle)
        raise_if_greater_than_90(alpha_v=angle)

        ratio = abs(v_ed_y) / abs(v_ed_x)
        if ratio <= 0.5:
            return rho_l_x
        if ratio < 2:
            alpha_v_rad = np.deg2rad(angle)
            return rho_l_x * np.cos(alpha_v_rad) ** 4 + rho_l_y * np.sin(alpha_v_rad) ** 4
        return rho_l_y

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 8.38, 8.39 and 8.40."""
        _equation: str = (
            r"\begin{cases} \rho_{l,x} & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \leq 0.5 \\ "
            r"\rho_{l,x} \cdot \cos^4(\alpha_v) + \rho_{l,y} \cdot \sin^4(\alpha_v) "
            r"& \text{if } 0.5 < \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} < 2 \\ "
            r"\rho_{l,y} & \text{if } \frac{\left|v_{Ed,y}\right|}{\left|v_{Ed,x}\right|} \geq 2 \end{cases}"
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
