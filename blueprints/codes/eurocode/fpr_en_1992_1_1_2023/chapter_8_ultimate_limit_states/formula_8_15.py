"""Formula 8.15 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8Dot15AverageConfinedConcreteStrength(Formula):
    r"""Class representing formula 8.15 for the calculation of the average design compressive strength of
    confined concrete.
    """

    label = "8.15"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        f_cd: MPA,
        k_conf_b: DIMENSIONLESS,
        k_conf_s: DIMENSIONLESS,
        delta_f_cd: MPA,
    ) -> None:
        r"""[$f_{cd,c}$] Average design compressive strength of confined concrete, smeared over the compression
        zone [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.1.4(4) - Formula (8.15)

        Parameters
        ----------
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        k_conf_b : DIMENSIONLESS
            [$k_{conf,b}$] Effectiveness factor accounting for the shape of the compression zone and of the
            confinement reinforcement, according to Table 8.1 [$-$].
        k_conf_s : DIMENSIONLESS
            [$k_{conf,s}$] Effectiveness factor accounting for the spacing of the confinement reinforcement,
            according to Table 8.1 [$-$].
        delta_f_cd : MPA
            [$\Delta f_{cd}$] Compressive strength increase of the confined concrete according to Formula
            (8.9) or (8.10), see Form8Dot9To10ConcreteStrengthIncreaseConfinement [$MPa$].
        """
        super().__init__()
        self.f_cd = f_cd
        self.k_conf_b = k_conf_b
        self.k_conf_s = k_conf_s
        self.delta_f_cd = delta_f_cd

    @staticmethod
    def _evaluate(
        f_cd: MPA,
        k_conf_b: DIMENSIONLESS,
        k_conf_s: DIMENSIONLESS,
        delta_f_cd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_cd=f_cd, k_conf_b=k_conf_b, k_conf_s=k_conf_s, delta_f_cd=delta_f_cd)

        return f_cd + k_conf_b * k_conf_s * delta_f_cd

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.15."""
        _equation: str = r"f_{cd} + k_{conf,b} \cdot k_{conf,s} \cdot \Delta f_{cd}"
        # \Delta f_{cd} is substituted before the bare f_{cd}, since f_{cd} is a literal substring of
        # \Delta f_{cd} and would otherwise also match there.
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\Delta f_{cd}": f"{self.delta_f_cd:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
                r"k_{conf,b}": f"{self.k_conf_b:.{n}f}",
                r"k_{conf,s}": f"{self.k_conf_s:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\Delta f_{cd}": rf"{self.delta_f_cd:.{n}f} \ MPa",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
                r"k_{conf,b}": f"{self.k_conf_b:.{n}f}",
                r"k_{conf,s}": f"{self.k_conf_s:.{n}f}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"f_{cd,c}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
