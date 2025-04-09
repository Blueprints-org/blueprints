"""Formula 6.77 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot77FatigueVerification(Formula):
    r"""Class representing formula 6.77 for the fatigue verification of concrete."""

    label = "6.77"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        sigma_c_max: MPA,
        sigma_c_min: MPA,
        f_cd_fat: MPA,
        f_ck: MPA,
    ) -> None:
        r"""[$\sigma_{Rd,max}$] Fatigue verification for concrete [$-$].

        NEN-EN 1992-1-1+C2:2011 art.6.8.7(2) - Formula (6.77)

        Parameters
        ----------
        sigma_c_max : MPA
            [$\sigma_{c,max}$] Maximum compressive stress at a fibre under the frequent load combination [$MPa$].
        sigma_c_min : MPA
            [$\sigma_{c,min}$] Minimum compressive stress at the same fibre where the maximum occurs [$MPa$].
        f_cd_fat : MPA
            [$f_{cd,fat}$] Design compressive strength of concrete under fatigue [$MPa$].
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.sigma_c_max = sigma_c_max
        self.sigma_c_min = sigma_c_min
        self.f_cd_fat = f_cd_fat
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        sigma_c_max: MPA,
        sigma_c_min: MPA,
        f_cd_fat: MPA,
        f_ck: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(sigma_c_max=sigma_c_max, sigma_c_min=sigma_c_min, f_ck=f_ck)
        raise_if_less_or_equal_to_zero(f_cd_fat=f_cd_fat)

        return sigma_c_max / f_cd_fat <= min(0.5 + 0.45 * sigma_c_min / f_cd_fat, 0.9 if f_ck <= 50 else 0.8)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.77."""
        _equation: str = (
            r"\frac{\sigma_{c,max}}{f_{cd,fat}} \leq \min\left(0.5 + 0.45 \cdot \frac{\sigma_{c,min}}{f_{cd,fat}}, \begin{cases} 0.9 & "
            r"\text{if } f_{ck} \leq 50 \\ 0.8 & \text{if } f_{ck} > 50 \end{cases}\right)"
        )
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\sigma_{c,max}": f"{self.sigma_c_max:.3f}",
                r"\sigma_{c,min}": f"{self.sigma_c_min:.3f}",
                "f_{cd,fat}": f"{self.f_cd_fat:.3f}",
                "f_{ck}": f"{self.f_ck:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="\\to",
            unit="",
        )
