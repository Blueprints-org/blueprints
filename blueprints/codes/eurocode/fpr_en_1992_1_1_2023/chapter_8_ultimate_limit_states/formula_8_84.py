"""Formula 8.84 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import numpy as np

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, MPA
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot84TorsionalStressResistanceConcreteCrushing(Formula):
    r"""Class representing formula 8.84 for the torsional strength when governed by crushing of the compression
    field in concrete.

    It is one of the three resistances that Formula (8.81) takes the minimum of, together with Formulas (8.82)
    and (8.83). It applies to a single cell, thin-walled section or a sub-section with constant effective wall
    thickness.

    Unlike the other two, this one does not depend on the reinforcement, and 8.3.1(3) uses it to distribute the
    acting torsional moment over the sub-sections of a complex shape.
    """

    label = "8.84"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        nu: DIMENSIONLESS,
        f_cd: MPA,
        theta: DEG,
    ) -> None:
        r"""[$\tau_{t,Rd,max}$] Torsional strength when governed by crushing of the compression field in concrete
        [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.3.4(3) - Formula (8.84)

        Parameters
        ----------
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor for concrete cracked in shear. It may be determined by the formulae
            in Annex G. A value of [$\nu = 0,60$] may be used when [$\cot\theta = 1,0$]. Neither Annex G nor that
            pairing is enforced here, so the choice stays with the caller [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        theta : DEG
            [$\theta$] Angle of compression field with respect to the longitudinal axis. Its range is restricted
            by Formula (8.85), which needs [$\cot\theta_{min}$] of 8.2.3(4) and is therefore not enforced here
            [$degrees$].
        """
        super().__init__()
        self.nu = nu
        self.f_cd = f_cd
        self.theta = theta

    @staticmethod
    def _evaluate(
        nu: DIMENSIONLESS,
        f_cd: MPA,
        theta: DEG,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(nu=nu, f_cd=f_cd)
        raise_if_less_or_equal_to_zero(theta=theta)

        return nu * f_cd / (cot(theta) + np.tan(np.deg2rad(theta)))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.84."""
        _equation: str = r"\frac{\nu \cdot f_{cd}}{\cot(\theta) + \tan(\theta)}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
                r"\theta": f"{self.theta:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\tau_{t,Rd,max}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
