"""Formula 6.21 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.math_helpers import cot
from blueprints.type_alias import DEG, MM, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot21CheckTransverseReinforcement(Formula):
    r"""Class representing formula 6.21 for checking transverse reinforcement per unit length."""

    label = "6.21"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        a_sf: MM2,
        f_yd: MPA,
        s_f: MM,
        v_ed: MPA,
        h_f: MM,
        theta_f: DEG,
    ) -> None:
        r"""Check the transverse reinforcement per unit length.

        NEN-EN 1992-1-1+C2:2011 art.6.2.4(4) - Formula (6.21)

        Parameters
        ----------
        a_sf : MM2
            [$A_{sf}$] Area of transverse reinforcement per unit length [$mm^2$].
        f_yd : MPA
            [$f_{yd}$] Design yield strength of reinforcement [$MPa$].
        s_f : MM
            [$s_{f}$] Spacing of transverse reinforcement [$mm$].
        v_ed : MPA
            [$v_{Ed}$] Design shear stress [$MPa$].
        h_f : MM
            [$h_{f}$] Thickness of flange at the junctions [$mm$].
        theta_f : DEG
            [$\theta_{f}$] Angle of the compression strut [$degrees$].
        """
        super().__init__()
        self.a_sf = a_sf
        self.f_yd = f_yd
        self.s_f = s_f
        self.v_ed = v_ed
        self.h_f = h_f
        self.theta_f = theta_f

    @staticmethod
    def _evaluate(
        a_sf: MM2,
        f_yd: MPA,
        s_f: MM,
        v_ed: MPA,
        h_f: MM,
        theta_f: DEG,
    ) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_sf=a_sf, f_yd=f_yd, v_ed=v_ed, h_f=h_f, theta_f=theta_f)
        denominator_rhs = cot(theta_f)
        raise_if_less_or_equal_to_zero(s_f=s_f, denominator_rhs=denominator_rhs)

        return (a_sf * f_yd / s_f) >= (v_ed * h_f / cot(theta_f))

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.21."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\left( \frac{A_{sf} \cdot f_{yd}}{s_{f}} \geq \frac{v_{Ed} \cdot h_{f}}{\cot(\theta_{f})} \right)",
            numeric_equation=rf"\left( \frac{{{self.a_sf:.3f} \cdot {self.f_yd:.3f}}}{{{self.s_f:.3f}}} \geq \frac{{{self.v_ed:.3f} "
            rf"\cdot {self.h_f:.3f}}}{{\cot({self.theta_f:.3f})}} \right)",
            comparison_operator_label="\\to",
            unit="",
        )
