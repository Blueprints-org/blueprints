"""Formula 8.60 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DEG, DIMENSIONLESS, MPA
from blueprints.utils.math_helpers import cot
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot60CheckCompressionFieldStressInclinedShearReinforcement(ComparisonFormula):
    r"""Class representing formula 8.60 for the verification of the stress in the compression field of members
    with inclined shear reinforcement.

    This replaces Formula (8.44) for such members, and it carries the character of that formula: 8.2.3(5)
    introduces (8.44) with "The stress in the compression field in all cross-sections shall be verified
    according to", so the relation is a verification that passes or fails and not a value to be clamped.
    The stress itself remains available as [$lhs$], and [$unity\_check$] gives the ratio to its limit.
    """

    label = "8.60"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, tau_ed: MPA, theta: DEG, alpha_w: DEG, nu: DIMENSIONLESS, f_cd: MPA) -> None:
        r"""Verify the stress in the compression field against its limit.

        FprEN 1992-1-1:2023 (E) art 8.2.3 (13) - Formula (8.60)

        Parameters
        ----------
        tau_ed : MPA
            [$\tau_{Ed}$] Average shear stress over the cross-section according to Formula (8.18) [$MPa$].
        theta : DEG
            [$\theta$] Inclination of the compression field in the web, selected within the range of Formula
            (8.58), see Form8Dot58CheckCotangentInclinedShearReinforcement [$degrees$].
        alpha_w : DEG
            [$\alpha_w$] Inclination of the shear reinforcement, measured positive as shown in Figure 8.11 b).
            The standard gives this clause for [$45 \leq \alpha_w < 90$] degrees, which is a condition of
            application and is not enforced. Angles above 90 degrees are rejected, since the standard says they
            should be avoided [$degrees$].
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor for concrete cracked in shear. A value of 0,5 may be adopted when
            using the angles of the compression field given in 8.2.3(4), see 8.2.3(6) [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.tau_ed = tau_ed
        self.theta = theta
        self.alpha_w = alpha_w
        self.nu = nu
        self.f_cd = f_cd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        return operator.le

    @staticmethod
    def _evaluate_lhs(tau_ed: MPA, theta: DEG, alpha_w: DEG, *_args, **_kwargs) -> float:
        """Evaluates the stress in the compression field, for more information see the __init__ method."""
        raise_if_negative(tau_ed=tau_ed)
        raise_if_less_or_equal_to_zero(theta=theta, alpha_w=alpha_w)

        cot_theta = cot(theta)

        # Cast away the numpy type: ComparisonFormula.__bool__ returns the result of the unity check, and
        # Python rejects a numpy.bool there.
        return float(tau_ed * (1 + cot_theta**2) / (cot_theta + cot(alpha_w)))

    @staticmethod
    def _evaluate_rhs(nu: DIMENSIONLESS, f_cd: MPA, *_args, **_kwargs) -> float:
        """Evaluates the limit on the stress, for more information see the __init__ method."""
        # Not merely non-negative: the limit is the denominator of the unity check, and a zero strength or a
        # zero reduction factor would make that ratio undefined rather than simply failing the check.
        raise_if_less_or_equal_to_zero(nu=nu, f_cd=f_cd)

        return float(nu * f_cd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.60."""
        _equation: str = (
            r"\sigma_{cd} = \tau_{Ed} \cdot \frac{1 + \left(\cot(\theta)\right)^2}"
            r"{\cot(\theta) + \cot(\alpha_w)} \leq \nu \cdot f_{cd}"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\sigma_{cd}": f"{self.lhs:.{n}f}",
                r"\tau_{Ed}": f"{self.tau_ed:.{n}f}",
                r"\theta": f"{self.theta:.{n}f}",
                r"\alpha_w": f"{self.alpha_w:.{n}f}",
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\sigma_{cd}": rf"{self.lhs:.{n}f} \ MPa",
                r"\tau_{Ed}": rf"{self.tau_ed:.{n}f} \ MPa",
                r"\theta": rf"{self.theta:.{n}f} ^\circ",
                r"\alpha_w": rf"{self.alpha_w:.{n}f} ^\circ",
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
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
