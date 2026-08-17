"""Fatigue life (number of cycles to failure) on a standard fatigue strength curve from EN 1993-1-9:2005: Chapter 7."""

from blueprints.codes.eurocode.en_1993_1_9_2005 import EN_1993_1_9_2005
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_life_curve_value import Form7FatigueLifeCurveValue
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import FatigueStrengthCurve
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve_limits import (
    Form7ConstantAmplitudeFatigueLimit,
    Form7CutOffLimit,
)
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form7FatigueLife(Formula):
    r"""Class representing the number of cycles to failure [$N_R$] for an applied stress range on a standard fatigue strength curve.

    This is the inverse of :class:`~blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength.Form7FatigueStrength`:
    given a constant-amplitude applied stress range [$\Delta\sigma_R$] (or [$\Delta\tau_R$]) and a detail category
    [$\Delta\sigma_C$], it returns the number of cycles [$N_R$] at which [$\Delta\sigma_R$] meets the characteristic
    fatigue strength curve (EN 1993-1-9:2005, Figures 7.1 - 7.2). It provides the denominator [$N_R$] of the partial
    damage [$n / N_R$] of a Palmgren-Miner accumulation (see Annex A). For direct stress (Figure 7.1) the extended
    curve of 7.1(3) is piecewise:

    - first branch (slope [$m = 3$]), [$\Delta\sigma_R \geq \Delta\sigma_D$]: [$N_R = N_C (\Delta\sigma_C / \Delta\sigma_R)^{m}$],
    - second branch (slope [$m = 5$]), [$\Delta\sigma_L \leq \Delta\sigma_R < \Delta\sigma_D$]: [$N_R = N_D (\Delta\sigma_D / \Delta\sigma_R)^{m}$],
    - below the cut-off limit, [$\Delta\sigma_R < \Delta\sigma_L$]: infinite life [$N_R = \infty$] (no fatigue damage).

    The two finite branches share a single relation, evaluated and rendered by
    :class:`~blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_life_curve_value.Form7FatigueLifeCurveValue`
    (the rearranged curve relation of 7.1(2) and 7.1(3)); this class only selects the governing branch and handles the
    infinite-life case.

    For shear (Figure 7.2) there is a single branch (slope [$m = 5$]) down to the cut-off limit [$\Delta\tau_L$], so
    any [$\Delta\tau_R < \Delta\tau_L$] gives infinite life.

    Note: the second branch of the direct stress curve belongs to the extended fatigue strength curves of 7.1(3),
    intended for stress spectra with ranges above and below the constant amplitude fatigue limit; under purely
    constant amplitude loading (7.1(2)) any [$\Delta\sigma_R < \Delta\sigma_D$] causes no fatigue damage.
    """

    label = "Figures 7.1-7.2 (fatigue life)"
    source_document = EN_1993_1_9_2005

    def __init__(self, delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$N_R$] Number of cycles to failure for an applied stress range on a standard fatigue strength curve [$-$].

        EN 1993-1-9:2005 - Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)

        Parameters
        ----------
        delta_sigma_r : MPA
            [$\Delta\sigma_R$] Applied constant-amplitude stress range to find the fatigue life for [$MPa$].
            For the shear curve this is the applied shear stress range [$\Delta\tau_R$].
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For the shear curve this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 7.1 - 7.2), fixing the slopes and the
            reference cycle numbers [$N_C$], [$N_D$], [$N_L$].

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
        r"""Reference strength and cycle number of the cut-off point [$(\Delta\sigma_L, N_L)$], below which the life is infinite."""
        return float(Form7CutOffLimit(delta_sigma_c=delta_sigma_c, curve=curve)), curve.n_l

    @staticmethod
    def _governing_value(delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> Form7FatigueLifeCurveValue | None:
        r"""Curve-value engine for the branch of ``curve`` that governs [$\Delta\sigma_R$], or ``None`` below the cut-off.

        The fatigue strength curve is piecewise (see :class:`Form7FatigueLife`); the governing branch is the one whose
        stress range covers [$\Delta\sigma_R$]. ``None`` signals the branch below the cut-off limit, where the life is
        infinite and there is no power-law relation to evaluate.
        """
        delta_sigma_l, _ = Form7FatigueLife._cutoff_anchor(delta_sigma_c, curve)
        if delta_sigma_r < delta_sigma_l:
            # below the cut-off limit: infinite life, no damage
            return None

        if curve.n_d is not None and curve.m2 is not None:
            delta_sigma_d = float(Form7ConstantAmplitudeFatigueLimit(delta_sigma_c=delta_sigma_c, curve=curve))
            if delta_sigma_r < delta_sigma_d:
                # second branch (slope m2), anchored at the constant amplitude fatigue limit point (N_D, Δσ_D)
                return Form7FatigueLifeCurveValue(
                    delta_sigma_ref=delta_sigma_d, n_ref=curve.n_d, m=curve.m2, delta_sigma_r=delta_sigma_r, point="D", stress_type=curve.stress_type
                )

        # first branch (slope m1), anchored at the detail category point (N_C, Δσ_C)
        return Form7FatigueLifeCurveValue(
            delta_sigma_ref=delta_sigma_c, n_ref=curve.n_c, m=curve.m1, delta_sigma_r=delta_sigma_r, point="C", stress_type=curve.stress_type
        )

    @staticmethod
    def _evaluate(delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c)

        value = Form7FatigueLife._governing_value(delta_sigma_r, delta_sigma_c, curve)
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
