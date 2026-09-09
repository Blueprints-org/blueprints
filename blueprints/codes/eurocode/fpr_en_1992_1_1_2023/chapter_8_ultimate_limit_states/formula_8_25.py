"""Formula 8.25 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, MM, N_MM
from blueprints.validations import raise_if_greater_than_90, raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot25EffectiveDepthFromPrincipalShearForce(Formula):
    """Class representing formula 8.25 for the calculation of the effective depth of planar members,
    as an alternative to formulas 8.22, 8.23 and 8.24.
    """

    label = "8.25"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        d_x: MM,
        d_y: MM,
        alpha_v: DEG | None = None,
        v_ed_x: N_MM | None = None,
        v_ed_y: N_MM | None = None,
    ) -> None:
        r"""[$d$] Effective depth of planar members, taken from the direction of the principal shear force [$mm$].

        FprEN 1992-1-1:2023 (E) art 8.2.1 (5) - Formula (8.25)

        This is the alternative offered by the standard to Formulas (8.22), (8.23) and (8.24), not an
        equivalent of them.

        The angle can be supplied in either of the two ways the standard offers. Give [$\alpha_v$] directly, or
        give the two shear forces and let Formula (8.26) produce it. At least one of the two routes is
        required; an [$\alpha_v$] that is given directly always wins, since the standard prints Formula (8.26)
        as what the angle "may be taken as" and so leaves room for a directly determined direction of the
        principal shear force.

        Parameters
        ----------
        d_x : MM
            [$d_x$] Effective depth in the x direction [$mm$].
        d_y : MM
            [$d_y$] Effective depth in the y direction [$mm$].
        alpha_v : DEG, optional
            [$\alpha_v$] Angle between the principal shear force and the x-axis, which may be taken according
            to Formula (8.26), see Form8Dot26AngleBetweenPrincipalShearForceAndXAxis. Leave it out to have it
            computed from the two shear forces instead. It lies between 0 and 90 degrees, as Formula (8.26) can
            produce nothing else [$degrees$].
        v_ed_x : N_MM, optional
            [$v_{Ed,x}$] Out-of-plane design shear force per unit width perpendicular to the x direction. Used
            only when [$\alpha_v$] is left out, and taken as a magnitude [$N/mm$].
        v_ed_y : N_MM, optional
            [$v_{Ed,y}$] Out-of-plane design shear force per unit width perpendicular to the y direction. Used
            only when [$\alpha_v$] is left out, and taken as a magnitude [$N/mm$].
        """
        super().__init__()
        self.d_x = d_x
        self.d_y = d_y
        self.v_ed_x = v_ed_x
        self.v_ed_y = v_ed_y
        self.alpha_v = self._angle(alpha_v, v_ed_x, v_ed_y)

    @staticmethod
    def _angle(alpha_v: DEG | None, v_ed_x: N_MM | None, v_ed_y: N_MM | None) -> DEG:
        """Returns the angle, either as given or from Formula (8.26) on the magnitudes of the shear forces."""
        if alpha_v is not None:
            return alpha_v
        if v_ed_x is None or v_ed_y is None:
            raise ValueError("Either alpha_v, or both v_ed_x and v_ed_y, must be given so that Formula (8.26) can supply the angle.")

        raise_if_less_or_equal_to_zero(abs_v_ed_x=abs(v_ed_x))
        return float(np.rad2deg(np.arctan(abs(v_ed_y) / abs(v_ed_x))))

    @classmethod
    def _evaluate(
        cls,
        d_x: MM,
        d_y: MM,
        alpha_v: DEG | None = None,
        v_ed_x: N_MM | None = None,
        v_ed_y: N_MM | None = None,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        angle = cls._angle(alpha_v, v_ed_x, v_ed_y)
        raise_if_negative(d_x=d_x, d_y=d_y, alpha_v=angle)
        raise_if_greater_than_90(alpha_v=angle)

        alpha_v_rad = np.deg2rad(angle)
        return d_x * np.cos(alpha_v_rad) ** 2 + d_y * np.sin(alpha_v_rad) ** 2

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.25."""
        _equation: str = r"d_x \cdot \cos^2(\alpha_v) + d_y \cdot \sin^2(\alpha_v)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_x": f"{self.d_x:.{n}f}",
                r"d_y": f"{self.d_y:.{n}f}",
                r"\alpha_v": f"{self.alpha_v:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_x": rf"{self.d_x:.{n}f} \ mm",
                r"d_y": rf"{self.d_y:.{n}f} \ mm",
                r"\alpha_v": rf"{self.alpha_v:.{n}f} \ degrees",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"d",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )
