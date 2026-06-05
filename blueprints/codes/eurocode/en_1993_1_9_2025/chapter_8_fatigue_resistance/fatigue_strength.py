"""Fatigue strength on a standard fatigue strength curve from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance."""

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import FatigueStrengthCurve, StressType
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_value import Form8FatigueStrengthCurveValue
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


def _power_law(delta_sigma_ref: MPA, n_ref: DIMENSIONLESS, n_target: DIMENSIONLESS, m: DIMENSIONLESS) -> MPA:
    """Single power-law step of the fatigue strength curve, reusing the validated engine formula.

    Only the numeric value is taken, so ``point`` is irrelevant here (it merely labels the engine's own
    LaTeX, which is never rendered through this helper); any valid point would give the same result.
    """
    return float(Form8FatigueStrengthCurveValue(delta_sigma_ref=delta_sigma_ref, n_ref=n_ref, n_target=n_target, m=m, point="D"))


class Form8FatigueStrength(Formula):
    r"""Class representing the characteristic fatigue strength [$\Delta\sigma_R$] (or [$\Delta\tau_R$]) at a given number of cycles.

    The value is read from one of the standard fatigue strength curves of EN 1993-1-9:2025 (Figures 8.1 - 8.4,
    selected through ``curve``), scaled to the detail category [$\Delta\sigma_C$]. The curve is piecewise:

    - first branch (slope [$m_1$]) for [$N \leq N_D$]: [$\Delta\sigma_R = \Delta\sigma_C \left( N_C / N \right)^{1 / m_1}$],
    - second branch (slope [$m_2$]) for [$N_D < N \leq N_L$]: [$\Delta\sigma_R = \Delta\sigma_D \left( N_D / N \right)^{1 / m_2}$],
    - constant cut-off for [$N > N_L$]: [$\Delta\sigma_R = \Delta\sigma_L$].

    For the shear curve (Figure 8.4) there is a single slope and the constant amplitude fatigue limit [$\Delta\tau_D$]
    also acts as the cut-off for [$N > N_D$].

    Note: only the curve relation itself is evaluated; no low-cycle bound (the curves are defined from about
    [$10^4$] cycles) and no static upper stress limit are enforced, so for [$N < N_C$] the first branch is
    extrapolated and returns [$\Delta\sigma_R > \Delta\sigma_C$].
    """

    label = "Figures 8.1-8.4 (fatigue strength)"
    source_document = EN_1993_1_9_2025

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve, n_cycles: DIMENSIONLESS) -> None:
        r"""[$\Delta\sigma_R$] Characteristic fatigue strength at [$N$] cycles on a standard fatigue strength curve [$MPa$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For shear curves this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4), fixing the slopes
            [$m_1$], [$m_2$] and the reference cycle numbers [$N_C$], [$N_D$], [$N_L$].
        n_cycles : DIMENSIONLESS
            [$N$] Number of cycles at which the fatigue strength is evaluated [$-$].

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_c: MPA = delta_sigma_c
        self.curve: FatigueStrengthCurve = curve
        self.n_cycles: DIMENSIONLESS = n_cycles

    @staticmethod
    def _evaluate(delta_sigma_c: MPA, curve: FatigueStrengthCurve, n_cycles: DIMENSIONLESS) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_c=delta_sigma_c)
        raise_if_less_or_equal_to_zero(n_cycles=n_cycles)

        delta_sigma_d = _power_law(delta_sigma_c, curve.n_c, curve.n_d, curve.m1)
        if n_cycles <= curve.n_d:
            # first branch, slope m1 (also covers N < N_C)
            return _power_law(delta_sigma_c, curve.n_c, n_cycles, curve.m1)
        if curve.m2 is None or curve.n_l is None:
            # shear curve: single slope, constant at the fatigue limit beyond N_D
            return delta_sigma_d
        if n_cycles <= curve.n_l:
            # second branch, slope m2
            return _power_law(delta_sigma_d, curve.n_d, n_cycles, curve.m2)
        # cut-off: constant at the cut-off limit beyond N_L
        return _power_law(delta_sigma_d, curve.n_d, curve.n_l, curve.m2)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the fatigue strength at the requested number of cycles."""
        curve = self.curve
        symbol = r"\Delta\tau" if curve.stress_type == StressType.SHEAR else r"\Delta\sigma"
        delta_sigma_d = _power_law(self.delta_sigma_c, curve.n_c, curve.n_d, curve.m1)

        # Each branch fixes the reference anchor, the slope and the cycle number that appear in the equation.
        if self.n_cycles <= curve.n_d:
            ref_sub, ref_value, ref_n, target_symbol, target_n, slope, slope_sub = (
                "C",
                self.delta_sigma_c,
                curve.n_c,
                "N",
                self.n_cycles,
                curve.m1,
                "1",
            )
        elif curve.m2 is None or curve.n_l is None:
            ref_sub, ref_value, ref_n, target_symbol, target_n, slope, slope_sub = (
                "C",
                self.delta_sigma_c,
                curve.n_c,
                "N_{D}",
                curve.n_d,
                curve.m1,
                "1",
            )
        elif self.n_cycles <= curve.n_l:
            ref_sub, ref_value, ref_n, target_symbol, target_n, slope, slope_sub = "D", delta_sigma_d, curve.n_d, "N", self.n_cycles, curve.m2, "2"
        else:
            ref_sub, ref_value, ref_n, target_symbol, target_n, slope, slope_sub = "D", delta_sigma_d, curve.n_d, "N_{L}", curve.n_l, curve.m2, "2"

        # The slope m is an integer (m1, m2 in {3, 5, 9}), so trailing zeros are stripped to keep the exponent clean.
        slope_str = f"{slope:.{n}f}"
        if "." in slope_str:
            slope_str = slope_str.rstrip("0").rstrip(".")

        return LatexFormula(
            return_symbol=rf"{symbol}_{{R}}",
            result=f"{self:.{n}f}",
            equation=rf"{symbol}_{{{ref_sub}}} \left( \frac{{N_{{{ref_sub}}}}}{{{target_symbol}}} \right)^{{1 / m_{{{slope_sub}}}}}",
            numeric_equation=(
                rf"{ref_value:.{n}f} \left( \frac{{{latex_scientific(ref_n)}}}{{{latex_scientific(target_n)}}} \right)^{{1 / {slope_str}}}"
            ),
            comparison_operator_label="=",
            unit="MPa",
        )
