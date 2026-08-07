"""Formula 8.69 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot69CheckTransverseReinforcementInFlange(ComparisonFormula):
    r"""Class representing formula 8.69 for the check of the transverse reinforcement in the flange.

    The standard phrases this paragraph as a way to determine [$A_{sf}$], but it prints a relation that the
    longitudinal shear stress has to satisfy, so it is implemented as the check of a chosen reinforcement
    rather than as a formula returning an area.
    """

    label = "8.69"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        tau_ed: MPA,
        a_sf: MM2,
        s_f: MM,
        h_f: MM,
        f_yd: MPA,
        cot_theta_f: DIMENSIONLESS,
    ) -> None:
        r"""Check whether the transverse reinforcement in the flange carries the longitudinal shear stress.

        FprEN 1992-1-1:2023 (E) art. 8.2.5(4) - Formula (8.69)

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Longitudinal shear stress at the junction between one side of a flange and the web
            according to Formula (8.65) [$MPa$].
        a_sf : MM2
            [$A_{sf}$] Area of the transverse reinforcement in the flange. The standard does not define it in
            words; it appears as a reinforcement area in Figure 8.13, placed at a spacing [$s_f$] [$mm^2$].
        s_f : MM
            [$s_f$] Spacing of the transverse reinforcement in the flange. The standard does not define it in
            words; it appears only as a dimension in Figure 8.13, between the transverse bars along
            [$\Delta x$] [$mm$].
        h_f : MM
            [$h_f$] Thickness of the flange at the junctions [$mm$].
        f_yd : MPA
            [$f_{yd}$] Design value of the yield strength of the transverse reinforcement [$MPa$].
        cot_theta_f : DIMENSIONLESS
            [$\cot\theta_f$] Cotangent of the selected inclination of the compression field in the flange with
            respect to the longitudinal axis, bounded by Formulas (8.67) and (8.68) [$-$].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.a_sf = a_sf
        self.s_f = s_f
        self.h_f = h_f
        self.f_yd = f_yd
        self.cot_theta_f = cot_theta_f

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(tau_ed: MPA, *_args, **_kwargs) -> float:
        """Evaluates the longitudinal shear stress, for more information see the __init__ method."""
        raise_if_negative(tau_ed=tau_ed)

        return float(tau_ed)

    @staticmethod
    def _evaluate_rhs(a_sf: MM2, s_f: MM, h_f: MM, f_yd: MPA, cot_theta_f: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the shear stress that the transverse reinforcement in the flange can carry."""
        raise_if_negative(a_sf=a_sf, f_yd=f_yd, cot_theta_f=cot_theta_f)
        raise_if_less_or_equal_to_zero(s_f=s_f, h_f=h_f)

        return float(a_sf / (s_f * h_f) * f_yd * cot_theta_f)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.69."""
        _equation: str = r"\tau_{Ed} \leq \frac{A_{sf}}{s_f \cdot h_f} \cdot f_{yd} \cdot \cot(\theta_f)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"A_{sf}": f"{self.a_sf:.{n}f}",
                r"s_f": f"{self.s_f:.{n}f}",
                r"h_f": f"{self.h_f:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
                r"\cot(\theta_f)": f"{self.cot_theta_f:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
                r"A_{sf}": rf"{self.a_sf:.{n}f} \ mm^2",
                r"s_f": rf"{self.s_f:.{n}f} \ mm",
                r"h_f": rf"{self.h_f:.{n}f} \ mm",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
                # The cotangent is dimensionless, so it carries no unit here.
                r"\cot(\theta_f)": f"{self.cot_theta_f:.{n}f}",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else r"\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"\to",
            unit="",
        )
