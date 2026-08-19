"""Formula 8.66 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MM2, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot66CheckOmissionOfShearVerification(ComparisonFormula):
    r"""Class representing formula 8.66 for the check that determines whether the verification of the shear
    between web and flanges may be omitted.

    A satisfied check does not mean the connection has been verified. It means the standard permits the
    verification to be skipped and requires no extra reinforcement above that for transverse bending. A check
    that is not satisfied does not mean the connection fails either; it means 8.2.5(3) and (4) have to be
    worked through, starting from Formula (8.69).
    """

    label = "8.66"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, tau_ed: MPA, a_st_min: MM2, s_f: MM, h_f: MM, f_yd: MPA) -> None:
        r"""Check whether further verification of the shear between web and flanges may be omitted.

        FprEN 1992-1-1:2023 (E) art 8.2.5 (2) - Formula (8.66)

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Longitudinal shear stress at the junction between one side of a flange and the web
            according to Formula (8.65), see Form8Dot65LongitudinalShearStressFlangeWebJunction [$MPa$].
        a_st_min : MM2
            [$A_{st,min}$] Minimum transverse reinforcement according to Table 12.1 (NDP) [$mm^2$].
        s_f : MM
            [$s_f$] Spacing of the transverse reinforcement in the flange. The standard does not define it in
            words; it appears only as a dimension in Figure 8.13, between the transverse bars along
            [$\Delta x$] [$mm$].
        h_f : MM
            [$h_f$] Thickness of the flange at the junctions [$mm$].
        f_yd : MPA
            [$f_{yd}$] Design value of the yield strength of the transverse reinforcement [$MPa$].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.a_st_min = a_st_min
        self.s_f = s_f
        self.h_f = h_f
        self.f_yd = f_yd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(tau_ed: MPA, *_args, **_kwargs) -> float:
        """Evaluates the longitudinal shear stress, for more information see the __init__ method."""
        raise_if_negative(tau_ed=tau_ed)

        return float(tau_ed)

    @staticmethod
    def _evaluate_rhs(a_st_min: MM2, s_f: MM, h_f: MM, f_yd: MPA, *_args, **_kwargs) -> float:
        """Evaluates the stress that the minimum transverse reinforcement already carries."""
        raise_if_negative(a_st_min=a_st_min, f_yd=f_yd)
        raise_if_less_or_equal_to_zero(s_f=s_f, h_f=h_f)

        return float(a_st_min / (s_f * h_f) * f_yd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.66."""
        _equation: str = r"\tau_{Ed} \leq \frac{A_{st,min}}{s_f \cdot h_f} \cdot f_{yd}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"A_{st,min}": f"{self.a_st_min:.{n}f}",
                r"s_f": f"{self.s_f:.{n}f}",
                r"h_f": f"{self.h_f:.{n}f}",
                r"f_{yd}": f"{self.f_yd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
                r"A_{st,min}": rf"{self.a_st_min:.{n}f} \ mm^2",
                r"s_f": rf"{self.s_f:.{n}f} \ mm",
                r"h_f": rf"{self.h_f:.{n}f} \ mm",
                r"f_{yd}": rf"{self.f_yd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
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
