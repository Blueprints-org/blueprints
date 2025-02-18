"""Formula 6.71 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot71CriteriaBasedOnStressRangeLHS(Formula):
    """Class representing Left Hand Side of formula 6.71 for the calculation of the fatigue criteria based on stress range."""

    label = "6.71 (LHS)"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        gamma_f_fat: DIMENSIONLESS,
        delta_sigma_s_equ_n_star: MPA,
    ) -> None:
        r"""[$\Delta\sigma_{Ed}$] Loading side of equation [$MPa$].

        NEN-EN 1993-1-1+C2:2011 art.6.8.5 - Formula (6.71)

        Parameters
        ----------
        gamma_f_fat : DIMENSIONLESS
            [$\gamma_{F,fat}$] Partial factor for fatigue actions [$-$].
        delta_sigma_s_equ_n_star : MPA
            [$\Delta\sigma_{s,equ}(N*)$] Damage equivalent stress range for types of reinforcement and considering number of cycles N* [$MPa$].

        Returns
        -------
        None
        """
        super().__init__()
        self.gamma_f_fat = gamma_f_fat
        self.delta_sigma_s_equ_n_star = delta_sigma_s_equ_n_star

    @staticmethod
    def _evaluate(
        gamma_f_fat: DIMENSIONLESS,
        delta_sigma_s_equ_n_star: MPA,
    ) -> MPA:
        """Evaluates the left hand side formula, for more information see the __init__ method."""
        raise_if_negative(gamma_f_fat=gamma_f_fat, delta_sigma_s_equ_n_star=delta_sigma_s_equ_n_star)
        return gamma_f_fat * delta_sigma_s_equ_n_star

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for left hand side formula 6.71."""
        return LatexFormula(
            return_symbol=r"\Delta \sigma_{Ed}",
            result=f"{self:.3f}",
            equation=r"\gamma_{F,fat} \cdot \Delta \sigma_{s,equ} (N^*)",
            numeric_equation=rf"{self.gamma_f_fat:.3f} \cdot {self.delta_sigma_s_equ_n_star:.3f}",
            comparison_operator_label=r"=",
        )


