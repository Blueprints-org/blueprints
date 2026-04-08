"""Formula 8.44 from prEN-1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.pr_en_1992_1_1_2023 import PR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot44StressCompressionField(Formula):
    r"""Class representing formula 8.44 for the verification of the compression field stress.

    The stress in the compression field in all cross-sections shall be verified according to:
    [$\sigma_{cd} = \tau_{Ed}(\cot \theta + \tan \theta) \leq \nu \cdot f_{cd}$]
    """

    label = "8.44"
    source_document = PR_EN_1992_1_1_2023

    def __init__(
        self,
        tau_ed: MPA,
        cot_theta: DIMENSIONLESS,
        tan_theta: DIMENSIONLESS,
        nu: DIMENSIONLESS,
        f_cd: MPA,
    ) -> None:
        r"""Verification of the compression field stress.

        prEN 1992-1-1:2023 art. 8.2.3 - Formula (8.44)

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Design value of the shear stress [$MPa$].
        cot_theta : DIMENSIONLESS
            [$\cot \theta$] Cotangent of the inclination angle of the compression strut (dimensionless).
        tan_theta : DIMENSIONLESS
            [$\tan \theta$] Tangent of the inclination angle of the compression strut (dimensionless).
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor for concrete cracked in shear (dimensionless).
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.cot_theta = cot_theta
        self.tan_theta = tan_theta
        self.nu = nu
        self.f_cd = f_cd

    @staticmethod
    def _evaluate_pt1(tau_ed: MPA, cot_theta: DIMENSIONLESS, tan_theta: DIMENSIONLESS, *_args, **_kwargs) -> float:
        """Evaluates part 1 of the formula, for more information see the __init__ method."""
        raise_if_negative(tau_ed=tau_ed, cot_theta=cot_theta, tan_theta=tan_theta)
        return tau_ed * (cot_theta + tan_theta)

    @staticmethod
    def _evaluate_pt2(nu: DIMENSIONLESS, f_cd: MPA, *_args, **_kwargs) -> float:
        """Evaluates part 2 of the formula, for more information see the __init__ method."""
        raise_if_negative(nu=nu, f_cd=f_cd)
        return nu * f_cd

    @staticmethod
    def _evaluate(tau_ed: MPA, cot_theta: DIMENSIONLESS, tan_theta: DIMENSIONLESS, nu: DIMENSIONLESS, f_cd: MPA, *_args, **_kwargs) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        eval_pt1 = Form8Dot44StressCompressionField._evaluate_pt1(
            tau_ed=tau_ed,
            cot_theta=cot_theta,
            tan_theta=tan_theta,
        )
        eval_pt2 = Form8Dot44StressCompressionField._evaluate_pt2(nu=nu, f_cd=f_cd)
        return min(eval_pt1, eval_pt2)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 8.44."""
        _equation: str = r"\tau_{Ed} \cdot (\cot \theta + \tan \theta) \leq \nu \cdot f_{cd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"\cot \theta": f"{self.cot_theta:.{n}f}",
                r"\tan \theta": f"{self.tan_theta:.{n}f}",
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
                r"\cot \theta": rf"{self.cot_theta:.{n}f}",
                r"\tan \theta": rf"{self.tan_theta:.{n}f}",
                r"\nu": rf"{self.nu:.{n}f}",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
            },
            False,
        )
        intermediate_result = rf"{self._evaluate_pt1(tau_ed=self.tau_ed, cot_theta=self.cot_theta, tan_theta=self.tan_theta):.{n}f} \leq {
            self._evaluate_pt2(nu=self.nu, f_cd=self.f_cd):.{n}f}"
        return LatexFormula(
            return_symbol=r"\sigma_{Rd}",
            result=f"{self:.{n}f}",
            intermediate_result=intermediate_result,
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label=r"=",
            unit="MPa",
        )
