"""Formula 8.70 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot70CheckCrushingOfCompressionFieldInFlange(ComparisonFormula):
    r"""Class representing formula 8.70 for the check that prevents crushing of the compression field in the flange.

    The standard writes the compressive stress [$\sigma_{cd}$] and the condition it has to satisfy on one line.
    The line is a verification and not a value with a cap on it, since the paragraph introduces it with "the
    following condition should be satisfied", so it is implemented as a comparison. The stress itself remains
    available through the ``lhs`` property.
    """

    label = "8.70"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        tau_ed: MPA,
        cot_theta_f: DIMENSIONLESS,
        nu: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        r"""Check whether the compression field in the flange is safe from crushing.

        FprEN 1992-1-1:2023 (E) art. 8.2.5(4) - Formula (8.70)

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Longitudinal shear stress at the junction between one side of a flange and the web
            according to Formula (8.65) [$MPa$].
        cot_theta_f : DIMENSIONLESS
            [$\cot\theta_f$] Cotangent of the selected inclination of the compression field in the flange with
            respect to the longitudinal axis, bounded by Formulas (8.67) and (8.68). The printed formula also
            contains [$\tan\theta_f$], which is taken as its reciprocal [$-$].
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor, for which 0,5 may be used according to Formula (8.71) [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.cot_theta_f = cot_theta_f
        self.nu = nu
        self.f_cd = f_cd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(tau_ed: MPA, cot_theta_f: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates the compressive stress in the compression field, for more information see the __init__ method."""
        raise_if_negative(tau_ed=tau_ed)
        # The cotangent is the denominator of the tangent in the printed formula, so it cannot be zero. A
        # cotangent of zero or less is not the inclination of a compression field either.
        raise_if_less_or_equal_to_zero(cot_theta_f=cot_theta_f)

        return float(tau_ed * (cot_theta_f + 1 / cot_theta_f))

    @staticmethod
    def _evaluate_rhs(nu: DIMENSIONLESS, f_cd: MPA, *_args, **_kwargs) -> float:
        """Evaluates the compressive strength of the compression field, for more information see the __init__ method."""
        raise_if_negative(nu=nu, f_cd=f_cd)

        return float(nu * f_cd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.70."""
        _equation: str = r"\sigma_{cd} = \tau_{Ed} \left(\cot(\theta_f) + \tan(\theta_f)\right) \leq \nu \cdot f_{cd}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\sigma_{cd}": f"{self.lhs:.{n}f}",
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"\cot(\theta_f)": f"{self.cot_theta_f:.{n}f}",
                r"\tan(\theta_f)": f"{1 / self.cot_theta_f:.{n}f}",
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\sigma_{cd}": rf"{self.lhs:.{n}f} \ MPa",
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
                # The cotangent, the tangent and the strength reduction factor are dimensionless.
                r"\cot(\theta_f)": f"{self.cot_theta_f:.{n}f}",
                r"\tan(\theta_f)": f"{1 / self.cot_theta_f:.{n}f}",
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
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
