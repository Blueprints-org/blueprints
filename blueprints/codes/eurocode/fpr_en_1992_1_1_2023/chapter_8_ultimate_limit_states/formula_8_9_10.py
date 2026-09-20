"""Formula 8.9 and 8.10 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot9To10ConcreteStrengthIncreaseConfinement(Formula):
    r"""Class representing formulas 8.9 and 8.10 for the calculation of the compressive strength increase of a
    concrete due to a transverse compressive stress from confinement reinforcement or triaxial compression.
    """

    label = "8.9/8.10"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        sigma_c2d: MPA,
        f_cd: MPA,
        d_dg: MM,
    ) -> None:
        r"""[$\Delta f_{cd}$] Compressive strength increase of a concrete due to a transverse compressive
        stress [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.1.4(2) - Formula (8.9) and (8.10)

        In case of concrete with [$d_{dg} < 32$] mm, the strength increase is reduced by the factor
        [$d_{dg}/32$ mm]; that reduction is applied inside this class rather than as a separate step.

        Parameters
        ----------
        sigma_c2d : MPA
            [$\sigma_{c2d}$] Absolute value of the minimum principal transverse compressive stress [$MPa$].
        f_cd : MPA
            [$f_{cd}$] Design value of the compressive strength of concrete [$MPa$].
        d_dg : MM
            [$d_{dg}$] Size parameter describing the failure zone roughness, according to 8.2.1(4) [$mm$].
        """
        super().__init__()
        self.sigma_c2d = sigma_c2d
        self.f_cd = f_cd
        self.d_dg = d_dg

    @staticmethod
    def _evaluate(
        sigma_c2d: MPA,
        f_cd: MPA,
        d_dg: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sigma_c2d=sigma_c2d, f_cd=f_cd)
        raise_if_less_or_equal_to_zero(d_dg=d_dg)

        delta_f_cd = 4 * sigma_c2d if sigma_c2d <= 0.6 * f_cd else 3.5 * sigma_c2d ** (3 / 4) * f_cd ** (1 / 4)

        reduction_factor = min(d_dg / 32, 1.0)
        return delta_f_cd * reduction_factor

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formulas 8.9 and 8.10."""
        _equation: str = (
            r"\min\left(\frac{d_{dg}}{32}, 1.0\right) \cdot "
            r"\begin{cases} 4 \cdot \sigma_{c2d} & \text{for } \sigma_{c2d} \leq 0.6 \cdot f_{cd} \\ "
            r"3.5 \cdot \left(\sigma_{c2d}\right)^{3/4} \cdot \left(f_{cd}\right)^{1/4} & \text{for } \sigma_{c2d} > 0.6 \cdot f_{cd} "
            r"\end{cases}"
        )
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_{dg}": f"{self.d_dg:.{n}f}",
                r"\sigma_{c2d}": f"{self.sigma_c2d:.{n}f}",
                r"f_{cd}": f"{self.f_cd:.{n}f}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"d_{dg}": rf"{self.d_dg:.{n}f} \ mm",
                r"\sigma_{c2d}": rf"{self.sigma_c2d:.{n}f} \ MPa",
                r"f_{cd}": rf"{self.f_cd:.{n}f} \ MPa",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"\Delta f_{cd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