class Form6Dot71CriteriaBasedOnStressRangeRHS(Formula):
    """Class representing Right Hand Side of formula 6.71 for the calculation of the fatigue criteria based on stress range."""

    label = "6.71 (RHS)"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        delta_sigma_rsk_n_star: MPA,
        gamma_s_fat: DIMENSIONLESS,
    ) -> None:
        r"""[$\Delta\sigma_{Rd}$] Resistance side of equation [$MPa$].

        NEN-EN 1993-1-1+C2:2011 art.6.8.5 - Formula (6.71)

        Parameters
        ----------
        delta_sigma_rsk_n_star : MPA
            [$\Delta\sigma_{Rsk}(N*)$] Stress range at N* cycles from the S-N curve in Figure 6.30 [$MPa$].
        gamma_s_fat : DIMENSIONLESS
            [$\gamma_{S,fat}$] Partial factor for reinforcing or prestressing steel under fatigue loading [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_rsk_n_star = delta_sigma_rsk_n_star
        self.gamma_s_fat = gamma_s_fat

    @staticmethod
    def _evaluate(gamma_s_fat: DIMENSIONLESS, delta_sigma_rsk_n_star: MPA) -> MPA:
        """Evaluates the right hand side formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_rsk_n_star=delta_sigma_rsk_n_star)
        raise_if_less_or_equal_to_zero(gamma_s_fat=gamma_s_fat)
        return delta_sigma_rsk_n_star / gamma_s_fat

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for right hand side formula 6.71."""
        return LatexFormula(
            return_symbol=r"\Delta \sigma_{Rd}",
            result=f"{self:.3f}",
            equation=r"\frac{\Delta \sigma_{Rsk} (N^*)}{\gamma_{s,fat}}",
            numeric_equation=rf"\frac{{{self.delta_sigma_rsk_n_star:.3f}}}{{{self.gamma_s_fat:.3f}}}",
            comparison_operator_label=r"=",
        )


class Form6Dot71CriteriaBasedOnStressRange:
    """Class representing formula 6.71 for the calculation of the fatigue criteria based on stress range."""

    label = "6.71"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        gamma_f_fat: DIMENSIONLESS,
        delta_sigma_s_equ_n_star: MPA,
        delta_sigma_rsk_n_star: MPA,
        gamma_s_fat: DIMENSIONLESS,
    ) -> None:
        r"""[$\text{CHECK}$] Criteria met, based on damage accumulation.

        NEN-EN 1993-1-1+C2:2011 art.6.8.5 - Formula (6.71)

        Parameters
        ----------
        gamma_f_fat : DIMENSIONLESS
            [$\gamma_{F,fat}$] Partial factor for fatigue actions [$-$].
        delta_sigma_s_equ_n_star : MPA
            [$\Delta\sigma_{s,equ}(N*)$] Damage equivalent stress range for types of reinforcement and considering number of cycles N* [$MPa$].
        delta_sigma_rsk_n_star : MPA
            [$\Delta\sigma_{Rsk}(N*)$] Stress range at N* cycles from the S-N curve in Figure 6.30 [$MPa$].
        gamma_s_fat : DIMENSIONLESS
            [$\gamma_{S,fat}$] Partial factor for reinforcing or prestressing steel under fatigue loading [$-$].

        Returns
        -------
        None
        """
        self.gamma_f_fat = gamma_f_fat
        self.delta_sigma_s_equ_n_star = delta_sigma_s_equ_n_star
        self.delta_sigma_rsk_n_star = delta_sigma_rsk_n_star
        self.gamma_s_fat = gamma_s_fat

    @property
    def left_hand_side(self) -> MPA:
        """Calculate the left hand side of the equation.

        Returns
        -------
            MPA: Left hand side, loading side of the equation
        """
        return Form6Dot71CriteriaBasedOnStressRangeLHS(
            gamma_f_fat=self.gamma_f_fat,
            delta_sigma_s_equ_n_star=self.delta_sigma_s_equ_n_star,
        )

    @property
    def right_hand_side(self) -> MPA:
        """Calculate the left hand side of the equation.

        Returns
        -------
            MPA: Right hand side, resistance side of the equation
        """
        return Form6Dot71CriteriaBasedOnStressRangeRHS(
            gamma_s_fat=self.gamma_s_fat,
            delta_sigma_rsk_n_star=self.delta_sigma_rsk_n_star,
        )

    @property
    def ratio(self) -> DIMENSIONLESS:
        """Ratio between left hand side and right hand side of the formula, commonly referred to as unity check."""
        return self.left_hand_side / self.right_hand_side

    def __bool__(self) -> bool:
        """Evaluates the formula, for more information see the __init__ method."""
        lhs = Form6Dot71CriteriaBasedOnStressRangeLHS(gamma_f_fat=self.gamma_f_fat, delta_sigma_s_equ_n_star=self.delta_sigma_s_equ_n_star)
        rhs = Form6Dot71CriteriaBasedOnStressRangeRHS(gamma_s_fat=self.gamma_s_fat, delta_sigma_rsk_n_star=self.delta_sigma_rsk_n_star)
        return lhs <= rhs

    def __str__(self) -> str:
        """Return the result of the formula."""
        return self.latex().complete

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.71."""
        return LatexFormula(
            return_symbol=r"CHECK",
            result="OK" if self.__bool__() else "\\text{Not OK}",
            equation=r"\gamma_{F,fat} \cdot \Delta \sigma_{s,equ} (N^*) \leq \frac{\Delta \sigma_{Rsk} (N^*)}{\gamma_{s,fat}}",
            numeric_equation=(
                rf"{self.gamma_f_fat:.3f} \cdot {self.delta_sigma_s_equ_n_star:.3f} "
                rf"\leq \frac{{{self.delta_sigma_rsk_n_star:.3f}}}{{{self.gamma_s_fat:.3f}}}"
            ),
            comparison_operator_label=r"\rightarrow",
        )
