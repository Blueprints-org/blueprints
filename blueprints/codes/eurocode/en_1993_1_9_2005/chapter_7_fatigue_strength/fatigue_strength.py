"""Fatigue strength on a standard fatigue strength curve from EN 1993-1-9:2005: Chapter 7 - Fatigue strength."""

from blueprints.codes.eurocode.en_1993_1_9_2005 import EN_1993_1_9_2005
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import FatigueStrengthCurve, StressType
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve_value import Form7FatigueStrengthCurveValue
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form7FatigueStrength(Formula):
    r"""Class representing the characteristic fatigue strength [$\Delta\sigma_R$] (or [$\Delta\tau_R$]) at a given number of cycles.

    The value is read from one of the standard fatigue strength curves of EN 1993-1-9:2005 (Figures 7.1 - 7.2,
    selected through ``curve``), scaled to the detail category [$\Delta\sigma_C$]. For direct stress (Figure 7.1)
    the extended curve of 7.1(3) is piecewise:

    - first branch (slope [$m = 3$]) for [$N \leq N_D$]: [$\Delta\sigma_R = \Delta\sigma_C \left( N_C / N \right)^{1 / m}$],
    - second branch (slope [$m = 5$]) for [$N_D < N \leq N_L$]: [$\Delta\sigma_R = \Delta\sigma_D \left( N_D / N \right)^{1 / m}$],
    - constant cut-off for [$N > N_L$]: [$\Delta\sigma_R = \Delta\sigma_L$].

    For shear (Figure 7.2, 7.1(2)) there is a single slope ([$m = 5$]) up to the cut-off limit [$\Delta\tau_L$] at
    [$N_L$], beyond which the strength is constant at [$\Delta\tau_L$].

    Note: the second branch of the direct stress curve belongs to the extended fatigue strength curves of 7.1(3),
    intended for stress spectra with ranges above and below the constant amplitude fatigue limit; under purely
    constant amplitude loading (7.1(2)) ranges below [$\Delta\sigma_D$] cause no fatigue damage. Also, only the curve
    relation itself is evaluated; no low-cycle bound (the curves are defined from about [$10^4$] cycles) and no static
    upper stress limit are enforced, so for [$N < N_C$] the first branch is extrapolated and returns
    [$\Delta\sigma_R > \Delta\sigma_C$].
    """

    label = "Figures 7.1-7.2 (fatigue strength)"
    source_document = EN_1993_1_9_2005

    def __init__(self, delta_sigma_c: MPA, curve: FatigueStrengthCurve, n_cycles: DIMENSIONLESS) -> None:
        r"""[$\Delta\sigma_R$] Characteristic fatigue strength at [$N$] cycles on a standard fatigue strength curve [$MPa$].

        EN 1993-1-9:2005 - Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)

        Parameters
        ----------
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For the shear curve this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 7.1 - 7.2), fixing the slopes and the
            reference cycle numbers [$N_C$], [$N_D$], [$N_L$].
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
    def _power_law(delta_sigma_ref: MPA, n_ref: DIMENSIONLESS, n_target: DIMENSIONLESS, m: DIMENSIONLESS, curve: FatigueStrengthCurve) -> MPA:
        """Single power-law step of the fatigue strength curve, reusing the validated engine formula.

        Only the numeric value is taken, so ``point`` is irrelevant here (it merely labels the engine's own LaTeX,
        which is never rendered through this helper); ``"L"`` is valid for both stress types and gives the same result.
        """
        return float(
            Form7FatigueStrengthCurveValue(
                delta_sigma_ref=delta_sigma_ref, n_ref=n_ref, n_target=n_target, m=m, point="L", stress_type=curve.stress_type
            )
        )

    @staticmethod
    def _evaluate(delta_sigma_c: MPA, curve: FatigueStrengthCurve, n_cycles: DIMENSIONLESS) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_c=delta_sigma_c)
        raise_if_less_or_equal_to_zero(n_cycles=n_cycles)

        first_branch_end = curve.n_d if curve.n_d is not None else curve.n_l
        if n_cycles <= first_branch_end:
            # first branch, slope m1 (also covers N < N_C)
            return Form7FatigueStrength._power_law(delta_sigma_c, curve.n_c, n_cycles, curve.m1, curve)
        if curve.n_d is None or curve.m2 is None:
            # shear curve: single slope, constant at the cut-off limit beyond N_L
            return Form7FatigueStrength._power_law(delta_sigma_c, curve.n_c, curve.n_l, curve.m1, curve)
        delta_sigma_d = Form7FatigueStrength._power_law(delta_sigma_c, curve.n_c, curve.n_d, curve.m1, curve)
        if n_cycles <= curve.n_l:
            # second branch, slope m2
            return Form7FatigueStrength._power_law(delta_sigma_d, curve.n_d, n_cycles, curve.m2, curve)
        # cut-off: constant at the cut-off limit beyond N_L
        return Form7FatigueStrength._power_law(delta_sigma_d, curve.n_d, curve.n_l, curve.m2, curve)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the fatigue strength at the requested number of cycles."""
        curve = self.curve
        symbol = r"\Delta\tau" if curve.stress_type == StressType.SHEAR else r"\Delta\sigma"
        first_branch_end = curve.n_d if curve.n_d is not None else curve.n_l

        # Each branch fixes the reference anchor, the slope and the cycle number that appear in the equation.
        if self.n_cycles <= first_branch_end:
            ref_sub, ref_value, ref_n, target_symbol, target_n, slope = "C", self.delta_sigma_c, curve.n_c, "N", self.n_cycles, curve.m1
        elif curve.n_d is None or curve.m2 is None:
            ref_sub, ref_value, ref_n, target_symbol, target_n, slope = "C", self.delta_sigma_c, curve.n_c, "N_{L}", curve.n_l, curve.m1
        else:
            delta_sigma_d = self._power_law(self.delta_sigma_c, curve.n_c, curve.n_d, curve.m1, curve)
            if self.n_cycles <= curve.n_l:
                ref_sub, ref_value, ref_n, target_symbol, target_n, slope = "D", delta_sigma_d, curve.n_d, "N", self.n_cycles, curve.m2
            else:
                ref_sub, ref_value, ref_n, target_symbol, target_n, slope = "D", delta_sigma_d, curve.n_d, "N_{L}", curve.n_l, curve.m2

        # The slope m is an integer (3 or 5), so trailing zeros are stripped to keep the exponent clean.
        slope_str = f"{slope:.{n}f}"
        if "." in slope_str:
            slope_str = slope_str.rstrip("0").rstrip(".")

        return LatexFormula(
            return_symbol=rf"{symbol}_{{R}}",
            result=f"{self:.{n}f}",
            equation=rf"{symbol}_{{{ref_sub}}} \left( \frac{{N_{{{ref_sub}}}}}{{{target_symbol}}} \right)^{{1 / m}}",
            numeric_equation=(
                rf"{ref_value:.{n}f} \left( \frac{{{latex_scientific(ref_n)}}}{{{latex_scientific(target_n)}}} \right)^{{1 / {slope_str}}}"
            ),
            comparison_operator_label="=",
            unit="MPa",
        )
