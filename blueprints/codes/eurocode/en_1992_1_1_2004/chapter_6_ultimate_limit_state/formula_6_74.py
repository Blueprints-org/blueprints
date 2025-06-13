"""Formula 6.74 from EN 1992-1-1:2004: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot74MinimumCompressiveStressLevel(Formula):
    r"""Class representing formula 6.74 for the calculation of the minimum compressive stress level [$E_{cd,min,equ}$]."""

    label = "6.74"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        sigma_cd_min_equ: MPA,
        f_cd_fat: MPA,
    ) -> None:
        r"""[$E_{cd,min,equ}$] Calculation of the minimum compressive stress level.

        EN 1992-1-1:2004 art.6.8.7(1) - Formula (6.74)

        Parameters
        ----------
        sigma_cd_min_equ : MPA
            [$\sigma_{cd,min,equ}$] Lower stress of the ultimate amplitude for N cycles [$MPa$].
        f_cd_fat : MPA
            [$f_{cd,fat}$] Design fatigue strength of concrete according to (6.76) [$MPa$].
        """
        super().__init__()
        self.sigma_cd_min_equ = sigma_cd_min_equ
        self.f_cd_fat = f_cd_fat

    @staticmethod
    def _evaluate(
        sigma_cd_min_equ: MPA,
        f_cd_fat: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sigma_cd_min_equ=sigma_cd_min_equ)
        raise_if_less_or_equal_to_zero(f_cd_fat=f_cd_fat)

        return sigma_cd_min_equ / f_cd_fat

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.74."""
        _equation: str = r"\frac{\sigma_{cd,min,equ}}{f_{cd,fat}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\sigma_{cd,min,equ}": f"{self.sigma_cd_min_equ:.{n}f}",
                r"f_{cd,fat}": f"{self.f_cd_fat:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"E_{cd,min,equ}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
