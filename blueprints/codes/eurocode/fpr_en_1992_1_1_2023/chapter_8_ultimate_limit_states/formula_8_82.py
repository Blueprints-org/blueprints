"""Formula 8.82 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, MM, MM2, MPA
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot82TorsionalStressResistanceShearReinforcement(Formula):
    r"""Class representing formula 8.82 for the torsional capacity when governed by yielding of the shear
    reinforcement.

    It is one of the three resistances that Formula (8.81) takes the minimum of, together with Formulas (8.83)
    and (8.84). It applies to a single cell, thin-walled section or a sub-section with constant effective wall
    thickness.

    The result is a shear stress, not a torsional moment. Formula (8.79) converts between the two.
    """

    label = "8.82"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        theta: DEG,
        a_sw: MM2,
        t_eff: MM,
        s: MM,
        f_ywd: MPA,
    ) -> None:
        r"""[$\tau_{t,Rd,sw}$] Torsional capacity when governed by yielding of the shear reinforcement [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.3.4(2) - Formula (8.82)

        Parameters
        ----------
        theta : DEG
            [$\theta$] Angle of compression field with respect to the longitudinal axis. Its range is restricted
            by Formula (8.85), which needs [$\cot\theta_{min}$] of 8.2.3(4) and is therefore not enforced here
            [$degrees$].
        a_sw : MM2
            [$A_{sw}$] Cross-sectional area of the shear reinforcement within the effective wall thickness in
            Figure 8.16 [$mm^2$].
        t_eff : MM
            [$t_{eff}$] Constant effective wall thickness of the single cell, thin-walled section or sub-section,
            refer to 8.3.4(1) and to the definition of [$t_{eff,i}$] in 8.3.2(2) [$mm$].
        s : MM
            [$s$] Spacing (in the longitudinal direction) between the shear reinforcement [$A_{sw}$] [$mm$].
        f_ywd : MPA
            [$f_{ywd}$] Design yield stress of the shear reinforcement [$MPa$].
        """
        super().__init__()
        self.theta = theta
        self.a_sw = a_sw
        self.t_eff = t_eff
        self.s = s
        self.f_ywd = f_ywd

    @staticmethod
    def _evaluate(
        theta: DEG,
        a_sw: MM2,
        t_eff: MM,
        s: MM,
        f_ywd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_sw=a_sw, f_ywd=f_ywd)
        raise_if_less_or_equal_to_zero(theta=theta, t_eff=t_eff, s=s)

        return cot(theta) * a_sw / (t_eff * s) * f_ywd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.82."""
        _equation: str = r"\cot(\theta) \cdot \frac{A_{sw}}{t_{eff} \cdot s} \cdot f_{ywd}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta": f"{self.theta:.{n}f}",
                r"A_{sw}": f"{self.a_sw:.{n}f}",
                r"t_{eff}": f"{self.t_eff:.{n}f}",
                r"\cdot s}": f"\\cdot {self.s:.{n}f}}}",
                r"f_{ywd}": f"{self.f_ywd:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
                r"A_{sw}": rf"{self.a_sw:.{n}f} \ mm^2",
                r"t_{eff}": rf"{self.t_eff:.{n}f} \ mm",
                r"\cdot s}": rf"\cdot {self.s:.{n}f} \ mm}}",
                r"f_{ywd}": rf"{self.f_ywd:.{n}f} \ MPa",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\tau_{t,Rd,sw}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
