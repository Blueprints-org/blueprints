"""Formula 8.114 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

import operator
from collections.abc import Callable

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import ComparisonFormula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot114CheckCompressiveStressInStrutOrCompressionField(ComparisonFormula):
    r"""Class representing formula 8.114 for the verification of the compressive stress in a strut or in a
    compression field developing within the concrete.
    """

    label = "8.114"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(self, sigma_cd: MPA, nu: DIMENSIONLESS, f_cd: MPA) -> None:
        r"""Check whether the compressive stress in a strut or in a compression field does not exceed its
        limit.

        FprEN 1992-1-1:2023 (E) art. 8.5.2(3) - Formula (8.114)

        Parameters
        ----------
        sigma_cd : MPA
            [$\sigma_{cd}$] Compressive stress in a strut or in a compression field developing within the
            concrete, according to Formula (8.113), see
            Form8Dot113CompressiveStressInStrutOrCompressionField [$MPa$].
        nu : DIMENSIONLESS
            [$\nu$] Strength reduction factor, defined in 8.5.2(4) and (5) [$-$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.sigma_cd = sigma_cd
        self.nu = nu
        self.f_cd = f_cd

    @classmethod
    def _comparison_operator(cls) -> Callable[[float, float], bool]:
        """Returns the comparison operator for the formula."""
        return operator.le

    @staticmethod
    def _evaluate_lhs(sigma_cd: MPA, *_args, **_kwargs) -> float:
        """Evaluates the compressive stress, for more information see the __init__ method."""
        raise_if_negative(sigma_cd=sigma_cd)

        return float(sigma_cd)

    @staticmethod
    def _evaluate_rhs(nu: DIMENSIONLESS, f_cd: MPA, *_args, **_kwargs) -> float:
        """Evaluates the limit on the compressive stress, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(nu=nu, f_cd=f_cd)

        return float(nu * f_cd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.114."""
        _equation: str = r"\sigma_{cd} \leq \nu \cdot f_{cd}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\sigma_{cd}": f"{self.sigma_cd:.{n}f}",
                r"\nu": f"{self.nu:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\sigma_{cd}": rf"{self.sigma_cd:.{n}f} \ MPa",
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
