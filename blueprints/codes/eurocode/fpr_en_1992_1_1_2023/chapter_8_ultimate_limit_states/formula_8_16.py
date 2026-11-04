"""Formula 8.16 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot16ConfinedStrainAtPeakStress(Formula):
    r"""Class representing formula 8.16 for the calculation of the confined compressive strain at peak
    stress, enhanced by confinement.
    """

    label = "8.16"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        delta_f_cd: MPA,
        f_cd: MPA,
    ) -> None:
        r"""[$\varepsilon_{c2,c}$] Confined compressive strain at peak stress [$-$].

        FprEN 1992-1-1:2023 (E) art. 8.1.4(5) - Formula (8.16)

        [$\varepsilon_{c2} = 0{,}002$], the unconfined value used in Formula (8.4), is fixed by the standard
        and is not an input of this class.

        Parameters
        ----------
        delta_f_cd : MPA
            [$\Delta f_{cd}$] Compressive strength increase of the confined concrete according to Formula
            (8.9) or (8.10), see Form8Dot9To10ConcreteStrengthIncreaseConfinement [$MPa$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.delta_f_cd = delta_f_cd
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        delta_f_cd: MPA,
        f_cd: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_f_cd=delta_f_cd)
        raise_if_less_or_equal_to_zero(f_cd=f_cd)

        epsilon_c2 = 0.002
        return epsilon_c2 * (1 + 5 * delta_f_cd / f_cd)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.16."""
        _equation: str = r"\varepsilon_{c2} \cdot \left(1 + 5 \cdot \frac{\Delta f_{cd}}{f_{cd}}\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\varepsilon_{c2}": "0.002",
                r"\Delta f_{cd}": f"{self.delta_f_cd:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\varepsilon_{c2}": "0.002",
                r"\Delta f_{cd}": rf"{self.delta_f_cd:.{n}f} \ MPa",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\varepsilon_{c2,c}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="-",
        )
