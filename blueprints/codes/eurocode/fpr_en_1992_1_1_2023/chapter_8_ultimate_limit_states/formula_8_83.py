"""Formula 8.83 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, MM, MM2, MPA
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot83TorsionalStressResistanceLongitudinalReinforcement(Formula):
    r"""Class representing formula 8.83 for the torsional capacity when governed by yielding of the longitudinal
    reinforcement.

    It is one of the three resistances that Formula (8.81) takes the minimum of, together with Formulas (8.82)
    and (8.84). It applies to a single cell, thin-walled section or a sub-section with constant effective wall
    thickness.

    The standard prints the numerator as the single quantity [$\Sigma A_{sl} f_{yd}$], the yield force of the
    longitudinal reinforcement. This class takes the area and the stress separately, which mirrors Formula
    (8.82) and lets the unit representation expose a mismatch. The two are equal only when every bar counted
    carries the same [$f_{yd}$]; for mixed steel grades, pass the area that gives the correct yield force.
    """

    label = "8.83"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        sum_a_sl: MM2,
        f_yd: MPA,
        t_eff: MM,
        u_k: MM,
        theta: DEG,
    ) -> None:
        r"""[$\tau_{t,Rd,sl}$] Torsional capacity when governed by yielding of the longitudinal reinforcement
        [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.3.4(2) - Formula (8.83)

        Parameters
        ----------
        sum_a_sl : MM2
            [$\Sigma A_{sl}$] Sum of the areas of the longitudinal reinforcement that may be included in the
            calculation of the torsional capacity. The amount of longitudinal reinforcement considered in Formula
            (8.83) should have a resultant tensile force that acts at the centroid of the equivalent thin-walled
            closed cross-section. The reinforcement should generally be distributed according to 12.3.3(9)
            [$mm^2$].
        f_yd : MPA
            [$f_{yd}$] Design yield stress of the longitudinal reinforcement [$A_{sl}$] [$MPa$].
        t_eff : MM
            [$t_{eff}$] Constant effective wall thickness of the single cell, thin-walled section or sub-section,
            refer to 8.3.4(1) and to the definition of [$t_{eff,i}$] in 8.3.2(2) [$mm$].
        u_k : MM
            [$u_k$] Perimeter of the area [$A_k$] [$mm$].
        theta : DEG
            [$\theta$] Angle of compression field with respect to the longitudinal axis. It sits in the
            denominator through [$\cot\theta$], so the result grows without bound as the angle approaches 90
            degrees. Formula (8.85) keeps it well away from there, but needs [$\cot\theta_{min}$] of 8.2.3(4)
            and is therefore not enforced here [$degrees$].
        """
        super().__init__()
        self.sum_a_sl = sum_a_sl
        self.f_yd = f_yd
        self.t_eff = t_eff
        self.u_k = u_k
        self.theta = theta

    @staticmethod
    def _evaluate(
        sum_a_sl: MM2,
        f_yd: MPA,
        t_eff: MM,
        u_k: MM,
        theta: DEG,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sum_a_sl=sum_a_sl, f_yd=f_yd)
        raise_if_less_or_equal_to_zero(t_eff=t_eff, u_k=u_k, theta=theta)

        return sum_a_sl * f_yd / (t_eff * u_k * cot(theta))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.83."""
        _equation: str = r"\frac{\Sigma A_{sl} \cdot f_{yd}}{t_{eff} \cdot u_k \cdot \cot(\theta)}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\Sigma A_{sl}": f"{self.sum_a_sl:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
                r"t_{eff}": f"{self.t_eff:.{n}f}",
                r"u_k": f"{self.u_k:.{n}f}",
                r"\theta": f"{self.theta:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\Sigma A_{sl}": rf"{self.sum_a_sl:.{n}f} \ mm^2",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
                r"t_{eff}": rf"{self.t_eff:.{n}f} \ mm",
                r"u_k": rf"{self.u_k:.{n}f} \ mm",
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\tau_{t,Rd,sl}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
