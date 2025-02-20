"""Formula 6.73 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot73StressRatio(Formula):
    r"""Class representing formula 6.73 for the calculation of [$R_{equ}$]."""

    label = "6.73"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        e_cd_min_equ: MPA,
        e_cd_max_equ: MPA,
    ) -> None:
        r"""[$R_{equ}$] Calculation of stress ratio.

        NEN-EN 1992-1-1+C2:2011 art.6.8.7(1) - Formula (6.73)

        Parameters
        ----------
        e_cd_min_equ : MPA
            [$E_{cd,min,equ}$] Minimum compressive stress level [$MPa$].
        e_cd_max_equ : MPA
            [$E_{cd,max,equ}$] Maximum compressive stress level [$MPa$].
        """
        super().__init__()
        self.e_cd_min_equ = e_cd_min_equ
        self.e_cd_max_equ = e_cd_max_equ

    @staticmethod
    def _evaluate(
        e_cd_min_equ: MPA,
        e_cd_max_equ: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(e_cd_min_equ=e_cd_min_equ)
        raise_if_less_or_equal_to_zero(e_cd_max_equ=e_cd_max_equ)

        return e_cd_min_equ / e_cd_max_equ

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.73."""
        _equation: str = r"\frac{E_{cd,min,equ}}{E_{cd,max,equ}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"E_{cd,min,equ}": f"{self.e_cd_min_equ:.3f}",
                r"E_{cd,max,equ}": f"{self.e_cd_max_equ:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"R_{equ}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="",
        )
