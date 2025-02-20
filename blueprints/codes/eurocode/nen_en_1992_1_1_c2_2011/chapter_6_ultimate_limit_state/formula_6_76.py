"""Formula 6.76 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form6Dot76DesignFatigueStrengthConcrete(Formula):
    """Class representing formula 6.76 for the design fatigue strength of concrete, [$f_{cd,fat}$]."""

    label = "6.76"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        k_1: DIMENSIONLESS,
        beta_cc_t0: DIMENSIONLESS,
        f_cd: MPA,
        f_ck: MPA,
    ) -> None:
        r"""[$f_{cd,fat}$] Design fatigue strength of concrete in [$MPa$].

        NEN-EN 1992-1-1+C2:2011 art. 6.8.7(1) - Formula (6.76)

        Parameters
        ----------
        k_1 : DIMENSIONLESS
            [$k_{1}$] k1 factor [$-$]
        beta_cc_t0 : DIMENSIONLESS
            [$β_{cc}(t_0)$] Coefficient for concrete strength at first load application see (3.1.2 (6)) [$-$].
            [$t_0$] The time of the start of the cyclic loading in concrete in days.
        f_cd : MPA
            [$f_{cd}$] Design strength of concrete [$MPa$]
        f_ck : MPA
            [$f_{ck}$] Characteristic strength of concrete [$MPa$]

        """
        super().__init__()
        self.k_1 = k_1
        self.beta_cc_t0 = beta_cc_t0
        self.f_cd = f_cd
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        k_1: DIMENSIONLESS,
        beta_cc_t0: DIMENSIONLESS,
        f_cd: MPA,
        f_ck: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(k_1=k_1, beta_cc_t0=beta_cc_t0, f_cd=f_cd, f_ck=f_ck)

        return k_1 * beta_cc_t0 * f_cd * (1 - f_ck / 250)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.76."""
        return LatexFormula(
            return_symbol=r"f_{cd,fat}",
            result=f"{self:.3f}",
            equation=r"k_{1} \cdot β_{cc}(t_0) \cdot f_{cd} \cdot \left(1-\frac{f_{ck}}{250}\right)",
            numeric_equation=rf"{self.k_1:.3f} \cdot {self.beta_cc_t0:.3f} \cdot {self.f_cd:.3f} \cdot "
            rf"\left(1-\frac{{{self.f_ck:.3f}}}{{250}}\right)",
            comparison_operator_label="=",
        )
