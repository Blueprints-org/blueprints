"""Formula 8.17 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot17ConfinedUltimateStrain(Formula):
    r"""Class representing formula 8.17 for the calculation of the confined ultimate compressive strain,
    enhanced by confinement.
    """

    label = "8.17"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        sigma_c2d: MPA,
        f_cd: MPA,
    ) -> None:
        r"""[$\varepsilon_{cu,c}$] Confined ultimate compressive strain [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.1.4(5) - Formula (8.17)

        [$\varepsilon_{cu} = 0{,}0035$], the unconfined value used in Formula (8.4), is fixed by the standard
        and is not an input of this class.

        Parameters
        ----------
        sigma_c2d : MPA
            [$\sigma_{c2d}$] Absolute value of the minimum principal transverse compressive stress [$MPa$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.sigma_c2d = sigma_c2d
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        sigma_c2d: MPA,
        f_cd: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sigma_c2d=sigma_c2d)
        raise_if_less_or_equal_to_zero(f_cd=f_cd)

        epsilon_cu = 0.0035
        return epsilon_cu + 0.2 * sigma_c2d / f_cd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.17."""
        _equation: str = r"\varepsilon_{cu} + 0.2 \cdot \frac{\sigma_{c2d}}{f_{cd}}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\varepsilon_{cu}": "0.0035",
                r"\sigma_{c2d}": f"{self.sigma_c2d:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\varepsilon_{cu}": "0.0035",
                r"\sigma_{c2d}": rf"{self.sigma_c2d:.{n}f} \ MPa",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\varepsilon_{cu,c}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
