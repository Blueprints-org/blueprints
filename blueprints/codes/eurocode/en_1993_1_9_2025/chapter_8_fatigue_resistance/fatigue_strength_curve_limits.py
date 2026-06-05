"""Fatigue strength curve limits from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)."""

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import FatigueStrengthCurve, StressType
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_value import Form8FatigueStrengthCurveValue
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_negative


class Form8ConstantAmplitudeFatigueLimit(Formula):
    r"""Class representing the constant amplitude fatigue limit [$\Delta\sigma_D$] at [$N_D$] cycles.

    The constant amplitude fatigue limit is read off the standard fatigue strength curve (EN 1993-1-9:2025,
    Figures 8.1 - 8.4) at [$N_D$], by scaling the detail category [$\Delta\sigma_C$] along the first branch
    (slope [$m_1$]): [$\Delta\sigma_D = \Delta\sigma_C \left( N_C / N_D \right)^{1 / m_1}$]. For shear curves
    (Figure 8.4) this is the shear constant amplitude fatigue limit [$\Delta\tau_D$].
    """

    label = "Figures 8.1-8.4 (constant amplitude fatigue limit)"
    source_document = EN_1993_1_9_2025

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$\Delta\sigma_D$] Constant amplitude fatigue limit at [$N_D$] cycles [$MPa$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For shear curves this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4).

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_c: MPA = delta_sigma_c
        self.curve: FatigueStrengthCurve = curve

    @staticmethod
    def _curve_value(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> Form8FatigueStrengthCurveValue:
        r"""Underlying power-law evaluation of [$\Delta\sigma_D$] from the detail category, used for the numeric value."""
        return Form8FatigueStrengthCurveValue(
            delta_sigma_ref=delta_sigma_c,
            n_ref=curve.n_c,
            n_target=curve.n_d,
            m=curve.m1,
            point="D",
        )

    @staticmethod
    def _evaluate(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_c=delta_sigma_c)
        return float(Form8ConstantAmplitudeFatigueLimit._curve_value(delta_sigma_c, curve))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the constant amplitude fatigue limit (Δτ symbol for shear curves)."""
        symbol = r"\Delta\tau" if self.curve.stress_type == StressType.SHEAR else r"\Delta\sigma"
        # The slope m1 is an integer (3, 5 or 9), so trailing zeros are stripped to keep the exponent clean.
        slope_str = f"{self.curve.m1:.{n}f}"
        if "." in slope_str:
            slope_str = slope_str.rstrip("0").rstrip(".")
        return LatexFormula(
            return_symbol=rf"{symbol}_{{D}}",
            result=f"{self:.{n}f}",
            equation=rf"{symbol}_{{C}} \left( \frac{{N_{{C}}}}{{N_{{D}}}} \right)^{{1 / m_{{1}}}}",
            numeric_equation=(
                rf"{self.delta_sigma_c:.{n}f} \left( \frac{{{latex_scientific(self.curve.n_c)}}}{{{latex_scientific(self.curve.n_d)}}} \right)"
                rf"^{{1 / {slope_str}}}"
            ),
            comparison_operator_label="=",
            unit="MPa",
        )


class Form8CutOffLimit(Formula):
    r"""Class representing the cut-off limit [$\Delta\sigma_L$] at [$N_L$] cycles.

    The cut-off limit is read off the standard fatigue strength curve (EN 1993-1-9:2025, Figures 8.1 - 8.4) at
    [$N_L$], by scaling the constant amplitude fatigue limit [$\Delta\sigma_D$] along the second branch
    (slope [$m_2$]): [$\Delta\sigma_L = \Delta\sigma_D \left( N_D / N_L \right)^{1 / m_2}$].

    Only curves with a second branch have a separate cut-off limit. The shear curve (Figure 8.4) has a single
    slope and its constant amplitude fatigue limit [$\Delta\tau_D$] also acts as the cut-off, so this formula is
    not defined for it (see :attr:`FatigueStrengthCurve.has_cutoff_segment`).
    """

    label = "Figures 8.1-8.4 (cut-off limit)"
    source_document = EN_1993_1_9_2025

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$\Delta\sigma_L$] Cut-off limit at [$N_L$] cycles [$MPa$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4). Must have a separate
            cut-off branch; the shear curve (Figure 8.4) is not allowed.

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_c: MPA = delta_sigma_c
        self.curve: FatigueStrengthCurve = curve

    @staticmethod
    def _curve_value(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> Form8FatigueStrengthCurveValue:
        r"""Underlying power-law evaluation of [$\Delta\sigma_L$] from the fatigue limit, reused for the value and its LaTeX."""
        if curve.m2 is None or curve.n_l is None:
            raise ValueError(
                f"Curve {curve.name} has no separate cut-off limit (single-slope shear curve); "
                "its constant amplitude fatigue limit acts as the cut-off."
            )
        delta_sigma_d = float(Form8ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=curve))
        return Form8FatigueStrengthCurveValue(
            delta_sigma_ref=delta_sigma_d,
            n_ref=curve.n_d,
            n_target=curve.n_l,
            m=curve.m2,
            point="L",
        )

    @staticmethod
    def _evaluate(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_c=delta_sigma_c)
        return float(Form8CutOffLimit._curve_value(delta_sigma_c, curve))

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the cut-off limit."""
        return self._curve_value(self.delta_sigma_c, self.curve).latex(n=n)
