"""Fatigue life (number of cycles to failure) on a standard fatigue strength curve from EN 1993-1-9:2025: Chapter 8."""

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_life_curve_value import Form8FatigueLifeCurveValue
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_limits import (
    Form8ConstantAmplitudeFatigueLimit,
    Form8CutOffLimit,
)
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form8FatigueLife(Formula):
    r"""Class representing the number of cycles to failure [$N_R$] for an applied stress range on a standard fatigue strength curve.

    This is the inverse of :class:`~blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength.Form8FatigueStrength`:
    given a constant-amplitude applied stress range [$\Delta\sigma_R$] (or [$\Delta\tau_R$]) and a detail category
    [$\Delta\sigma_C$], it returns the number of cycles [$N_R$] at which [$\Delta\sigma_R$] meets the characteristic
    fatigue strength curve (EN 1993-1-9:2025, Figures 8.1 - 8.4). It provides the denominator [$N_R$] of the partial
    damage [$n / N_R$] of a Palmgren-Miner accumulation. The curve is piecewise:

    - first branch (slope [$m_1$]), [$\Delta\sigma_R \geq \Delta\sigma_D$]: [$N_R = N_C (\Delta\sigma_C / \Delta\sigma_R)^{m_1}$],
    - second branch (slope [$m_2$]), [$\Delta\sigma_L \leq \Delta\sigma_R < \Delta\sigma_D$]: [$N_R = N_D (\Delta\sigma_D / \Delta\sigma_R)^{m_2}$],
    - below the cut-off limit, [$\Delta\sigma_R < \Delta\sigma_L$]: infinite life [$N_R = \infty$] (no fatigue damage).

    The two finite branches share a single relation, evaluated and rendered by
    :class:`~blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_life_curve_value.Form8FatigueLifeCurveValue`
    (the inverse of the strength-side curve value engine); this class only selects the governing branch and handles the
    infinite-life case.

    For the shear curve (Figure 8.4) there is a single slope and the constant amplitude fatigue limit [$\Delta\tau_D$]
    acts as the cut-off, so any [$\Delta\tau_R < \Delta\tau_D$] gives infinite life.
    """

    label = "Figures 8.1-8.4 (fatigue life)"
    source_document = EN_1993_1_9_2025

    def __init__(self, delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$N_R$] Number of cycles to failure for an applied stress range on a standard fatigue strength curve [$-$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)

        Parameters
        ----------
        delta_sigma_r : MPA
            [$\Delta\sigma_R$] Applied constant-amplitude stress range to find the fatigue life for [$MPa$].
            For shear curves this is the applied shear stress range [$\Delta\tau_R$].
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For shear curves this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4), fixing the slopes
            [$m_1$], [$m_2$] and the reference cycle numbers [$N_C$], [$N_D$], [$N_L$].

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_r: MPA = delta_sigma_r
        self.delta_sigma_c: MPA = delta_sigma_c
        self.curve: FatigueStrengthCurve = curve

    @staticmethod
    def _cutoff_anchor(delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> tuple[MPA, DIMENSIONLESS]:
        r"""Reference strength and cycle number of the cut-off point, below which the life is infinite.

        For curves with a second branch this is the cut-off limit [$(\Delta\sigma_L, N_L)$]; for the single-slope
        shear curve it is the constant amplitude fatigue limit [$(\Delta\tau_D, N_D)$], which also acts as the cut-off.
        """
        if curve.has_cutoff_segment:
            return float(Form8CutOffLimit(delta_sigma_c=delta_sigma_c, curve=curve)), curve.n_l or curve.n_d
        return float(Form8ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=curve)), curve.n_d

    @staticmethod
    def _governing_value(delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> Form8FatigueLifeCurveValue | None:
        r"""Curve-value engine for the branch of ``curve`` that governs [$\Delta\sigma_R$], or ``None`` below the cut-off.

        The fatigue strength curve is piecewise (see :class:`Form8FatigueLife`); the governing branch is the one whose
        stress range covers [$\Delta\sigma_R$]. ``None`` signals the branch below the cut-off limit, where the life is
        infinite and there is no power-law relation to evaluate.
        """
        delta_sigma_d = float(Form8ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=curve))
        if delta_sigma_r >= delta_sigma_d:
            # first branch (slope m1), anchored at the detail category point (N_C, Δσ_C)
            return Form8FatigueLifeCurveValue(
                delta_sigma_ref=delta_sigma_c, n_ref=curve.n_c, m=curve.m1, delta_sigma_r=delta_sigma_r, point="C", stress_type=curve.stress_type
            )

        if curve.m2 is not None and curve.n_l is not None:
            # second branch (slope m2), anchored at the constant amplitude fatigue limit point (N_D, Δσ_D)
            delta_sigma_l, _ = Form8FatigueLife._cutoff_anchor(delta_sigma_c, curve)
            if delta_sigma_r >= delta_sigma_l:
                return Form8FatigueLifeCurveValue(
                    delta_sigma_ref=delta_sigma_d, n_ref=curve.n_d, m=curve.m2, delta_sigma_r=delta_sigma_r, point="D", stress_type=curve.stress_type
                )

        # below the cut-off limit Δσ_L (or below Δτ_D for the single-slope shear curve): infinite life, no damage
        return None

    @staticmethod
    def _evaluate(delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c)

        value = Form8FatigueLife._governing_value(delta_sigma_r, delta_sigma_c, curve)
        if value is None:
            # below the cut-off limit: infinite life, no damage
            return float("inf")
        return float(value)

    @property
    def detailed_result(self) -> dict:
        r"""Reference anchor of the governing branch, so callers can label [$N_R$] without re-deriving the branch.

        Returns
        -------
        dict
            ``reference_point`` ("C", "D" or "L"), the governing reference strength ``delta_sigma_ref`` [$MPa$]
            ([$\Delta\sigma_C$], [$\Delta\sigma_D$] or [$\Delta\sigma_L$]), its cycle number ``n_ref`` [$-$], the
            governing slope ``m`` [$-$] (``None`` below the cut-off) and the fatigue life ``n_r`` [$-$].
        """
        value = self._governing_value(self.delta_sigma_r, self.delta_sigma_c, self.curve)
        if value is None:
            delta_sigma_ref, n_ref = self._cutoff_anchor(self.delta_sigma_c, self.curve)
            return {"reference_point": "L", "delta_sigma_ref": delta_sigma_ref, "n_ref": n_ref, "m": None, "n_r": float(self)}
        return {"reference_point": value.point, "delta_sigma_ref": value.delta_sigma_ref, "n_ref": value.n_ref, "m": value.m, "n_r": float(self)}

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the fatigue life at the applied stress range."""
        value = self._governing_value(self.delta_sigma_r, self.delta_sigma_c, self.curve)
        if value is None:
            # below the cut-off limit: the life is infinite, so there is no fraction to evaluate
            return LatexFormula(return_symbol="N_{R}", result=r"\infty", comparison_operator_label="=")
        return value.latex(n=n)
